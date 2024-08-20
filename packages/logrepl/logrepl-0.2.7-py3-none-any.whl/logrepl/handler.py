from pathlib import Path
from datetime import datetime
import sys

# import readline
import builtins
import time
from contextlib import contextmanager
from io import TextIOWrapper
from threading import Thread
from dotenv import dotenv_values
from functools import reduce
from queue import Queue
import traceback

nm_config_dir = "dir"
nm_config_prefix = "prefix"
nm_config_err_acc_time = "err_acc_time"
fname_config = ".pylogrepl"
default_dir = "."
default_err_acc_time = 1.0
default_will_log = True

is_debug = False


def debug_write(msg):
    if is_debug:
        with open("debug.log", "a") as log:
            log.write(f"{msg}\n")


# builtin_read = sys.__stdin__.read
# builtin_readline = sys.__stdin__.readline
builtin_input = builtins.input
builtin_stdout_write = sys.__stdout__.write
builtin_stderr_write = sys.__stderr__.write


def gen_log_fname(prefix=None):
    t_tag = datetime.now().strftime("%Y%m%d%H%M")
    fname = f"{t_tag}.log"
    if prefix is not None:
        fname = f"{prefix}_{fname}"
    return fname


class LogOutWrapper(TextIOWrapper):
    def __init__(self, ref: TextIOWrapper, decorate):
        super(LogOutWrapper, self).__init__(
            ref.buffer,
            encoding=ref.encoding,
            errors=ref.errors,
            line_buffering=ref.line_buffering,
            write_through=ref.write_through,
            # newline use default
        )
        self.write_fn = ref.write
        self.write = decorate(self.write_fn)

    def __del__(self):
        pass


class LogInWrapper(TextIOWrapper):
    def __init__(self, ref: TextIOWrapper, decorate):
        super(LogInWrapper, self).__init__(
            ref.buffer,
            encoding=ref.encoding,
            errors=ref.errors,
            line_buffering=ref.line_buffering,
            write_through=ref.write_through,
            # newline use default
        )
        self.read_fn = ref.read
        self.readline_fn = ref.readline
        self.read = decorate(self.read_fn)
        self.readline = decorate(self.readline_fn)

    def __del__(self):
        pass


def arg_config_default(arg, dict_config, nm_config, default, type_fn):
    if arg is None:
        if nm_config in dict_config:
            return type_fn(dict_config[nm_config])
        else:
            return default
    else:
        return arg


class Handler:

    def __init__(
        self,
        log_dir=default_dir,
        prefix=None,
        err_acc_time=default_err_acc_time,
        will_log=default_will_log,
        is_repl=False,
    ):

        self.log_dir = Path(log_dir)
        self.prefix = prefix
        self.update_suffix()
        self.will_log = will_log

        self.err_acc_time = err_acc_time
        self.last_err_time = None
        self.errors = Queue()
        self.err_thread = None
        self.is_repl = is_repl

    @classmethod
    def from_env(
        cls,
        log_dir=None,
        prefix=None,
        err_acc_time=None,
        is_repl=None,
    ):
        config = dotenv_values(fname_config)

        log_dir = arg_config_default(
            log_dir, config, nm_config_dir, default_dir, str
        )

        if prefix is None and nm_config_prefix in config:
            prefix = str(config[nm_config_prefix])

        err_acc_time = arg_config_default(
            err_acc_time,
            config,
            nm_config_err_acc_time,
            default_err_acc_time,
            float,
        )

        if is_repl is None:
            is_repl = False

        return cls(log_dir, prefix, err_acc_time, True, is_repl)

    def set_dir(self, log_dir):
        """
        Update new logging dir.
        log_dir must be string or Path.
        The suffix _yyyymmddhhmm.log will also be updated.
        """
        self.log_dir = Path(log_dir)
        self.update_suffix(self)

    def set_prefix(self, prefix):
        """
        Update new prefix for the log file.
        `prefix` sholud be `str` or `None`.
        The suffix `_yyyymmddhhmm.log` will also be updated
        while the `log_dir` will remain unchanged.
        Drop the prefix of new log file by setting `prefix` as `None`.
        """
        self.prefix = prefix
        self.update_suffix()

    def update_suffix(self):
        """
        Update the timestamp suffix with `log_dir` & `prefix` unchanged.
        """
        self.log_file = gen_log_fname(self.prefix)

    def set_will_log(self, log_or_not):
        self.will_log = log_or_not

    def get_path(self):
        if self.log_file is None:
            raise ValueError("logrepl log_file is None.")
        return self.log_dir / self.log_file

    def check_dir_write(self, msg):
        if self.will_log:
            # raise Exception(f'dead {self.errors.qsize() % 2}') # for debug
            self.log_dir.mkdir(exist_ok=True, parents=True)
            with open(self.get_path(), "a") as log:
                log.write(msg)

    def decorate_log_out(self, fn):
        def new_func(*args, **kwargs):
            try:
                self.check_dir_write(args[0])
            except Exception as e:
                self.add_err(str(e))
            finally:
                return fn(*args, **kwargs)

        return new_func

    def decorate_log_in(self, fn):
        def new_func(*args, **kwargs):
            s = fn(*args, **kwargs)
            try:
                self.check_dir_write(s)
            except Exception as e:
                self.add_err(str(e))
            finally:
                return s

        return new_func

    def gen_logged_input(self):

        def logged_input(prompt=""):
            got = builtin_input(prompt)
            try:
                self.check_dir_write(f"{prompt}{got}\n")
            except Exception as e:
                self.add_err(str(e))
            finally:
                return got

        return logged_input

    def set_io(self):
        sys.stdout = LogOutWrapper(sys.__stdout__, self.decorate_log_out)
        sys.stderr = LogOutWrapper(sys.__stderr__, self.decorate_log_out)
        sys.stdin = LogInWrapper(sys.__stdin__, self.decorate_log_in)
        builtins.input = self.gen_logged_input()

    def show_err(self):
        try:
            time_diff = time.time() - self.last_err_time
            while time_diff < self.err_acc_time:
                time.sleep(self.err_acc_time)
                time_diff = time.time() - self.last_err_time

            set_errs = set()
            while not self.errors.empty():
                set_errs.add(str(self.errors.get(block=False)))

            msg = (
                reduce(
                    lambda acc, x: acc + f"{x}\n",
                    set_errs,
                    "\nlogrepl got errors (ignore the duplicated ones):\n",
                )
                + "\n"
            )

            if self.is_repl:
                msg += ">>> "

            builtin_stderr_write(msg)

        except Exception as e:
            debug_write(str(e))
            builtin_stderr_write(str(e))

    def add_err(self, err):
        try:
            self.last_err_time = time.time()
            self.errors.put(err)
            if self.err_thread is None or not self.err_thread.is_alive():
                thr = Thread(target=self.show_err)
                thr.start()
                self.err_thread = thr
        except Exception as e:
            debug_write(str(e))
            builtin_stderr_write(str(e))

    def exit(self):
        if self.err_thread is not None and self.err_thread.is_alive():
            self.is_repl = False
            self.err_thread.join()
            # builtin_stderr_write('exit join done.')
        self.reset_io()

    def stop_log(self):
        print("logrepl stopped log to file.")
        self.set_will_log(False)

    def start_log(self):
        self.set_will_log(True)
        print("logrepl start log to file.")

    @staticmethod
    def reset_io():
        sys.stdout.flush()
        sys.stdout = sys.__stdout__
        sys.stderr.flush()
        sys.stderr = sys.__stderr__
        sys.stdin = sys.__stdin__
        builtins.input = builtin_input  # useless for the running repl!!


@contextmanager
def log_handler(log_dir=None, prefix=None, err_acc_time=None, is_repl=False):
    hd = Handler.from_env(log_dir, prefix, err_acc_time, is_repl)
    hd.set_io()
    try:
        yield hd
    except Exception as e:
        e_str = traceback.format_exc()
        try:
            hd.check_dir_write(e_str)
        except Exception as e1:
            hd.add_err(e1)
        raise e
    finally:
        hd.exit()

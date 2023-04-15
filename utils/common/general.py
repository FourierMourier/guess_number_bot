from pathlib import Path
import time

import re
import yaml
import functools

from typing import Dict, Callable, Iterable, Any, Union


def load_yaml(filepath: Union[str, Path], **kwargs) -> Dict[str, Any]:
    with open(filepath, 'r', **kwargs) as file:
        config = yaml.safe_load(file)
    return config


def methods(instance):
    # Get class/instance methods
    return [f for f in dir(instance) if callable(getattr(instance, f)) and not f.startswith("__")]


def attributes(instance):
    # Get class/instance attributes
    return [a for a in dir(instance) if not callable(getattr(instance, a)) and not a.startswith("__")]


def clean_str(s):
    # Cleans a string by replacing special characters with underscore _
    return re.sub(pattern="[|@#!¡·$€%&()=?¿^*;:,¨´><+]", repl="_", string=s)


def colorstr(*input):
    # Colors a string https://en.wikipedia.org/wiki/ANSI_escape_code, i.e.  colorstr('blue', 'hello world')
    *args, string = input if len(input) > 1 else ('blue', 'bold', input[0])  # color arguments, string
    colors = {'black': '\033[30m',  # basic colors
              'red': '\033[31m',
              'green': '\033[32m',
              'yellow': '\033[33m',
              'blue': '\033[34m',
              'magenta': '\033[35m',
              'cyan': '\033[36m',
              'white': '\033[37m',
              'bright_black': '\033[90m',  # bright colors
              'bright_red': '\033[91m',
              'bright_green': '\033[92m',
              'bright_yellow': '\033[93m',
              'bright_blue': '\033[94m',
              'bright_magenta': '\033[95m',
              'bright_cyan': '\033[96m',
              'bright_white': '\033[97m',
              'end': '\033[0m',  # misc
              'bold': '\033[1m',
              'underline': '\033[4m'}
    return ''.join(colors[x] for x in args) + f'{string}' + colors['end']


# declare partial functions from colorstr:
exceptionColorstr = functools.partial(colorstr, 'bold', 'bright_red')
infoColorstr = functools.partial(colorstr, 'blue', 'bold')
warningColorstr = functools.partial(colorstr, 'bright_yellow', 'bold')


# ==== wrappers section ====
def time_counter(is_classmethod: bool = False, background_color: str = 'magenta') -> Callable:
    # see https://stackoverflow.com/a/68278527 for more examples with is_classmethod
    def outer_wrapper(func: Callable) -> Callable:

        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs) -> Any:
            s0: float = time.time()
            result = func(*args, **kwargs)
            s1: float = time.time()

            elapsed = s1 - s0

            seen_args: Iterable[Any]
            if is_classmethod is True:
                seen_args = args[1: ]
            else:
                seen_args = args

            stripped_msg: str = (f"function {func.__name__} took {elapsed:.3f} "
                                 f"seconds to execute with args, kwargs = {seen_args, kwargs}")
            # now make it colored:
            msg_body = colorstr('bright_cyan', 'bold', stripped_msg)
            # and now add background
            # from https://gist.github.com/vratiu/9780109
            # # Background
            # On_Black="\[\033[40m\]"       # Black
            # On_Red="\[\033[41m\]"         # Red
            # On_Green="\[\033[42m\]"       # Green
            # On_Yellow="\[\033[43m\]"      # Yellow
            # On_Blue="\[\033[44m\]"        # Blue
            # On_Purple="\[\033[45m\]"      # Purple
            # On_Cyan="\[\033[46m\]"        # Cyan
            # On_White="\[\033[47m\]"       # White

            msg_with_background: str
            # msg_with_background = "\033[47m" + msg_body
            if background_color == 'magenta':
                msg_with_background = "\033[45m" + msg_body
            elif background_color == 'white':
                msg_with_background = "\033[47m" + msg_body
            else:
                msg_with_background = "\033[45m" + msg_body

            print(msg_with_background)

            return result

        return inner_wrapper

    return outer_wrapper

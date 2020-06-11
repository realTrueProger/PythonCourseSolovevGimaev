import inspect
import contextlib
import io


def reflect(func):
    """
    Quine is a program which takes no input but outputs a copy of its own code.
    So function reflect is not a quine, because:
    1. It takes function as input.
    2. Its output depends on a given function rather than producing it by itself.

    Decorator that show certain stats and the source code on the wrapped function.
    :param func: Function to be wrapped
    """

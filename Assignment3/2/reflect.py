import inspect
import contextlib
import io


def write_stat(name, content):
    """
    Utility function to pretty-print multi-line information in the following form:
    [Name]: [line 1]
            [line 2]
            ...
    :param name: Name of the stat
    :param content: The potentially multi-line information to be printed
    """
    content = content.replace("\n", "\n\t")
    print(f"{name}:\t{content}")


def reflect(func):
    """
    Quine is a program which takes no input but outputs a copy of its own code.
    So function reflect is not a quine, because:
    1. It takes function as input.
    2. Its output depends on a given function rather than producing it by itself.

    Decorator that show certain stats and the source code on the wrapped function.
    :param func: Function to be wrapped
    """

    def wrapper(*args, **kwargs):
        stdout_redir = io.StringIO()
        with contextlib.redirect_stdout(stdout_redir):
            func(*args, **kwargs)

        output = stdout_redir.getvalue()
        source = inspect.getsource(func)

        sourcelines, _ = inspect.getsourcelines(func)

        # Output
        write_stat("Name", func.__name__)
        write_stat("Type", str(type(func)))
        write_stat("Sign", str(inspect.signature(func)))
        print()
        write_stat("Args", f"positional {args}\nkey=worded {kwargs}")
        print()
        write_stat("Doc", str(inspect.getdoc(func)))
        print()
        write_stat("Source", source)
        # For some reason, inspect.getsource adds a newline at the end of the function,
        #  thus no print() here
        write_stat("Output", output)
        print()

    return wrapper

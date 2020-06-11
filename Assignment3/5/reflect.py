import inspect
from io import StringIO
from contextlib import redirect_stdout
from functools import wraps

# @reflect
def reflect(func):
    '''Prints all kind of info about *func* using 'inspect' module'''
    @wraps(func)
    def print_func_info(*args, **kwargs):
        print_aligned('Name:', func.__name__)
        print_aligned('Type:', func.__class__)
        print_aligned('Sign:', inspect.signature(func))
        
        frame = inspect.currentframe()
        posargs = 'Positional ' + str(frame.f_locals['args'])
        keyargs = 'Key ' + str(frame.f_locals['kwargs'])
        print_aligned('Args:', posargs + '\n' + keyargs)
        
        source_code = inspect.getsource(func)
        acount = count_word_in_code(source_code)
        print_aligned('Complx:', acount)
        print_aligned('Doc:', func.__doc__)
        print_aligned('Source:', source_code)
        
        stream = StringIO()
        with redirect_stdout(stream):
            func(*args, **kwargs)
        output = stream.getvalue()
        print_aligned('Output:', output)
        print('\n')

    return print_func_info

def print_aligned(attribute, body):
    if body is not str:
        try:
            body = str(body)
        except:
            print("Can't make a string out of what you want to print")
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if i == 0:
            print('{:<10} {}'.format(attribute, line))
        else:
            print('{:<10} {}'.format('', line))

def count_word_in_code(code, word='wraps'):
    acount = 0
    docstring = False
    buf = StringIO(code)
    for line in buf:
        if docstring == False:
            until = line.find('#')
            if word in line[:until]:
                acount += 1
        if ('"""' in line or "'''" in line):
            if docstring == False:
                if line.count("'''") == 2 or line.count('"""') == 2:
                    pass
                else:
                    docstring = True
            else:
                docstring = False

    return str({word: acount})

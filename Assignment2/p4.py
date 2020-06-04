# Python 3.6.9

import dis
import sys
import marshal
import py_compile
import os

def main():
    args_length = len(sys.argv)

    if args_length == 1:
        print_help()
    else:
        action = sys.argv[1]

        if action == 'compile':
            flag = sys.argv[2]

            if flag == '-py':
                compile_file(sys.argv[3])
            elif flag == '-s':
                compile_src(sys.argv[3])
            else:
                print('wrong flag', flag)

        if action == 'print':
            flag = sys.argv[2]
        
            if flag == '-py':
                py(sys.argv[3])
            elif flag == '-pyc':
                pyc(sys.argv[3])
            elif flag == '-s':
                s(sys.argv[3])
            else:
                print('wrong flag', flag)
            
def print_help():
    print('usage: p4.py action [-flag value]')
    print('compile')
    print('\t-py file.py // compile file into bytecode and store it as file.pyc')
    print('\t-s "src" // compile src into bytecode and store it as out.pyc')
    print('print')
    print('\t-py src.py // produce human-readable bytecode from python file')
    print('\t-pyc src.pyc // produce human-readable bytecode from compiled .pyc file')
    print('\t-s "src" // produce human-readable bytecode from normal string')

def py(script_name):
    with open(script_name) as f:
                code = f.read()
                print_optcode(code, script_name)

def pyc(pyc):
    header_sizes = [
    (8,  (0, 9, 2)),  
    (12, (3, 6)),     
    (16, (3, 7))]

    header_size = next(s for s, v in reversed(header_sizes) if sys.version_info >= v)

    with open(pyc, "rb") as f:
        f.read(header_size)  
        code = marshal.load(f)  

    print_optcode(code, pyc)

def s(str):
    print_optcode(str, str)

def print_optcode(code, src):
    print('opcode for:', src)
    print('________________________________')       

    bytecode = dis.Bytecode(code)
    for instr in bytecode:
        print(instr.opname, instr.argval)

def compile_file(src):
    py_compile.compile(src, cfile=src.split('.')[0] + '.pyc')
    print('compiled')

def compile_src(src):
    with open('tmp','w') as f:
        f.write(src)
    py_compile.compile('tmp', cfile='out.pyc')
    os.remove('tmp')
    
main()
# Python 3.6.9

import dis
import sys
import marshal

def main():
    args_length = len(sys.argv)

    if args_length == 1:
        print_help()
    else:
        format = sys.argv[1]
        
        if format == '-py':
            py(sys.argv[2])
        elif format == '-pyc':
            pyc(sys.argv[2])
        elif format == '-s':
            print('-s')
            s(sys.argv[2])
        else:
            print('wrong format argument', format)
            
def print_help():
    print('To use run the script and provide format attribute and another .py script or a string as arguments')
    print('usage: p3.py -py src.py // produce human-readable bytecode from python file')
    print('usage: p3.py -pyc src.pyc // produce human-readable bytecode from compiled .pyc file')
    print('usage: p3.py -s "src" // produce human-readable bytecode from normal string')

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

main()
# Python 3.6.9

import dis
import sys

def main():
    args_length = len(sys.argv)

    if args_length == 1:
        print('To use run the script and provide another .py scripts as arguments')
        print('usage: p2.py [files]')
    else:
        script_names = sys.argv[1:]

        for script in script_names:
            with open(script) as f:
                code = f.read()
                print('opcode for:', script)
                print('________________________________')
                get_opcode(code)
                print('\n')

def get_opcode(script):
    '''print opcodes'''
    bytecode = dis.Bytecode(script)
    for instr in bytecode:
        print(instr.opname, instr.argval)


main()
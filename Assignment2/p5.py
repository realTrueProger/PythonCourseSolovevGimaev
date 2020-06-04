# !!!!!!!!!!!!!!!!!!!!
# python3.8 is a must for this to work 

import dis
import sys
import marshal
import py_compile
import os
import subprocess
import re
import io

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

        if action == 'compare':
            compare(sys.argv[2:])
            
def print_help():
    print('usage: p4.py action [-flag value]')
    print('compile')
    print('\t-py file.py // compile file into bytecode and store it as file.pyc')
    print('\t-s "src" // compile src into bytecode and store it as out.pyc')
    print('print')
    print('\t-py src.py // produce human-readable bytecode from python file')
    print('\t-pyc src.pyc // produce human-readable bytecode from compiled .pyc file')
    print('\t-s "src" // produce human-readable bytecode from normal string')
    print('compare -format src [-format src]+')
    print('\tproduce bytecode comparison for giving sources (supported formats -py, -pyc, -s)')

def py(script_name, action = None):
    '''read opcode from file'''
    if action == 'compare':
        return get_optcode_for_file(script_name)
    with open(script_name) as f:
        code = f.read()

        # need to change output too
        print_optcode(code, script_name)

def pyc(pyc, action = None):
    '''read opcode from .pyc'''
    header_sizes = [
    (8,  (0, 9, 2)),  
    (12, (3, 6)),     
    (16, (3, 7))]

    header_size = next(s for s, v in reversed(header_sizes) if sys.version_info >= v)

    with open(pyc, "rb") as f:
        f.read(header_size)  
        code = marshal.load(f)  

    if action == 'compare':
        return get_optcode(code, pyc)
    else:
        print_optcode(code, pyc)

def s(str, action = None):
    '''read opcode from string'''
    if action == 'compare':
        return get_optcode(str, str)
    else:
        print_optcode(str, str)

def print_optcode(code, src):
    '''print opcodes'''
    print('opcode for:', src)
    print('________________________________')       

    bytecode = dis.Bytecode(code)
    for instr in bytecode:
        print(instr.opname, instr.argval)

def get_optcode(code, src):
    '''prepare optcodes dict'''
    opcode = {}

    bytecode = dis.Bytecode(code)
    for instr in bytecode:
        opcode[instr.opname] = opcode.get(instr.opname, 0) + 1
    
    return opcode

def get_optcode_for_file(src):
    '''get optcode for file, special case'''
    # dis.dis() from script do not work recursevly and dont check inner functions, looks like the 
    # only way is to run it as subprocess and it requires python 3.8 minimum
    opcode = {}

    proc = subprocess.Popen(f'python3.8 -m dis {src}', shell=True, stdout=subprocess.PIPE)
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):  # or another encoding
        line = line.rstrip()
        opname = re.findall('[A-Z]*_[A-Z]*', line)
        if opname:
            on = opname[0]
            opcode[on] = opcode.get(on, 0) + 1

    return opcode

def compile_file(src):
    '''compile from file'''
    py_compile.compile(src, cfile=src.split('.')[0] + '.pyc')
    print('compiled')

def compile_src(src):
    '''compile from string'''
    with open('tmp','w') as f:
        f.write(src)
    py_compile.compile('tmp', cfile='out.pyc')
    os.remove('tmp')

def compare(argv):
    '''prepare compare table data'''
    flags = []
    srcs = []
    opcode_dic = {}
    opcodes_set = set()
    final_data = []

    # get flags and sources
    for i in range(len(argv)):
        if i % 2 == 0:
            flags.append(argv[i])
        else:
            srcs.append(argv[i])

    # get dic of opcodes for required src
    for i in range(len(flags)):
        if flags[i] == '-py':
            opcode_dic[srcs[i]] = py(srcs[i], 'compare')
        if flags[i] == '-pyc':
            opcode_dic[srcs[i]] = pyc(srcs[i], 'compare')
        if flags[i] == '-s':
            opcode_dic[srcs[i]] = s(srcs[i], 'compare')

    # get set of unique opcodes
    for opcodes in opcode_dic.values():
        for key in opcodes:
            opcodes_set.add(key)

    # prepare list of final data
    for key in opcodes_set:
        tmp = []
        for src in srcs:
            tmp.append(opcode_dic[src].get(key, 0))
        final_data.append((key, *tmp ))

    print_final_table(final_data, srcs)

def print_final_table(data, srcs):
    '''write table in file'''

    data.sort(key=lambda t: max(t[1:]), reverse=True)

    with open('output', 'w') as f:
        result = ''
        header = '{:15s}'.format('INSTRUCTION') + '|'

        for src in srcs:
            header = header + '{:15s}'.format(src) + '|'

        result = header + '\n'

        for row in data:
            row_print = ''
            for i in range(len(row)):
                row_print = row_print + '{:16s}'.format(str(row[i]))

            result = result + row_print + '\n'

        f.write(result)
    
main()
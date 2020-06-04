# Python 3.6.9

import sys
import subprocess
from datetime import datetime

def main():
    args_length = len(sys.argv)

    if args_length == 1:
        print('To use run the script and provide another .py scripts as arguments')
        print('usage: p1.py [files]')
    else:
        time_list = get_execution_time_table(sys.argv[1:])
        print_table(time_list)


def get_execution_time_table(scripts):
    '''create list with scripts and their execution time'''
    time_list = []

    for script in scripts:
        comand = 'python3 ' + script
        start_time = datetime.now()
        subprocess.run(comand, shell=True, stdout=subprocess.PIPE)
        end_time = datetime.now() - start_time
        time_list.append((script, end_time.total_seconds()))
    
    return time_list

def print_table(time_list):
    '''Print output table'''
    time_list.sort(key=lambda tup: tup[1])

    print('{:10}|{:5}|{:10}'.format('PROGRAM', 'RANK', 'TIME ELAPSED'))

    for i in range(len(time_list)):
        script_name = time_list[i][0].ljust(10)[:10]
        rank = str(i).ljust(5)[:5]
        time = (str(time_list[i][1]) + 's').ljust(10)[:10]

        print(script_name + ' ' + rank + ' ' + time)

main()
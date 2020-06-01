# We switched to subprocess from p3
# failed with p4..

import os
import subprocess, shlex
import re
from datetime import datetime

logfile = os.getcwd() + "/log.txt"

print('Please enter shell commands or "exit" to quit')

def reformatDir():
    '''reformat current dir to first letters version'''
    currentDir = os.getcwd()
    splitDir = currentDir.split('/')

    if splitDir[0] == "":
        splitDir = splitDir[1:]

    for i in range(len(splitDir)):
        if splitDir[i].startswith('.'):
            splitDir[i] = '.' + splitDir[i][1]
        else:
            splitDir[i] = splitDir[i][0]

    
    return "/".join(splitDir)

def createLog(process):
    '''logger function'''
    
    log = {
        'timestamp': '[' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']',
        'cmd': process.args[0],
        'args': process.args[1:] or ['[]'],
        'stdout': str(process.stdout.count('\n')),
        'pid': str(os.getpid()),
        'exitcode': str(process.returncode)
    }

    logline = log['timestamp'] + ' cmd: ' + log['cmd'] + ' args: ' + ', '.join(log['args']) + ' stdout: ' + log['stdout'] + ' pid: ' + log['pid'] + ' exitcode: ' + log['exitcode'] + '\n'
                
    with open(logfile, "a") as myfile:
        myfile.write(logline)

def logcd(path):
    '''log cd'''
    log = {
        'timestamp': '[' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']',
        'cmd': 'cd',
        'args': path,
        'stdout': '0',
        'pid': str(os.getpid()),
        'exitcode': '0'
    }

    logline = log['timestamp'] + ' cmd: ' + log['cmd'] + ' args: ' + log['args'] + ' stdout: ' + log['stdout'] + ' pid: ' + log['pid'] + ' exitcode: ' + log['exitcode'] + '\n'
 
    with open(logfile, "a") as myfile:
        myfile.write(logline)

# main loop

while True:
    mycommand = input('myshell ' + '[' + '/' + reformatDir() + ']: ')
    path = os.getcwd()

    if mycommand == 'exit': 
        print('Goodbye!')
        break
    if mycommand.startswith('cd'):
        path = re.findall("cd (.*)", mycommand)[0]
        logcd(path)
        os.chdir(path)
        continue

    args = shlex.split(mycommand)
    

    process = subprocess.run(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            cwd=path)

    createLog(process)

    print(process.stdout)



import os
import re
print('Please enter shell commands or "exit" to quit')

def cd(path):
    '''make cd command works'''
    x = path[0]
    os.chdir(x)

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


# main loop
while True:
    currentDir = reformatDir()

    mycommand = input('myshell ' + '[' + '/' + currentDir + ']: ')

    if mycommand == 'exit': 
        break
    if mycommand.startswith('cd'):
        path = re.findall("cd (.*)", mycommand)
        cd(path)
        continue

    os.system(mycommand)



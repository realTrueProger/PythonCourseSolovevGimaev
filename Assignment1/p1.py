import os
print('Please enter shell commands or "exit" to quit')

while True:
    mycommand = input('myshell: ')
    if mycommand == 'exit': break
    os.system(mycommand)
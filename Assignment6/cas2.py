# check if chars are digit
def is_digit(c):
    try:
        int(c)
        return True
    except ValueError:
        return  False

# check if the char is operation
def is_operation(c):
    operations = ['+', '-']
    if c in operations:
        return True
    else:
        return False 

def simplify(x):
    # we split everythhing in operations and operands
    operations = []
    operands = []
    for c in x.split():
        if is_digit(c):
            operands.append(int(c))
        elif is_operation(c):
            if not operands:
                print('err: invalid expression')
                return('error')
            else:
                operations.append(c)
        else:
            print('err: invalid expression')
            return('error')
    if len(operations) + 1 != len(operands): # check if number of operations relate to number of operands
        print('err: invalid expression')
        return('error')
    else:
        # compute the result
        result = operands[0] # we start with first operand
        for n, operation in enumerate(operations):
            if operation == '+':
                result +=  operands[n+1]
            else: 
                result -= operands[n+1]
        return str(result)

# split string by space 
def split_string(x):
    result = []
    a = ''
    length = len(x)
    for n, c in enumerate(x):
        if c != ' ':
            a += c 
        elif c == ' ':
            result.append(a)
            a = ''
        if len(x) == n+1:
            result.append(a)
    return result

count = 0
results = []
while True:
    keyboard_input = input()
    if keyboard_input == 'exit': # condition on exit
        break
    else:
        # handle brackets
        open_brackets = False
        # first we do every operation in brackets 
        # then expand them and compute everything else
        brackets_place = [] # list of list [start, end, result]
        for n, c in enumerate(split_string(keyboard_input)):
            if c.startswith("(") and not open_brackets:
                open_brackets = True
                brackets_place.append([n,0,0]) # bracket starts 
                inside_bracket = c[1:]
            elif open_brackets:
                if c.endswith(")"):
                    open_brackets = False
                    inside_bracket += ' ' + c[:-1]
                    brackets_place[-1][1] = n # bracket ends 
                    brackets_place[-1][2] = simplify(inside_bracket) # bracket result 
                else: 
                    inside_bracket += ' ' + c
            elif c.startswith("[") and not open_brackets:
                brackets_place.append([n,0,0]) # bracket starts 
                if c.endswith("]") and len(results) != 0:
                    brackets_place[-1][1] = n # bracket ends
                    brackets_place[-1][2] = results[int(c[1:-1])] # bracket result
                else: 
                    print('err: invalid expression')
                    break
            elif not open_brackets and c.endswith(")"):
                print('err: invalid expression')
                break
        # replace everything inside the brackets
        brackets_place.reverse()
        new_keyboard_input = split_string(keyboard_input)
        for bracket in brackets_place:
            del new_keyboard_input[bracket[0]:bracket[1]+1]
            new_keyboard_input.insert(bracket[0], bracket[2])
        # compute final result
        result = simplify(' '.join(new_keyboard_input))
        if result != 'error': 
            print(f'{count}: {result}')
            results.append(result)
            count += 1

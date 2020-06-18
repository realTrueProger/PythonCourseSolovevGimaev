import sys
import tokenize
import math

def printOperators(operators):
    N1 = 0
    print('[operators]')

    for key, value in operators.items():
        N1 += value
        print(f'{key}: {value}')

    print(f'N1: {N1}') 
    return N1

def printOperands(operands):
    N2 = 0
    print('[operands]')

    for key, value in operands.items():
        N2 += value
        print(f'{key}: {value}')

    print(f'N2: {N2}')   
    return N2  

def printMetrics(N1, N2, n1, n2):
    print('[program]') 
    vocabulary = n1 + n2
    length = N1 + N2
    calc_length = n1 * math.log2(n1) + n2 * math.log2(n2)
    volume = length * math.log2(vocabulary)
    difficulty = (n1/2) * (N2/n2)
    effort = difficulty * volume

    print('vocabulary:', vocabulary)
    print('length:', length)
    print('calc_length:', math.floor(calc_length))
    print('volume:', math.floor(volume))
    print('difficulty:', math.floor(difficulty))
    print('effort:', math.floor(effort))
   

def main():
    operators = {}
    operands = {}

    try:
        filename = sys.argv[1]

        try:
            with tokenize.open(filename) as f:
                tokens = tokenize.generate_tokens(f.readline)
                for token in tokens:
                    # exclude NL, NEWLINE, INDENT, DEDENT, ENDMDARKER token types 
                    if token.type not in [4, 61, 5, 6, 0]:
                        if (token.string == '(' or token.string == '[') and 'if' not in token.line and 'def' not in token.line:
                            operands['args'] = operands.get('args', 0) + 1
                        if token.type == 3 and '"""' in token.string:
                            operands['docstrings'] = operands.get('docstrings', 0) + 1
                            continue
                        if token.type == 60:
                            operands['inlinedocs'] = operands.get('inlinedocs', 0) + 1
                            continue
                        if token.type == 2 or token.type == 3:
                            operands['literal'] = operands.get('literal', 0) + 1
                            continue
                        if token.string in ['import', 'if', 'elif', 'else', 'try', 'for', 'with', 'return', 'def', 'except']:
                            operators[token.string] = operators.get(token.string, 0) + 1
                            continue
                        if token.string == '=':
                            operators['assignment'] = operators.get('assignment', 0) + 1
                            continue
                        if token.string in ['+', '-', '/', '*']:
                            operators['arithmetic'] = operators.get('arithmetic', 0) + 1
                            continue
                        if token.string in ['==', '!=', 'and', 'not']:
                            operators['logic'] = operators.get('logic', 0) + 1
                            continue
                        # get calls by '(' lines excluding lines with 'if' or 'def'
                        if token.string == '(' and 'if' not in token.line and 'def' not in token.line:
                            operators['calls'] = operators.get('calls', 0) + 1   

            operands['entities'] = operators.get('assignment', 0) + operators.get('def', 0)                              

            N1 = printOperators(operators)  
            print(' ')
            N2 = printOperands(operands)
            print(' ')

            n1 = 0
            n2 = 0

            for v in operators.values():
                if v != 0: n1 += 1

            for v in operands.values():
                if v != 0: n2 += 1    

            printMetrics(N1, N2, n1, n2) 
  
        except Exception as e:
            print(e)
            print('argument is not a correct python file. exit()')        
    
    except:
        print('filename not provided. exit()')

main()
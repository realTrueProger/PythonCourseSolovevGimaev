import sys
import tokenize

def printOperators(operators):
    N1 = 0
    print('[operators]')

    for key, value in operators.items():
        N1 += value
        print(f'{key}: {value}')

    print(f'N1: {N1}') 

def printOperands(operands):
    N2 = 0
    print('[operands]')

    for key, value in operands.items():
        N2 += value
        print(f'{key}: {value}')

    print(f'N2: {N2}')     

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

            printOperators(operators)  
            print(' ')
            printOperands(operands) 
  
        except Exception as e:
            print(e)
            print('argument is not a correct python file. exit()')        
    
    except:
        print('filename not provided. exit()')

main()
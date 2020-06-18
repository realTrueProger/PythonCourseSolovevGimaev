import sys
import tokenize

def printResults(result):
    N1 = 0
    print('[operators]')

    for key, value in result.items():
        N1 += value
        print(f'{key}: {value}')

    print(f'N1: {N1}') 

def main():
    result = {}

    try:
        filename = sys.argv[1]

        try:
            with tokenize.open(filename) as f:
                tokens = tokenize.generate_tokens(f.readline)
                for token in tokens:
                    # exclude NL, NEWLINE, INDENT, DEDENT, ENDMDARKER token types 
                    if token.type not in [4, 61, 5, 6, 0]:
                        if token.string in ['import', 'if', 'elif', 'else', 'try', 'for', 'with', 'return', 'def', 'except']:
                            result[token.string] = result.get(token.string, 0) + 1
                            continue
                        if token.string == '=':
                            result['assignment'] = result.get('assignment', 0) + 1
                            continue
                        if token.string in ['+', '-', '/', '*']:
                            result['arithmetic'] = result.get('arithmetic', 0) + 1
                            continue
                        if token.string in ['==', '!=', 'and', 'not']:
                            result['logic'] = result.get('logic', 0) + 1
                            continue
                        # get calls by '(' lines excluding lines with 'if' or 'def'
                        if token.string == '(' and 'if' not in token.line and 'def' not in token.line:
                            result['calls'] = result.get('calls', 0) + 1                 

            printResults(result)   
  
        except:
            print('argument is not a correct python file. exit()')        
    
    except:
        print('filename not provided. exit()')

main()
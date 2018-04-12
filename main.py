import sys
import src.code_parser as code_parser
from src.conf import conf

from src.parser import Parser

import src.ast as ast
from src.ast_eval import eval


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: [filename]')
        sys.exit(1)

    path = sys.argv[1]

    
    lexer = code_parser.Lexer(code_parser.FileStream(path), conf)
    while True:
        tok = lexer.get_token()
        print(tok)
        if tok.type == code_parser.TOKEN_EOF:
            break
    

    '''
    lexer = code_parser.Lexer(code_parser.FileStream(path), conf)
    parser = Parser(lexer)

    x = parser.build_ast()
    ast.print_ast(x)

    eval(x)
    '''

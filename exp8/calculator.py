from lexer import lexer
from parser import parser

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    lexer.input(s)
    result = parser.parse(s)
    print(result)
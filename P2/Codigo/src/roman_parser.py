import ply.yacc as yacc
from src.roman_lexer import tokens

# Gramática

def p_romanNumber(p):
    'romanNumber : thousand hundred ten digit'
    p[0] = p[1] + p[2] + p[3] + p[4]

def p_thousand(p):
    '''thousand : M thousand
                | lambda'''
    if len(p) == 3:
        p[0] = 1000 + p[2]
    else:
        p[0] = 0

def p_hundred(p):
    '''hundred : small_hundred
               | C D
               | C M
               | D small_hundred'''
    if len(p) == 2:
        if p[1] == 'C D':
            p[0] = 400
        elif p[1] == 'C M':
            p[0] = 900
        else:
            p[0] = p[1]
    elif len(p) == 3:
        p[0] = 500 + p[2]

def p_small_hundred(p):
    '''small_hundred : C small_hundred
                     | lambda'''
    if len(p) == 3:
        p[0] = 100 + p[2]
    else:
        p[0] = 0

def p_ten(p):
    '''ten : small_ten
            | X L
            | X C
            | L small_ten'''
    if len(p) == 2:
        if p[1] == 'X L':
            p[0] = 40
        elif p[1] == 'X C':
            p[0] = 90
        else:
            p[0] = 0
    elif len(p) == 3:
        p[0] = 50 + p[2]

def p_small_ten(p):
    '''small_ten : X small_ten
                 | lambda'''
    if len(p) == 3:
        p[0] = 10 + p[2]
    else:
        p[0] = 0

def p_digit(p):
    '''digit : small_digit
              | I V
              | I X
              | V small_digit'''
    if len(p) == 2:
        if p[1] == 'I V':
            p[0] = 4
        elif p[1] == 'I X':
            p[0] = 9
        else:
            p[0] = 0
    elif len(p) == 3:
        p[0] = 5 + p[2]

def p_small_digit(p):
    '''small_digit : I small_digit
                   | lambda'''
    if len(p) == 3:
        p[0] = 1 + p[2]
    else:
        p[0] = 0

def p_empty(p):
    'lambda :'
    p[0] = 0

# Manejo de errores sintácticos
def p_error(p):
    print("Error de sintaxis en '%s'" % p.value if p else "EOF")

# Construir el parser
parser = yacc.yacc()

if __name__ == "__main__":
    while True:
        try:
            s = input("Ingrese un número romano: ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"El valor numérico es: {result}")

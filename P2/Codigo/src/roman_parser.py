import ply.yacc as yacc
from src.roman_lexer import tokens

# Gramática

def p_romanNumber(p):
    'romanNumber : thousand hundred ten digit'
    p[0] = {"val":p[1]["val"] + p[2]["val"] + p[3]["val"] + p[4]["val"]}
    # p[0] = {"val":p[1]["val"] + p[2]["val"] + p[3]["val"] + p[4]["val"], "valid" : p[1]["valid"] and p[2]["valid"] and p[3]["valid"] and p[4]["valid"]}

def p_thousand(p):
    '''thousand : M thousand
                | lambda'''
    if len(p) == 3:
        p[0] = {"val": 1000 + p[2]["val"]}
        # p[0]["valid"] = True and p[2]["valid"]

    else:
        p[0] = {"val": 0}

def p_hundred(p):
    '''hundred : small_hundred
               | C D
               | C M
               | D small_hundred'''

    if len(p) == 2:
            p[0] = {"val": p[1]["val"]}

    elif len(p) == 3:
        if p[1] == 'C' and p[2] == 'D':
            p[0] = {"val": 400}
        elif p[1] == 'C' and p[2] == 'M':
            p[0] = {"val": 900}
        else:
            p[0] = {"val": 500 + p[2]["val"]}

def p_small_hundred(p):
    '''small_hundred : C small_hundred
                     | lambda'''
    if len(p) == 3:
        p[0] =  {"val": 100 + p[2]["val"]}
    else:
        p[0] = {"val": 0}

def p_ten(p):
    '''ten : small_ten
            | X L
            | X C
            | L small_ten'''
    if len(p) == 2:
        p[0] =  {"val": p[1]["val"]}
    elif len(p) == 3:
        if p[1] == 'X' and p[2] == 'L':
            p[0] = {"val": 40}
        elif p[1] == 'X' and p[2] == 'C':
            p[0] = {"val": 90}
        else:
            p[0] = {"val": 50 + p[2]["val"]}

def p_small_ten(p):
    '''small_ten : X small_ten
                 | lambda'''
    if len(p) == 3:
        p[0] =  {"val": 10 + p[2]["val"]}
    else:
        p[0] = {"val": 0}

def p_digit(p):
    '''digit : small_digit
              | I V
              | I X
              | V small_digit'''
    if len(p) == 2:
        p[0] = {"val": p[1]["val"]}
    elif len(p) == 3:
        if p[1] == 'I' and p[2] == 'V':
            p[0] = {"val": 4}
        elif p[1] == 'I' and p[2] == 'X':
            p[0] = {"val": 9}
        else:
            p[0] =  {"val": 5 + p[2]["val"]}

def p_small_digit(p):
    '''small_digit : I small_digit
                   | lambda'''
    if len(p) == 3:
        p[0] =  {"val": 1 + p[2]["val"]}
    else:
        p[0] = {"val": 0}

def p_empty(p):
    'lambda :'
    p[0] = {"val": 0}

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
        print(f"El valor numérico es: {result["val"]}")

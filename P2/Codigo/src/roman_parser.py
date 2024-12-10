import ply.yacc as yacc
from src.roman_lexer import tokens

# Gramática
synt_error = False

def p_romanNumber(p):
    'romanNumber : hundred ten digit'
    # p[0] = {"val":p[1]["val"] + p[2]["val"] + p[3]["val"]}
    global synt_error
    p[0] = {"val":p[1]["val"] + p[2]["val"] + p[3]["val"], "valid" : True}
    if synt_error:
        p[0] = {"val":-1, "valid" : False}
        synt_error = False
    

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

def p_small_hundred(p): #aniadir no mas de 3
    '''small_hundred : C small_hundred
                     | lambda'''
    global synt_error
    if len(p) == 3:
        p[0] =  {"val": 100 + p[2]["val"]}
        if p[0]["val"] > 300:
            synt_error = True

    else:
        p[0] = {"val": 0, }

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

def p_small_ten(p): #aniadir no mas de 3
    '''small_ten : X small_ten
                 | lambda'''
    global synt_error
    if len(p) == 3:
        p[0] =  {"val": 10 + p[2]["val"]}
        if p[0]["val"] > 30:
            synt_error = True
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

def p_small_digit(p): #aniadir no mas de 3
    '''small_digit : I small_digit
                   | lambda'''
    global synt_error
    if len(p) == 3:
        p[0] =  {"val": 1 + p[2]["val"]}
        if p[0]["val"] > 3:
            synt_error = True
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

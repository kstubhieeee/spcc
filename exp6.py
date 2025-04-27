from collections import namedtuple

# Define a simple struct-like object
Operator = namedtuple('Operator', ['pos', 'op'])

# Globals
i = 1
j = 0
no = 0
tmpch = 90  # ASCII 'Z'
str_expr = ""
left = ""
right = ""
k = []

def findopr():
    global k
    operators = [':', '/', '*', '+', '-']
    for op in operators:
        for idx, ch in enumerate(str_expr):
            if ch == op:
                k.append(Operator(pos=idx, op=op))

def explore():
    global i, tmpch, no, left, right, str_expr
    i = 1
    while i < len(k):
        fleft(k[i].pos)
        fright(k[i].pos)
        str_expr_list = list(str_expr)
        str_expr_list[k[i].pos] = chr(tmpch)
        str_expr = ''.join(str_expr_list)
        
        print(f"\t{chr(tmpch)} := {left}{k[i].op}{right}\t\t", end='')
        for ch in str_expr:
            if ch != '$':
                print(ch, end='')
        print()
        
        tmpch -= 1
        i += 1

    fright(-1)
    if no == 0:
        fleft(len(str_expr))
        print(f"\t{right} := {left}")
    if i > 0:
        print(f"\t{right} := {str_expr[k[i-1].pos]}")

def fleft(x):
    global left, str_expr
    w = []
    flag = False
    x -= 1
    str_expr_list = list(str_expr)
    while x != -1 and str_expr_list[x] not in ['+', '*', '=', '\0', '-', '/', ':']:
        if str_expr_list[x] != '$' and not flag:
            w.append(str_expr_list[x])
            str_expr_list[x] = '$'
            flag = True
        x -= 1
    left = ''.join(reversed(w))
    str_expr = ''.join(str_expr_list)

def fright(x):
    global right, str_expr
    w = []
    flag = False
    x += 1
    str_expr_list = list(str_expr)
    while x < len(str_expr_list) and str_expr_list[x] not in ['+', '*', '\0', '=', ':', '-', '/']:
        if str_expr_list[x] != '$' and not flag:
            w.append(str_expr_list[x])
            str_expr_list[x] = '$'
            flag = True
        x += 1
    right = ''.join(w)
    str_expr = ''.join(str_expr_list)

def main():
    global str_expr
    print("\t\tINTERMEDIATE CODE GENERATION\n")
    str_expr = input("Enter the Expression: ")
    print("The intermediate code:\t\tExpression")
    findopr()
    explore()

if __name__ == "__main__":
    main()

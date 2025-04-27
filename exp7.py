import re
from dataclasses import dataclass

@dataclass
class Quadruple:
    op: str = ''
    arg1: str = ''
    arg2: str = ''
    result: str = ''

quad = []
tuple_list = []

def codegen(op, t):
    print(f"MOV R0, {quad[t].arg1}")
    print(f"{op} R0, {quad[t].arg2}")
    print(f"MOV {quad[t].result}, R0")

def assignment(t):
    print(f"MOV R0, {quad[t].arg1}")
    print(f"MOV {quad[t].result}, R0")

def uminus(t):
    print("MOV R0, 0")
    print(f"SUB R0, {quad[t].arg1}")
    print(f"MOV {quad[t].result}, R0")

def explore():
    for i, expr in enumerate(tuple_list):
        q = Quadruple()
        
        # Match patterns like: a=b+c or a=-b
        match = re.match(r'(\w+)=(.+)', expr)
        if not match:
            continue

        q.result, rhs = match.groups()
        
        # Check if rhs is simple assignment or an operation
        op_match = re.match(r'(-?[\w\d]+)([\+\-\*/])?([\w\d]*)', rhs)

        if op_match:
            arg1, op, arg2 = op_match.groups()
            if op:
                q.op = op
                q.arg1 = arg1
                q.arg2 = arg2
            else:
                if arg1.startswith('-'):
                    q.op = '-'
                    q.arg1 = arg1[1:]
                    q.arg2 = ''
                else:
                    q.op = '='
                    q.arg1 = arg1
                    q.arg2 = ''

        quad.append(q)

def main():
    global tuple_list
    m = int(input("Enter the number of statements: "))
    print("Enter the statements:")
    for _ in range(m):
        statement = input().strip()
        tuple_list.append(statement)

    explore()

    print("\n\nCode generated:")
    for i, q in enumerate(quad):
        if q.op == '+':
            codegen("ADD", i)
        elif q.op == '=':
            assignment(i)
        elif q.op == '-':
            if q.arg2 == '':
                uminus(i)
            else:
                codegen("SUB", i)
        elif q.op == '*':
            codegen("MUL", i)
        elif q.op == '/':
            codegen("DIV", i)

if __name__ == "__main__":
    main()

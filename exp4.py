productions = {
    'E': ["T E'"],
    "E'": ["+ T E'", 'ε'],
    'T': ["F T'"],
    "T'": ["* F T'", 'ε'],
    'F': ["( E )", 'i']
}

def compute_first(productions):
    FIRST = {nt: set() for nt in productions}
    def first(symbol):
        if symbol not in productions: return {symbol}
        if FIRST[symbol]: return FIRST[symbol]
        result = set()
        for rule in productions[symbol]:
            for sym in rule.split():
                res = first(sym)
                result.update(res - {'ε'})
                if 'ε' not in res: break
            else:
                result.add('ε')
        FIRST[symbol] = result
        return result
    for nt in productions: first(nt)
    return FIRST

def compute_follow(productions, FIRST):
    FOLLOW = {nt: set() for nt in productions}
    FOLLOW[next(iter(productions))].add('$')
    def follow(nt):
        for lhs, rules in productions.items():
            for rule in rules:
                symbols = rule.split()
                for i, symbol in enumerate(symbols):
                    if symbol == nt:
                        if i + 1 < len(symbols):
                            next_sym = symbols[i + 1]
                            if next_sym in productions:
                                FOLLOW[nt].update(FIRST[next_sym] - {'ε'})
                                if 'ε' in FIRST[next_sym]:
                                    FOLLOW[nt].update(FOLLOW[lhs])
                            else:
                                FOLLOW[nt].add(next_sym)
                        else:
                            FOLLOW[nt].update(FOLLOW[lhs])
    for _ in range(len(productions)):
        for nt in productions: follow(nt)
    return FOLLOW

def construct_parsing_table(productions, FIRST, FOLLOW):
    table = {}
    for lhs, rules in productions.items():
        for rule in rules:
            rule_first = set()
            for symbol in rule.split():
                if symbol in FIRST: rule_first.update(FIRST[symbol] - {'ε'})
                else: rule_first.add(symbol)
                if 'ε' not in FIRST.get(symbol, {}): break
            else:
                rule_first.add('ε')
            for terminal in rule_first:
                if terminal != 'ε':
                    table[(lhs, terminal)] = rule
            if 'ε' in rule_first:
                for terminal in FOLLOW[lhs]:
                    table[(lhs, terminal)] = rule
    return table

def display_sets(FIRST, FOLLOW):
    print("\nFIRST Sets:")
    for nt, s in FIRST.items():
        print(f"FIRST({nt}) = {s}")
    print("\nFOLLOW Sets:")
    for nt, s in FOLLOW.items():
        print(f"FOLLOW({nt}) = {s}")

def display_parsing_table(table, productions):
    non_terminals = list(productions.keys())
    terminals = sorted(set(
        symbol for rules in productions.values()
        for rule in rules for symbol in rule.split() if symbol not in productions
    )) + ['$']
    print("\nParsing Table:")
    print(f"{'':<10}", end="")
    for t in terminals:
        print(f"{t:<10}", end="")
    print("\n" + "-" * (len(terminals) * 10))
    for nt in non_terminals:
        print(f"{nt:<10}", end="")
        for t in terminals:
            rule = table.get((nt, t), '')
            print(f"{rule:<10}", end="")
        print()

def parse_input(input_string, parsing_table):
    stack = ['$', 'E']
    tokens = input_string.split() + ['$']
    index = 0
    print("\nParsing Steps:")
    print(f"{'Stack':<20} {'Input':<20} {'Action'}")
    print("-" * 60)

    while stack:
        top = stack[-1]
        current = tokens[index]
        print(f"{' '.join(stack):<20} {' '.join(tokens[index:]):<20}", end=' ')
        if top == current:
            stack.pop()
            index += 1
            print("Pop")
        elif top in productions:
            rule = parsing_table.get((top, current))
            if rule:
                stack.pop()
                for sym in reversed(rule.split()):
                    if sym != 'ε': stack.append(sym)
                print(f"Apply {top} -> {rule}")
            else:
                print("Error: No rule")
                return False
        else:
            print("Error: Mismatch")
            return False

    if index == len(tokens):
        print("Input Accepted!")
        return True
    else:
        print("Error: Input not fully consumed")
        return False

FIRST = compute_first(productions)
FOLLOW = compute_follow(productions, FIRST)
parsing_table = construct_parsing_table(productions, FIRST, FOLLOW)

display_sets(FIRST, FOLLOW)
display_parsing_table(parsing_table, productions)

input_string = "i + i"
parse_input(input_string, parsing_table)

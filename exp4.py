# Grammar rules
productions = {
    'E': ["T E'"],
    "E'": ["+ T E'", 'ε'],
    'T': ["F T'"],
    "T'": ["* F T'", 'ε'],
    'F': ["( E )", 'i']
}

# Function to compute FIRST sets
def compute_first(productions):
    FIRST = {nt: set() for nt in productions}

    def first(symbol):
        if symbol not in productions:  # Terminal
            return {symbol}
        if FIRST[symbol]:  # Already computed
            return FIRST[symbol]
        result = set()
        for rule in productions[symbol]:
            for sub_symbol in rule.split():
                sub_first = first(sub_symbol)
                result.update(sub_first - {'ε'})
                if 'ε' not in sub_first:
                    break
            else:
                result.add('ε')
        FIRST[symbol] = result
        return result

    for nt in productions:
        first(nt)
    return FIRST

# Function to compute FOLLOW sets
def compute_follow(productions, FIRST):
    FOLLOW = {nt: set() for nt in productions}
    start_symbol = next(iter(productions))
    FOLLOW[start_symbol].add('$')  # Start symbol has '$' in FOLLOW

    def follow(nt):
        for lhs, rules in productions.items():
            for rule in rules:
                symbols = rule.split()
                for i, symbol in enumerate(symbols):
                    if symbol == nt:
                        if i + 1 < len(symbols):  # If there's a symbol after nt
                            next_symbol = symbols[i + 1]
                            if next_symbol in productions:  # Non-terminal
                                FOLLOW[nt].update(FIRST[next_symbol] - {'ε'})
                                if 'ε' in FIRST[next_symbol]:
                                    FOLLOW[nt].update(FOLLOW[lhs])
                            else:  # Terminal
                                FOLLOW[nt].add(next_symbol)
                        else:  # nt is at the end
                            FOLLOW[nt].update(FOLLOW[lhs])

    for _ in range(len(productions)):  # Iterate multiple times to propagate
        for nt in productions:
            follow(nt)
    return FOLLOW

FIRST = compute_first(productions)
FOLLOW = compute_follow(productions, FIRST)

# Predictive Parsing Table
def construct_parsing_table(productions, FIRST, FOLLOW):
    parsing_table = {}
    for lhs, rules in productions.items():
        for rule in rules:
            rule_first = set()
            for symbol in rule.split():
                if symbol in productions:
                    rule_first.update(FIRST[symbol] - {'ε'})
                else:
                    rule_first.add(symbol)
                if 'ε' not in FIRST.get(symbol, {}):
                    break
            else:
                rule_first.add('ε')

            for terminal in rule_first:
                if terminal != 'ε':
                    parsing_table[(lhs, terminal)] = rule
            if 'ε' in rule_first:
                for terminal in FOLLOW[lhs]:
                    parsing_table[(lhs, terminal)] = rule
    return parsing_table

parsing_table = construct_parsing_table(productions, FIRST, FOLLOW)

# Display FIRST sets
print("\nFIRST Sets:")
for nt, first_set in FIRST.items():
    print(f"FIRST({nt}) = {first_set}")

# Display FOLLOW sets
print("\nFOLLOW Sets:")
for nt, follow_set in FOLLOW.items():
    print(f"FOLLOW({nt}) = {follow_set}")

# Display Predictive Parsing Table
print("\nPredictive Parsing Table:")
non_terminals = list(productions.keys())
terminals = sorted(set(
    symbol for rules in productions.values()
    for rule in rules for symbol in rule.split() if symbol not in productions
))
terminals.append('$')

# Print table header
print(f"{'':<10}", end="")
for t in terminals:
    print(f"{t:<10}", end="")
print("\n" + "-" * (len(terminals) * 10))

# Print table rows
for nt in non_terminals:
    print(f"{nt:<10}", end="")
    for t in terminals:
        rule = parsing_table.get((nt, t), "")
        print(f"{rule:<10}", end="")
    print()

# Function to parse input
def parse_input(input_string, parsing_table):
    stack = ['$', 'E']  # Start with the end marker and the start symbol
    input_tokens = input_string.split() + ['$']  # Tokenize input and add end marker
    index = 0  # Pointer for input tokens

    print("\nParsing Steps:")
    print(f"{'Stack':<30} {'Input':<30} {'Action'}")
    print("-" * 80)

    while stack:
        stack_top = stack[-1]
        current_input = input_tokens[index]

        print(f"{' '.join(stack):<30} {' '.join(input_tokens[index:]):<30}", end=' ')

        if stack_top == current_input:  # Match terminal
            stack.pop()
            index += 1
            print("Pop")
            if current_input == '$':
                print("Input Accepted Successfully!")
                return True
        elif stack_top in productions:  # Non-terminal
            rule = parsing_table.get((stack_top, current_input))
            if rule:
                stack.pop()
                # Push rule symbols in reverse order (except ε)
                for symbol in reversed(rule.split()):
                    if symbol != 'ε':
                        stack.append(symbol)
                print(f"Apply {stack_top} -> {rule}")
            else:
                print("Error: No rule found for", (stack_top, current_input))
                return False
        else:  # Stack top is terminal but not matching
            print("Error: Unexpected symbol", current_input)
            return False

    if index == len(input_tokens):
        print("Parsing completed!")
        return True
    else:
        print("Error: Input not fully consumed")
        return False

# Example input to parse
input_string = "i + i"  # Change this to test different inputs
parse_input(input_string, parsing_table)

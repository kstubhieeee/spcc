import copy

def grammarAugmentation(rules, nonterm_userdef, start_symbol):
    newRules = []
    newChar = start_symbol + "'"
    while newChar in nonterm_userdef:
        newChar += "'"
    newRules.append([newChar, ['.', start_symbol]])
    for rule in rules:
        k = rule.split("->")
        lhs = k[0].strip()
        rhs = k[1].strip()
        multirhs = rhs.split('|')
        for rhs1 in multirhs:
            rhs1 = rhs1.strip().split()
            rhs1.insert(0, '.')
            newRules.append([lhs, rhs1])
    return newRules

def findClosure(input_state, dotSymbol):
    global start_symbol, separatedRulesList, statesDict
    closureSet = []
    if dotSymbol == start_symbol:
        for rule in separatedRulesList:
            if rule[0] == dotSymbol:
                closureSet.append(rule)
    else:
        closureSet = input_state
    prevLen = -1
    while prevLen != len(closureSet):
        prevLen = len(closureSet)
        tempClosureSet = []
        for rule in closureSet:
            indexOfDot = rule[1].index('.')
            if rule[1][-1] != '.':
                dotPointsHere = rule[1][indexOfDot + 1]
                for in_rule in separatedRulesList:
                    if dotPointsHere == in_rule[0] and in_rule not in tempClosureSet:
                        tempClosureSet.append(in_rule)
        for rule in tempClosureSet:
            if rule not in closureSet:
                closureSet.append(rule)
    return closureSet

def compute_GOTO(state):
    global statesDict, stateCount
    generateStatesFor = []
    for rule in statesDict[state]:
        if rule[1][-1] != '.':
            indexOfDot = rule[1].index('.')
            dotPointsHere = rule[1][indexOfDot + 1]
            if dotPointsHere not in generateStatesFor:
                generateStatesFor.append(dotPointsHere)
    if len(generateStatesFor) != 0:
        for symbol in generateStatesFor:
            GOTO(state, symbol)

def GOTO(state, charNextToDot):
    global statesDict, stateCount, stateMap
    newState = []
    for rule in statesDict[state]:
        indexOfDot = rule[1].index('.')
        if rule[1][-1] != '.' and rule[1][indexOfDot + 1] == charNextToDot:
            shiftedRule = copy.deepcopy(rule)
            shiftedRule[1][indexOfDot] = shiftedRule[1][indexOfDot + 1]
            shiftedRule[1][indexOfDot + 1] = '.'
            newState.append(shiftedRule)
    addClosureRules = []
    for rule in newState:
        indexDot = rule[1].index('.')
        if rule[1][-1] != '.':
            closureRes = findClosure(newState, rule[1][indexDot + 1])
            for rule in closureRes:
                if rule not in addClosureRules and rule not in newState:
                    addClosureRules.append(rule)
    for rule in addClosureRules:
        newState.append(rule)
    stateExists = -1
    for state_num in statesDict:
        if statesDict[state_num] == newState:
            stateExists = state_num
            break
    if stateExists == -1:
        stateCount += 1
        statesDict[stateCount] = newState
        stateMap[(state, charNextToDot)] = stateCount
    else:
        stateMap[(state, charNextToDot)] = stateExists

def generateStates(statesDict):
    prev_len = -1
    called_GOTO_on = []
    while len(statesDict) != prev_len:
        prev_len = len(statesDict)
        keys = list(statesDict.keys())
        for key in keys:
            if key not in called_GOTO_on:
                called_GOTO_on.append(key)
                compute_GOTO(key)

def createParseTable(statesDict, stateMap, T, NT):
    global separatedRulesList, diction
    rows = list(statesDict.keys())
    cols = T+['$']+NT
    Table = [['' for _ in range(len(cols))] for _ in range(len(rows))]
    for entry in stateMap:
        state, symbol = entry
        a, b = rows.index(state), cols.index(symbol)
        if symbol in NT:
            Table[a][b] += f"{stateMap[entry]} "
        elif symbol in T:
            Table[a][b] += f"S{stateMap[entry]} "
    print("\nSLR(1) parsing table:\n")
    frmt = "{:>8}" * len(cols)
    print(" ", frmt.format(*cols), "\n")
    for j, y in enumerate(Table):
        frmt1 = "{:>8}" * len(y)
        print(f"I{j} {frmt1.format(*y)}")

def printResult(rules):
    for rule in rules:
        print(f"{rule[0]} -> {' '.join(rule[1])}")

rules = ["S -> S + M | M | n", "M -> M * P | P | a", "P -> ( S ) | id | b"]
nonterm_userdef = ['S', 'M', 'P']
term_userdef = ['id', '+', '*', '(', ')', 'a', 'b', 'n']
start_symbol = 'S'
print("\nOriginal grammar input:\n")
for y in rules:
    print(y)
separatedRulesList = grammarAugmentation(rules, nonterm_userdef, start_symbol)
print("\nGrammar after Augmentation: \n")
printResult(separatedRulesList)
start_symbol = separatedRulesList[0][0]
print("\nCalculated closure: I0\n")
I0 = findClosure(0, start_symbol)
printResult(I0)
statesDict = {0: I0}
stateMap = {}
stateCount = 0
generateStates(statesDict)
print("\nStates Generated: \n")
for st in statesDict:
    print(f"State = I{st}")
    printResult(statesDict[st])
    print()
print("\nGOTO Computation:\n")
for entry in stateMap:
    print(f"GOTO(I{entry[0]}, {entry[1]}) = I{stateMap[entry]}")
diction = {}
createParseTable(statesDict, stateMap, term_userdef, nonterm_userdef)
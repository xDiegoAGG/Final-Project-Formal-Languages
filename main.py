import functions as f
from utilities import countElements, summarizeProductions, repeatFunction, enumerateProductions

cases = input()  # Variable used to store the number of cases the user wants.
for i in range(int(cases)):  # Loop for the number of cases.
    first = {}
    follow = {}
    nonTerminals = []  # Nonterminals list.
    nonTerminalsList = []  # Derivations of each nonterminal
    nonTerminalsNumber = int(input())
    summarizeProductions(nonTerminalsNumber, nonTerminals, nonTerminalsList)
    details = [nonTerminals, nonTerminalsList, first, follow]
    f.initialFirst(details)
    f.initialFollow(details)
    repeatFunction(details, f.getFirst, first)
    repeatFunction(details, f.getFollow, follow)
    for j in range(len(nonTerminals)):
        print(f"First({nonTerminals[j]}) = {'{' + ','.join(first[nonTerminals[j]]) + '}'}")
    for j in range(len(nonTerminals)):
        print(f"Follow({nonTerminals[j]}) = {'{' + ','.join(follow[nonTerminals[j]]) + '}'}")
    if int(cases) > 1 and i != int(cases) - 1:
        print()
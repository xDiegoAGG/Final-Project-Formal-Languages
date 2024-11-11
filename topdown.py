import functions as f
from utilities import countElements, summarizeProductions, repeatFunction

cases = input()  # Variable used to store the number of cases the user wants.
for i in range(int(cases)):  # Loop for the number of cases.
    first = {}
    follow = {}
    nonTerminals = []  # Nonterminals list.
    nonTerminalsList = []  # Derivations of each nonterminal
    stringInput = []
    nonTerminalsNumber = int(input())
    inputStrings = int(input())
    summarizeProductions(nonTerminalsNumber, nonTerminals, nonTerminalsList)
    for j in range(inputStrings):
        stringInput.append(input())
    details = [nonTerminals, nonTerminalsList, first, follow]
    f.initialFirst(details)
    f.initialFollow(details)
    repeatFunction(details, f.getFirst, first)
    repeatFunction(details, f.getFollow, follow)
    table = f.predictiveTable(details)
    if table is None:
        print("Sorry bro, ur grammar is not LL(1)")
    else:
        for j in range(inputStrings):
            print(f.predictiveParsing(table, stringInput[j], details))

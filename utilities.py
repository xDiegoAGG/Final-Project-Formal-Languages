def countElements(dictionary):
    cont = 0
    for key, values in dictionary.items():
        cont += len(set(values))
    return cont

def makePairs(productionsList):
    pairs = []
    for productions in productionsList:
        pairs.append([])
        for i in range(len(productions) -1):
            for j in range(i+1, len(productions)):
                pairs[-1].append([productions[i], productions[j]])
    return pairs

def summarizeProductions(nonTerminalsNumber, nonTerminals, nonTerminalsList):
    for j in range(nonTerminalsNumber):  # This for loop allows the user to enter the productions of the grammar.
        production = input().split(" ")  # Captures the input
        nonTerminals.append(production[0])  # Stores the nonterminal symbol in nonterminals list.
        nonTerminalsList.append(production[1:])  # Stores the productions in nonterminals_list list.

def repeatFunction(details, function, countableSet):
    counter = 0
    nonTerminals = details[0]
    while True:
        for nonTerminal in nonTerminals:
            function(nonTerminal, details)
        auxVar = countElements(countableSet)
        if counter == auxVar:
            break
        counter = auxVar

def derivationPath(derivationList, left = True):
    path = "S"
    stringAux = "S"
    for element in derivationList:
        nonterminal = element[0]
        body = element[element.index(">") + 1:]
        if body == "e":
            body = ""
        if left:
            index = stringAux.index(nonterminal)
        else:
            index = len(stringAux) - stringAux[::-1].index(nonterminal) - 1
        stringAux = stringAux[:index] + body + stringAux[index + 1:]
        path += "->" + stringAux
    return path
def stringPreparation(string):
    stringAux = ""
    for char in string:
        if char != " " and char != "e":
            stringAux += char
    return stringAux

def insertDot(item, pos):
    stringAux = ""
    done = False
    for i in range(len(item)):
        if i == pos:
            stringAux += "·"
            done = True
        if item[i] != "·":
            stringAux += item[i]
    if not done:
        stringAux += "·"
    return stringAux

def enumerateProductions(nonterminals, nonterminallist):
    enumeration = {}
    counter = 1
    for i in range(len(nonterminals)):
        for j in range(len(nonterminallist[i])):
            enumeration[f"{nonterminals[i]}->{nonterminallist[i][j]}"] = counter
            counter += 1
    return enumeration

def removeDot(item):
    stringAux = ""
    for char in item:
        if char != "·":
            stringAux += char
    return stringAux

def kernelListToSet(kernelList):
    kernelSet = set()
    for element in kernelList:
        kernelSet.add(tuple(element))
    return kernelSet

def findProduction(number, enumeratedProductions):
    for key, value in enumeratedProductions.items():
        if value == number:
            return key
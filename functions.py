from inspect import stack

import utilities as u
from utilities import derivationPath


def initialFirst(details):
    nonTerminals = details[0]
    first = details[2]
    for element in nonTerminals:
        first[element] = set()


def initialFollow(details):
    nonTerminals = details[0]
    follow = details[3]
    for element in nonTerminals:
        follow[element] = set()
        if element == "S":
            follow[element].add("$")

def getFirst(nonTerminal, details):
    nonTerminals = details[0]
    nonTerminalsList = details[1]
    first = details[2]
    counterEpsilon = 0
    hasEpsilon = True
    for production in nonTerminalsList[nonTerminals.index(nonTerminal)]:
        for letter in production:
            if hasEpsilon:
                if not letter.isupper():
                    first[nonTerminal].add(letter)
                    hasEpsilon = False
                else:
                    hasEpsilon = False
                    for element in first[letter]:
                        if element == "e":
                            hasEpsilon = True
                            counterEpsilon += 1
                        else:
                            first[nonTerminal].add(element)
            else:
                break
        hasEpsilon = True
        if counterEpsilon == len(production) and len(production) != 0:
            first[nonTerminal].add("e")


def firstString(string, details):
    first = details[2]
    firstStr = set()
    hasEpsilon = True
    epsilonCounter = 0
    for letter in string:
        if hasEpsilon:
            hasEpsilon = False
            if letter.isupper():
                firstStr.update(first[letter])
                if "e" in firstStr:
                    epsilonCounter += 1
                    firstStr.remove("e")
                    hasEpsilon = True
            else:
                firstStr.add(letter)
        else:
            break
    if epsilonCounter == len(string):
        firstStr.add("e")
    return firstStr

def getFollow(nonTerminal, details):
    nonTerminals = details[0]
    nonTerminalsList = details[1]
    follow = details[3]
    for production in nonTerminalsList[nonTerminals.index(nonTerminal)]:
        for number in range(len(production)):
            if production[number].isupper():
                aux = production[number + 1:]
                if len(aux) > 0:
                    firstAux = firstString(aux, details)
                    if "e" in firstAux:
                        follow[production[number]].update(follow[nonTerminal])
                        firstAux.remove("e")
                    follow[production[number]].update(firstAux)
                else:
                    ()
                    follow[production[number]].update(follow[nonTerminal])

def isLL1(details):
    isLL1 = True
    nonTerminals = details[0]
    follow = details[3]
    productions = details[1]
    pairs = u.makePairs(productions)

    for number in range(len(nonTerminals)):
        for pair in pairs[number]:
            first1 = firstString(pair[0], details)
            first2 = firstString(pair[1], details)
            if len(first1 & first2) != 0:
                isLL1 = False
                break
            if "e" in first1 and len(follow[nonTerminals[number]] & first2) != 0:
                isLL1 = False
                break
            elif "e" in first2 and len(follow[nonTerminals[number]] & first1) != 0:
                isLL1 = False
                break
    return isLL1

def predictiveTable(details):
    if isLL1(details):
        nonTerminals = details[0]
        nonterminalsList = details[1]
        follow = details[3]
        table = {}
        for nonTerminalNumber in range(len(nonTerminals)):
            for production in nonterminalsList[nonTerminalNumber]:
                firstProduction = firstString(production, details)
                for letter in firstProduction:
                    if letter != "e":
                        table[f"{nonTerminals[nonTerminalNumber]},{letter}"] = f"{nonTerminals[nonTerminalNumber]}->{production}"
                    else:
                        for symbol in follow[nonTerminals[nonTerminalNumber]]:
                            table[f"{nonTerminals[nonTerminalNumber]},{symbol}"] = f"{nonTerminals[nonTerminalNumber]}->{production}"
        return table
    else:
        return None

def predictiveParsing(table, string, details):
    string = u.stringPreparation(string)
    symbolCounter = 0
    derivationPath = ""
    inputBuffer = f"{string}$"
    stack = ["$", "S"]
    derivation = ["S"]
    a = inputBuffer[symbolCounter]
    x = stack[-1]
    while x != "$":
        if x == a:
            stack.pop(-1)
            symbolCounter += 1
            a = inputBuffer[symbolCounter]
        elif not x.isupper():
            derivationPath = "ERROR"
            break
        elif f"{x},{a}" not in table:
            derivationPath = "ERROR"
            break
        elif f"{x},{a}" in table:
            derivation.append(table[f"{x},{a}"])
            stack.pop(-1)
            for element in table[f"{x},{a}"][::-1]:
                if element == ">":
                    break
                elif element != "e":
                    stack.append(element)
        x = stack[-1]
    if derivationPath != "ERROR":
        derivationPath = u.derivationPath(derivation[1:])
    return derivationPath

def clousure(setI, grammarDetails):
    nonTerminalsList = grammarDetails[1]
    nonTerminals = grammarDetails[0]
    clousureSet = []
    setToAppend = [x for x in setI]
    auxSet = setToAppend[:]
    while len(setToAppend) != 0:
        for production in setToAppend:
            body = production[1]
            if body[-1] != "·":
                char = body[body.index("·")+1]
                if char.isupper() and char != "":
                    for element in nonTerminalsList[nonTerminals.index(char)]:
                        item = (char, u.insertDot(element, 0))
                        if item not in clousureSet:
                            auxSet.append(item)
        for element in auxSet:
            clousureSet.append(element)
        setToAppend = auxSet
        auxSet = []
    return clousureSet

def canSet(details, enumeratedProductions):
    pendingKernel = [[("S'", "·S")]]
    action = {}
    goTo = {}
    can = []
    foundKernels = [u.kernelListToSet(pendingKernel[0])]
    processedKernels = []
    while len(pendingKernel) != 0:
        kernelSymbols = []
        kernelItems = []
        kernelSet = pendingKernel[0]
        actualItem = foundKernels.index(set(kernelSet))
        can.append(clousure(kernelSet, details))
        for ind in range(len(can[-1])):
            nonTerminal = can[-1][ind][0]
            body = can[-1][ind][1]
            dotPos = body.index("·")
            if dotPos == len(body) - 1:
                if nonTerminal != "S'":
                    for element in details[3][nonTerminal]:
                        action[f"{actualItem},{element}"] = ["r",enumeratedProductions[f"{nonTerminal}->{u.removeDot(body)}"]]
                else:
                    action[f"{actualItem},$"] = "acc"
            else:
                nextChar = body[dotPos + 1]
                if nextChar not in kernelSymbols:
                    kernelSymbols.append(nextChar)
                    kernelItems.append([])
                kernelItems[kernelSymbols.index(nextChar)].append((nonTerminal, u.insertDot(body, dotPos+2)))
        pendingKernel.pop(0)
        processedKernels.append(set(kernelSet))
        for symInd in range(len(kernelSymbols)):
            newKernel = kernelItems[symInd]
            symbol = kernelSymbols[symInd]
            setNew = set(newKernel)
            if setNew not in foundKernels:
                foundKernels.append(setNew)
            if setNew not in processedKernels:
                pendingKernel.append(newKernel)
            if symbol.isupper():
                goTo[f"{actualItem},{symbol}"] = foundKernels.index(setNew)
            else:
                action[f"{actualItem},{symbol}"] = ["s", foundKernels.index(setNew)]
    table = [action, goTo]
    return can, table

def SLRParsing(string, enumeratedProductions, table):
    string = u.stringPreparation(string)
    inputString = string + "$"
    derivationPath = ""
    derivation = []
    stack = [0]
    action = table[0]
    goTo = table[1]
    a = inputString[0]
    stringIndex = 0
    while True:
        s = stack[0]
        key = f"{s},{a}"
        if key in action:
            data = action[key]
            if type(data) == list:
                if data[0] == "s":
                    stack = [data[1]] + stack
                    stringIndex += 1
                    a = inputString[stringIndex]
                else:
                    production = u.findProduction(data[1], enumeratedProductions)
                    nonterminal = production[0]
                    body = production[production.index(">") + 1:]
                    stack = stack[len(body):]
                    stack = [goTo[f"{stack[0]},{nonterminal}"]] + stack
                    derivation.append(production)
            else:
                return u.derivationPath(derivation[::-1])
        else:
            return "ERROR"
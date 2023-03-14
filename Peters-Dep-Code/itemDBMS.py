import json
import re
import os

parameterList = ["ac", "isMagic", "damage", "damageType", "isHomebrew", "Master"]
conditionList = ["equals", "greaterThan", "lessThan", "greaterThanorEqual", "lessThanorEqual"]
maxHistoryCount = 5

def add(itemName):
    with open("manifestMaster.json", "r") as outfile:
        masterManifest = json.load(outfile)

    if itemName in masterManifest:
        #print("Item already exists in the itembase")
        return False

    #print(itemName)
    #print("Creating an item with the name: " + itemName)
    #isMagic = input("Is this item magical?(Enter yes or no)\n\t>")
    #acNum = input("What is the ac of this item?(Enter a number)\n\t>")
    #damageNum = input("What the is the damage of the item?(Enter 0 if there is no damage done)\n\t>")
    #try:
    #    isZero = int(damageNum)

    #    if isZero != 0:
    #        damageType = input("What is the damage type?\n\t>")
    #    else:
    #        damageType = "none"

    #except ValueError:
    #    damageType = "none"
    #print("Enter a discription:")
    #x = ''
    #discription = ''
    #for line in iter(input, x):
    #    pass
    #    discription = discription + line + " "
        
    #item = {

    #    "itemName": itemName,
    #    "isMagic": isMagic,
    #    "damage": damageNum,
    #    "ac": acNum,
    #    "damageType": damageType,
    #    "isHomebrew": "yes",
    #    "discription": discription

    #}
    item = {

        "itemName": itemName,
        "isMagic": "yes",
        "damage": 0,
        "ac": 0,
        "damageType": "none",
        "isHomebrew": "yes",
        "discription": "blank"

    }

    with open("items/" + itemName.replace(" ", "") + ".json", "w") as outfile:
        json.dump(item, outfile)

    masterManifest[itemName] = itemName.replace(" ", "")
    with open("manifestMaster.json", "w") as outfile:
        json.dump(masterManifest, outfile)

    with open("manifestisMagic.json", "r") as outfile:
        masterManifest = json.load(outfile)
    masterManifest[itemName] = "yes"
    with open("manifestisMagic.json", "w") as outfile:
        json.dump(masterManifest, outfile)

    with open("manifestdamage.json", "r") as outfile:
        masterManifest = json.load(outfile)
    masterManifest[itemName] = 0
    with open("manifestdamage.json", "w") as outfile:
        json.dump(masterManifest, outfile)

    with open("manifestac.json", "r") as outfile:
        masterManifest = json.load(outfile)
    masterManifest[itemName] = 0
    with open("manifestac.json", "w") as outfile:
        json.dump(masterManifest, outfile)

    with open("manifestdamageType.json", "r") as outfile:
        masterManifest = json.load(outfile)
    masterManifest[itemName] = "none"
    with open("manifestdamageType.json", "w") as outfile:
        json.dump(masterManifest, outfile)

    with open("manifestisHomebrew.json", "r") as outfile:
        masterManifest = json.load(outfile)
    masterManifest[itemName] = "yes"
    with open("manifestisHomebrew.json", "w") as outfile:
        json.dump(masterManifest, outfile)
    
    jsonItem = json.dumps(item)

    #print(item)
    #print(jsonItem)

##    returnStatement = {

##        "printType" : "add"
##        "data" : item

##    }
    
##    return returnStatement
    return True

def edit(itemName):
    return "yet to be implemented"

def delete(itemName):
    with open("manifestMaster.json", "r") as outfile:
        masterManifest = json.load(outfile)

    if itemName in masterManifest:
        result = True
    else:
        return False

    with open("manifestisMagic.json", "r") as outfile:
        masterManifest = json.load(outfile)
    result = dict(filter(lambda x: x[0] != itemName, masterManifest.items()))
    with open("manifestMaster.json", "w") as outfile:
        json.dump(result, outfile)

    with open("manifestisMagic.json", "r") as outfile:
        masterManifest = json.load(outfile)
    result = dict(filter(lambda x: x[0] != itemName, masterManifest.items()))
    with open("manifestisMagic.json", "w") as outfile:
        json.dump(result, outfile)

    with open("manifestdamage.json", "r") as outfile:
        masterManifest = json.load(outfile)
    result = dict(filter(lambda x: x[0] != itemName, masterManifest.items()))
    with open("manifestdamage.json", "w") as outfile:
        json.dump(result, outfile)

    with open("manifestac.json", "r") as outfile:
        masterManifest = json.load(outfile)
    result = dict(filter(lambda x: x[0] != itemName, masterManifest.items()))
    with open("manifestac.json", "w") as outfile:
        json.dump(result, outfile)

    with open("manifestdamageType.json", "r") as outfile:
        masterManifest = json.load(outfile)
    result = dict(filter(lambda x: x[0] != itemName, masterManifest.items()))
    with open("manifestdamageType.json", "w") as outfile:
        json.dump(result, outfile)

    with open("manifestisHomebrew.json", "r") as outfile:
        masterManifest = json.load(outfile)
    result = dict(filter(lambda x: x[0] != itemName, masterManifest.items()))
    with open("manifestisHomebrew.json", "w") as outfile:
        json.dump(result, outfile)

    os.remove("items/" + itemName + ".json")

#    returnStatement = {

#        "printType" = "delete"
#        "data" = "Deleted Successfully"

#    }

#    return returnStatement
    return result

def search(parameters):
    result = list(filter(lambda x: parameters[0] in x, parameterList))
    if len(result) == 0:
        print("No extra parameters were provided with. Searching all items.")
        returnedResult = searchManifest("Master", parameters, 0)
        print("Here is the list of all the returned values:")
        for key in returnedResult.keys():
            print("{}".format(key))
    elif len(result) > 1:
        print("More than one searchable paramters were found\n", result)
        whichOne = input("Which paremeter would you like to search for?\n\t>")
        if whichOne in result:
            print("Searching with this parameter in mind: " + whichOne)
            print("Not implemented yet")
        else:
            print("This is not one of the listed parameters")
    else:
        condition = list(filter(lambda x: parameters[1] in x, conditionList))
        if len(condition) == 0:
            print("Searching in the " + result[0])
            returnedResult = searchManifest(result[0], parameters, 0)
            print("Here is the list of all the returned values:")
            for key in returnedResult.keys():
                print("{}".format(key))
        else:
            returnedResult = searchManifest(parameters[0], parameters[1:], 1)
            print("Here is the list of all returned values:")
            for key in returnedResult.keys():
                print("{}".format(key))
    return

def searchManifest(whichManifest, searchTerms, switch):
    if(switch == 0):
        resultString = ' '.join(searchTerms)
        try:
            with open("manifest" + whichManifest + ".json", "r") as outfile:
                manifest = json.load(outfile)
            result = dict(filter(lambda x: resultString in x[0], manifest.items()))
            return result
        except:
            return []
    
    operator = searchTerms[0]
    refinedSearch = searchTerms[1:]
    resultString = ' '.join(refinedSearch)
    with open("manifest" + whichManifest + ".json", "r") as outfile:
        manifest = json.load(outfile)

    try:
        int(resultString)
    except:
        return []

    if operator == "equals":
        result = dict(filter(lambda x: int(x[1]) == int(resultString), manifest.items()))
    elif operator == "greaterThan":
        result = dict(filter(lambda x: int(x[1]) > int(resultString), manifest.items()))
    elif operator == "lessThan":
        result = dict(filter(lambda x: int(x[1]) < int(resultString), manifest.items()))
    elif operator == "greaterThanorEquals":
        result = dict(filter(lambda x: int(x[1]) >= int(resultString), manifest.items()))
    elif operator == "lessThanorEquals":
        result = dict(filter(lambda x: int(x[1]) <= int(resultString), manifest.items()))

    return result

def printItem(itemName):
    with open("items/" + itemName.replace(" ", "") + ".json", "r") as outfile:
            item = json.load(outfile)
    for value, key in item.items():
        print(value, ": ", key)
    return

def printManifest(whichManifest):
    return "Not yet implemented"

def printHistory():
    with open("history", "r") as outfile:
        historyContents = outfile.read()
    print(historyContents)
    return

def printHelp():
    print("List of avaiable commands:")
    print("add <itemName>: This command takes an itemName and takes you through a list of options to create the item. It then adds it to the database.")
    print("delete <itemName>: This command takes an itemName and deletes it from the database system")
    print("search <parameters>: This command takes in a search parameter and searchs the database for all relevant items")
    return

def commandParser(commandInput):
    command = commandInput[0]
    args = commandInput[1:]
    argsString = ' '.join(args)

    returnBool = True
    
    if command == "search":
        search(args)
    elif command == "add":
        add(argsString)
    elif command == "delete":
        delete(argsString)
    elif command == "print":
        printItem(argsString)
    elif command == "help":
        printHelp()
    elif command == "exit":
        print("Exiting program. Have a good day!")
    elif command == "history":
        printHistory()
    else:
        returnBool = False
        print("Error!! " + command + " is not a valid command!")
    return returnBool

def storeToHistory(commandLineInput):
    
    with open("history", "a") as outfile:
        outfile.write(commandLineInput + "\n")
        
    with open("history", "r") as outfile:
        historyContentsList = [word.strip('\n') for word in outfile.readlines()]
    if len(historyContentsList) > maxHistoryCount:
        historyContentsListCorrected = historyContentsList[len(historyContentsList)-maxHistoryCount-1 : len(historyContentsList)-1]
        historyContentsListCorrectedString = '\n'.join(historyContentsListCorrected)
        print(historyContentsListCorrectedString)
        with open("history", "w") as outfile:
            outfile.write(historyContentsListCorrectedString)
    return True

print("Welcome to the commandLine itemDMBS tool!")
printHelp()

commandInput = ["DNE"]

while commandInput[0] != "exit":
    commandInputRaw = input(">")
    commandInput = re.split(" ", commandInputRaw)
    commandParser(commandInput)
    storeToHistory(commandInputRaw)
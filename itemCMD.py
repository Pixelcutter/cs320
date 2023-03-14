from itemDB import *

"""
This function takes in an input and parses it all out
It splits it via spaces
It then counts all the arguments and returns how many arguments there where and what the arguments where
"""
def commandParser(rawInput):
    args = { 
        "c": rawInput.split()
    }
    args.update({"v": len(args["c"])})
    return args

"""
This sets data the data in a way that kwargs will accept it for the methods that use it
"""
def keyCreation(unformatedData):
    keyValue = {}
    for entry in unformatedData:
        tmp = entry.split("=")
        keyValue.update({str(tmp[0]): tmp[1]})

    if "homebrew" in keyValue:
        keyValue["homebrew"] = strToBool(keyValue["homebrew"])

    return keyValue

"""
This will take pyDict/JSON and print it out in a manner that makes sense
"""
def printResult(result):
    if result["success"]:
        for key, value in result.items():
            if(not key == "success"):
                if(key == "string"):
                    print(value)

    else:
        print(f"Error!!", result["reason"], sep="\n")

"""
To convert a true/false as strings into a bool, because apperently there are no good methods out there already
"""
def strToBool(string):

    return string.lower() in ['true']


"""
This is all the cli interface code

Most of it hasn't been implemented yet
Most of the item database stuff has been implemented and should be working correctly
"""
def main():
    items = itemDB()#Start the database
    items.updateList()#Must call this function, else you are fucked

    #Prints out a welcome message
    print("Welcome to the item database command line interface.\nThis the command line version of the database.\nType 'help' to get a list of commands.\nType 'exit' to exit the CMD inteface.")

    command = ""

    #stuck in this loop until something unexpected happens or the user enters in exit
    while command != "exit":
        commandInput = input(">")
        args = commandParser(commandInput)
        command = args["c"][0]

        print(args)

        #Item database stuff
        if(command == "addItem" and args["v"] >= 3):
            keyValue = keyCreation(args["c"][2:])
            printResult(items.addItem(args["c"][1], **keyValue))

        elif(command == "deleteItem" and args["v"] == 2):
            printResult(items.deleteItem(args["c"][1]))

        elif(command == "editItem" and args["v"] == 4):
            if "homebrew" == args["c"][2]:
                args["c"][3] = strToBool(args["c"][3])
            printResult(items.editItem(args["c"][1], args["c"][2], args["c"][3]))

        elif(command == "printItem" and args["v"] == 2):
            printResult(items.printItem(args["c"][1]))

        elif(command == "listItems" and args["v"] == 1):
            print("List of all items in the database:")
            print(items)

        elif(command == "search"):
            print("Hasn't been implemented yet")

        #Inventory database stuff
        elif(command == "setInventory" and args["v"] == 2):
            print("Hasn't been implemented yet")

        elif(command == "newInventory" and args["v"] == 2):
            print("Hasn't been implemented yet")

        elif(command == "deleteInventory" and args["v"] == 2):
            print("Hasn't been implemented yet")

        elif(command == "increment" and args["v"] == 3):
            print("Hasn't been implemented yet")

        elif(command == "decrement" and args["v"] == 3):
            print("Hasn't been implemented yet")

        elif(command == "remove" and args["v"] == 2):
            print("Hasn't been implemented yet")

        #Other Stuff
        elif(command == "help" and args["v"] == 1):
            print("Hasn't been implemented yet")

        elif(command == "exit"):
            print("Have a good day!")

        else:
            print("No such command exists or not enough arguments.\nRun 'help' to get help")


if __name__ == '__main__':
    main()
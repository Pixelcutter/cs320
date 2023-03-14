import os
import json
"""
This is the item database system. You only need to call this class once to start the database
After you call the class you will want to run the updateList() method, otherwise everything will break
Each methat that is ment to be accessed from the outside (public methods) should return a json/pyDict for the you query
"""

class itemDB:
    """
    This initializes the database and sets what are valid things that can go into the item files
    This will also set all the valid search keys that user can do
    """
    def __init__(self):#Intilizes the database
        self.itemList = []
        self.validKeys = [
            "name",
            "homebrew",
            "description",
            "range",
            "ac",
            "damage",
            "rarity",
            "weight"
        ]
        self.validSearchKeys = [
            "name",
            "homebrew",
            "ac",
            "damage",
            "weight",
            "rarity"
        ]

    """
    This method will update the active list of items that are avaible
    It is require to run once right after you instantiate the database
    Otherwise you don't ever need to run it again, all methods that affect the database will run this as needed on its own

    Public Method
    """        
    def updateList(self):#Updates the current list of items in the database
        self.itemList = []
        for file in os.listdir("items/"):
            if file.endswith(".item"):
                self.itemList.append(self.itemName("items/" + file))

    """
    This method add a new item to the database
    It will require to have homebrew tag as one the arguments you pass it, if you don't have it will tell you
    You should be able to add whatever tags you want while creating a new item

    Public Method
    """
    def addItem(self, name, **kwargs):#This will add an item to the database
        if(self.isItem(name)):
            return self.jsonFormat(False, reason = "Item already exists")

        tmp = self.convertKwargs(**kwargs)

        if(not ('homebrew' in tmp)):
            return self.jsonFormat(False, reason = "Must contain the homebrew key")

        newItem = {"name": name}
        for tName, dType in kwargs.items():
            if tName in self.validKeys:
                newItem.update({str(tName): dType})

        self.save(newItem)
        self.updateList()

        return self.jsonFormat(True)

    """
    This method will delete an item from the database
    There really isn't any prereqs needed other than it needs to be a valid item in the database

    Public Method
    """
    def deleteItem(self, name):#This will delete and item from the database
        if(not self.isItem(name)):
            return self.jsonFormat(False, reason = "Item does not exist")

        if(not self.isHomebrew(name)):
            return self.jsonFormat(False, reason = "Don't have permission to delete item")

        if os.path.exists(f'items/{self.fileName(name)}.item'):
            os.remove(f'items/{self.fileName(name)}.item')
        else:
            return self.jsonFormat(False, reason = "No such file exists")

        self.updateList()

        return self.jsonFormat(True)

    """
    This method will edit an item
    you will need to provide it with the name of the item, the value you want to affect, and what you want it to be
    It will check if item exists, and then check if you supplied a valid key to affect, if it passes those two reqs it will update the item

    Public Method
    """
    def editItem(self, name, key, value):#This will edit the item in the database
        if(not self.isItem(name)):
            return self.jsonFormat(False, reason = "Item does not exist")
        
        if(not self.isHomebrew(name)):
            return self.jsonFormat(False, reason = "Don't have permission to edit item")

        if key not in self.validKeys:
            return self.jsonFormat(False, reason = "{key} is not a valid key")

        if(key == "name"):
            with open(f'items/{self.fileName(name)}.item', 'r') as file:
                item = json.load(file)
                item[key] = value
                self.save(item)
            os.remove(f'items/{self.fileName(name)}.item')
            self.updateList()
            return self.jsonFormat(True)                      

        with open(f'items/{self.fileName(name)}.item', 'r') as file:
            item = json.load(file)
            if key in item:
                item.update({key: value})
                self.save(item)
                return self.jsonFormat(True)
            else:
                return self.jsonFormat(False, reason = "Doesn't exist for {name}")

    """
    This method will print an item, or well make it into a printable manner
    It does two things, it formats it into a string that the user can just query in the return value
    The second thing it does is print out each indiviual value into the return statment so it can be formatted as the user wishes    

    Public Method
    """
    def printItem(self, name):#This prints out the item in a nice format
        if(not self.isItem(name)):
            return self.jsonFormat(False, reason = "Item does not exist")

        with open(f'items/{self.fileName(name)}.item', 'r') as file:
            item = json.load(file)
            itemString = ""
            for key, value in item.items():
                itemString += f"{str(key).capitalize()}: {value}\n"

            return self.jsonFormat(True, string = itemString, **item)

    """
    This method will search the database based on what you inputed and return the result, if any
    It should differentate between numerical values and string values and search accordingly
    It will also figure out which operator you want
    Though you dont have to supply a search key and operator as it does have defaults it will back onto

    Known issue: it currently doesn't work as intended as will only search if the item exists trying to do anything else will fail with what you are trying to do

    Public Method
    """
    def search(self, search, searchKey="name", operator="="):
        if not searchKey in self.validSearchKeys:
            return self.jsonFormat(False, result = "{searchKey} is not a valid search key")

        if self.checkGreaterThan(operator):
            if isinstance(search, str):
                strResult = filter(lambda x: search in x, self.itemList)
                return self.jsonFormat(True, result = strResult)

            return self.jsonFormat(True, result = "IDK")
        elif self.checkLessThan(operator):
            return self.jsonFormat(True, result = "IDK")
        elif self.checkLessEqual(operator):
            return self.jsonFormat(True, result = "IDK")
        elif self.checkGreaterEqual(operator):
            return self.jsonFormat(True, result = "IDK")
        elif self.checkEqual(operator):
            return self.jsonFormat(True, result = "IDK")
        else:
            return self.jsonFormat(False, reason="Can't figure out what you mean")

    """
    The following set of functions determines what kind of operator it is
    it won't catch all instances of it, but it should do a fairly decent job at it

    All methods: Private Methods
    """
    def checkGreaterThan(self, possible):
        if possible.lower().strip() in ["greaterthan", ">"]:
            return True
        return False

    def checkLessThan(self, possible):
        if possible.lower().strip() in ["lessthan", "<"]:
            return True
        return False

    def checkGreaterEqual(self, possible):
        if possible.lower().strip() in ["greaterorequal", ">=", "greaterequal"]:
            return True
        return False

    def checkLessEqual(self, possible):
        if possible.lower().strip() in ["lessequal", "<", "lessorequal"]:
            return True
        return False

    def checkEqual(self, possible):
        if possible.lower().strip() in ["=", "equal"]:
            return True
        return False

    """
    I am unsure as to why I added this, probably will have to dig through my code to figure out why, it might be redundant
    """
    def returnValidKeys(self):
        return self.validKeys

    """
    This will check if the item exists in the data base

    Private method
    """
    def isItem(self, name):#Checks to see if item exists in the data base
        for itemName in self.itemList:
            if (itemName == name):
                return True

        return False

    """
    This checks if the following item is a homebrewable item

    private method
    """
    def isHomebrew(self, itemName):#Checks to see if item is homebrew or not
        with open(f'items/{self.fileName(itemName)}.item', 'r') as file:
            item = json.load(file)
            return item["homebrew"]

    """
    Obtains the item name from the item file

    Private Method
    """
    def itemName(self, filePath):#Returns the item's name
        file = open(filePath)
        data = json.load(file)
        file.close()
        return data["name"]

    """
    The save method will save the data to the correct item file
    All methods that affect the item data in some manner will automatically call this method

    Private Method
    """
    def save(self, data):#Saves the item
        with open(f'items/{self.fileName(data["name"])}.item', 'w') as item:
            json.dump(data, item)

    """
    Converts the item name into a file name to use

    Private Method
    """
    def fileName(self, name):#Converts an item's name to an acceptable file name
        return name.lower().strip()

    """
    Had to add this method because apperently kwargs stores key value pairs as lists for whatever reason
    This will turn the key value list into a proper pyDict

    Private Method
    """
    def convertKwargs(self, **kwargs):
        formatedKwargs = {}
        
        for key, value in kwargs.items():
            formatedKwargs.update({str(key): value})

        return formatedKwargs

    """
    This method will take all the info that public methods pass it and convert it into json/pyDict like format for the public functions to return
    Requires that seccess flag be passed

    Private method
    """
    def jsonFormat(self, success, **kwargs):#Takes in the arguments and converts it into a dict/json
        dataFormated = {"success": success}

        for tName, dType in kwargs.items():
            dataFormated.update({str(tName): dType})

        return dataFormated

    """
    Using str on the class/instance itself will return all the items in the database
    """
    def __str__(self):#Will return the full list of items in database
        return str('\n'.join(map(str, self.itemList)))
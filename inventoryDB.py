import json
import os

"""
This is the inventory Database system
When called make sure to run the updateList() method right after to get list of all possible inventories
All public return values are in a pyDict/json format
"""

class inventoryDB:
    def __init__(self):
        self.current = ""
        self.inventoryList = []

    """
    This will get all the avaible inventories

    Public Method 
    """
    def updateList(self):
        self.inventoryList = []
        for file in os.listdir("inventory/"):
            if file.endswith(".inventory"):
                self.inventoryList.append(self.inventoryName("inventory/" + file))

    """
    The user will need to call this set the inventory they want to use
    It will check if the inventory exists, and if it does it will set the current value to that inventory

    Public Method
    """
    def setInventory(self, name):
        if(not self.inventoryExists(name)):
            return self.jsonFormat(False, reason = "Inventory for {name} does not exist")

        self.current = self.inventoryName(f"inventory/{self.fileName(name)}.inventory")

        return self.jsonFormat(True)

    """
    The user can use this to create a new inventory
    It will check if the inventory with the same name exists already

    Public Method
    """
    def createNewInventory(self, name):
        if(self.inventoryExists(name)):
            return self.jsonFormat(False, reason = "Inventory for {name} already exists")

        with open(f"inventory/{self.fileName(name)}.inventory", "w") as newInventory:
            json.dump({"name": name}, newInventory)

        self.updateList()

        return self.jsonFormat(True)

    """
    The user can use this to delete an inventory
    Once deleted it cannot be recovered, though might implement a system to do so down the line

    Public Method
    """
    def deleteInventory(self, name):
        if(not self.inventoryExists(name)):
            return self.jsonFormat(False, reason = "Inventory for {name} does not exist")

        if os.path.exists(f'inventory/{self.fileName(name)}.inventory'):
            os.remove(f'inventory/{self.fileName(name)}.inventory')
        else:
            return self.jsonFormat(False, reason = "No such file exists")

        if(self.current == name):
            self.current = ""

        self.updateList()

        return self.jsonFormat(True)

    """
    The user can use this method to add an item to the current inventory, or increment the count of the item

    Public Method
    """
    def incrementItem(self, itemName, amount):
        if(not self.inventoryExists(self.current)):
            return self.jsonFormat(False, reason = "Inventory for {name} does not exist")

        inventory = {}

        with open(f'inventory/{self.fileName(self.current)}.inventory', "r") as inventoryFile:
            inventory = json.load(inventoryFile)
            if itemName in inventory:
                tmp = inventory[itemName]
                tmp += amount
                inventory[itemName] = tmp
            else:
                inventory.update({itemName, amount})
            
        with open(f'inventory/{self.fileName(self.current)}.inventory', "w") as inventoryFile:
            json.dump(inventory, inventoryFile)

        self.updateList()
        
        return self.jsonFormat(False, reason = "Cause yeah")

    """
    The user can use this decrement the amount of an item in the inventory
    It can go into the negatives

    Public method
    """
    def decrementItem(self, itemName, amount):
        if(not self.inventoryExists(self.current)):
            return self.jsonFormat(False, reason = "Inventory for {self.current} does not exist")

        inventory = {}

        with open(f'inventory/{self.fileName(self.current)}.inventory', "r") as inventoryFile:
            inventory = json.load(inventoryFile)
            if itemName in inventory:
                tmp = inventory[itemName]
                tmp -= amount
                inventory[itemName] = tmp
            else:
                inventory.update({itemName, (-1 * amount)})
            
        with open(f'inventory/{self.fileName(self.current)}.inventory', "w") as inventoryFile:
            json.dump(inventory, inventoryFile)

        self.updateList()

        return self.jsonFormat(True)

    """
    The user can use this to remove an item from the current inventory entirely

    Public Method
    """
    def removeItem(self, itemName):
        if(not self.inventoryExists(self.current)):
            return self.jsonFormat(False, reason = "Inventory for {self.current} does not exist")

        if os.path.exists(f'items/{self.fileName(self.current)}.item'):
            os.remove(f'items/{self.fileName(self.current)}.item')
        else:
            return self.jsonFormat(False, reason = "No such file exists")

        self.updateList()

        return self.jsonFormat(True)

    """
    The user can use this method to get the contents of the current inventory

    Public Method
    """
    def printInventory(self):
        if(not self.inventoryExists(self.current)):
            return self.jsonFormat(False, reason = "Inventory for {self.current} does not exist")

        with open(f'inventory/{self.fileName(self.current)}.inventory', "r") as inventoryFile:
            inventory = json.load(inventoryFile)
            return self.jsonFormat(True, **inventory)

    """
    This will check if the inventory exists

    Private Method
    """
    def inventoryExists(self, name):
        for inventoryName in self.itemList:
            if (inventoryName == name):
                return True

        return False

    """
    This will obtain the name of the inventory

    Private Method
    """
    def inventoryName(self, filePath):
        file = open(filePath)
        data = json.load(file)
        file.close()
        return data["name"]

    """
    This will convert the inventory name into a file name

    Private Method
    """
    def fileName(self, name):#Converts an item's name to an acceptable file name
        return name.lower().strip()

    """
    This method takes what the public methods give it and convert it into a pyDict/json format
    It requires a success flag to be passed

    Private Method
    """
    def jsonFormat(self, success, **kwargs):#Takes in the arguments and converts it into a dict/json
        dataFormated = {"success": success}

        for tName, dType in kwargs.items():
            dataFormated.update({str(tName): dType})

        return dataFormated

    """
    When str is called on the inventory database it will return all the aviable inventories
    """
    def __str__(self):
        return str('\n'.join(map(str, self.inventoryList)))

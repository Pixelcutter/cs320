from os.path import exists as itemExists
import os

class item:

    #This creates the item or imports the item from a file if it exists
    def __init__(self, name, homebrew):
        self.parameterList = ["name", "homebrew", "rarity", "type", "damage", "ac", "discription"]
        if(itemExists(f'items/{self.fileName(name)}.item')):
            with open(f'items/{self.fileName(name)}.item', 'r') as file:
                itemInfoRaw = file.read()
                self.itemInfo = itemInfoRaw.split("\n")
        else:
            self.itemInfo = []
            self.itemInfo.append(name)
            self.itemInfo.append(str(homebrew))
            self.save()

    #this edits the item info
    def editItem(self, parameter, data):
        if(not self.isHomebrew()):#checks if the item is homebrew or not
            return False#if its not homebrew you cant edit it

        dataLocation = self.parameterList.index(parameter)#this gets the location of where data is being edited

        if(dataLocation == 0):#if the name is being changed it updates the file name
            os.rename(f'items/{self.fileName(self.itemInfo[0])}.item', f'items/{self.fileName(data)}.item')

        self.itemInfo[dataLocation] = str(data)#updates the info and makes sure its a string data type
        
        self.save()#calls the save function

        return True

    def itemName(self):
        return self.itemInfo[0]

    def isHomebrew(self):
        return self.convertStrToBool(self.itemInfo[1])

    def save(self):
        with open(f'items/{self.fileName(self.itemInfo[0])}.item', 'w') as file:
            itemString = ""
            for data in self.itemInfo:
                itemString += data + "\n" 
            file.write(itemString)

    def convertStrToBool(self, string):
        return string.lower() in ("true")

    def fileName(self, name):
        return name.lower().strip()

    def __str__(self):
        return f'item({self.itemInfo[0]}, Homebrew = {self.itemInfo[1]})'
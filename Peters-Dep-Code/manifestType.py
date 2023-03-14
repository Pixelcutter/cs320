class manifest:
    def __init__ (self, name):
        self.name = name
        self.list = {}

    def editItem(self, itemName, value):
        if value == "Remove":
            self.__removeItem(itemName)
        else:
            self.list.update({itemName: value})

    def __removeItem(self, itemName):
        del self.list[itemName]

    def __str__ (self):
        return f'manifest({self.name}, Contents = {self.list})'
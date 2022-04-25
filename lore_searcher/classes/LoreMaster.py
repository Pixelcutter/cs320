import textwrap
import os
import json
from functools import reduce
from .LorePage import Page
from .LoreSection import Section
from .LoreSearcher import Searcher

class Master:
    def __init__(self, characterName):
        self.cName = characterName
        self.cBio = ""
        self.cClass = ""
        self.cRace = ""
        self.cOrigin = ""
        self.cSex = ""
        self.sectionDict = {}
        self.sectionNames = []

    def addSection(self, section) -> bool:
        sName = section.sectionName
        if sName in self.sectionDict:
            return False
        self.sectionDict[sName] = section
        self.sectionNames.append(sName)
        return True

    def delSection(self, sectionName) -> bool:
        if sectionName not in self.sectionDict:
            return False
        del self.sectionDict[sectionName]
        del self.sectionNames[self.sectionNames.index(sectionName)]
        return True

    def printSection(self, sectionName, bound=80):
        if sectionName in self.sectionDict:
            self.sectionDict[sectionName].printSection(bound)

    def getPageTotal(self) -> int:
        return reduce(lambda x,y: x+y, list(map(lambda x: self.sectionDict[x].totalPages, self.sectionDict)))

    def printLore(self, bound=80):
        print(self.cName.title().center(bound) + "\n")
        print("Class:", self.cClass.title())
        print("Race:", self.cRace.title())
        print("Sex:", self.cSex.title())
        print("Origin:", self.cOrigin.title(), "\n")
        print(textwrap.fill(f"{self.cBio}", width=bound))
        print()
        for name, section in self.sectionDict.items():
            section.printSection(bound)

    def getMaster(self):
        return {
            "character-name": self.cName,
            "cBio": self.cBio,
            "cClass": self.cClass,
            "cRace": self.cRace,
            "cOrigin": self.cOrigin,
            "cSex": self.cSex,
            "page-total": self.getPageTotal(),
            "section-names": self.sectionNames,
            "sections": list(map(lambda x: self.sectionDict[x].getSection(), self.sectionNames))
        }

    def listSection(self, sectionName) -> bool:
        if sectionName in self.sectionDict:
            self.sectionDict[sectionName].listSection()
            return True
        return False

    def listAllSections(self):
        for name, section in self.sectionDict.items():
            section.listSection()

    def saveLore(self, filePath) -> bool:
        try:
            data = self.getMaster()
            with open(filePath, 'w+') as fd:
                json.dump(data, fd, indent=4)
        except:
            return False

    def loadLore(self, filePath) -> bool:
        if not os.path.exists(filePath):
            return False

        data = json.load(filePath)
        self.cName = data['character-name']
        self.cBio = data['cBio']
        self.cClass = data['cClass']
        self.cOrigin = data['cOrigin']
        self.cRace = data['cRace']
        self.cSex = data['cSex']
        self.sectionNames = data['section-names']

        for section in data['sections']:
            newSection = Section(section['name'])
            for page in section['page-list']:
                tmpPage = Searcher.searchID()


    def prettySave(self, path) -> bool:
        pass

import textwrap
import os
import sys
import json
from functools import reduce
from .LorePage import Page
from .LoreSection import Section
from .LoreSearcher import Searcher

""" Master is the backbone of any LoreBook. It stores all attribute information
for a character / campaign, as well as any LoreSections / LorePages. There are
several useful methods available to Master:

- getMeta()
- addSection(section: Section)
- delSection(sectionName: str)
- printSection(sectionName: str, bound: int)
- getPageTotal()
- printLore(bound: int, saving: bool)
- getMaster()
- listSection(sectionName: str)
- listAllSections()
- saveLore(filePath: str)
- loadLore(filePath: str, searcher: Searcher)
- prettySave(filePath: str, bound: int)

You can read about these methods below
"""

class Master:

    # Initializes Master
    # characterName: desired name for character / campaign
    # isCamp: bool that indicates character (False) or campaign (True)
    # bio: character / campaign backstory
    # cClass: character class
    # race: character race
    # origin: character origin
    # sex: character sex
    # cArch: character archetype

    def __init__(self, characterName="Adventurer", isCamp=False, bio="", cClass="", cArch="", race="", origin="", sex=""):
        self.cName = characterName
        self.cBio = bio
        self.cClass = cClass
        self.cRace = race
        self.cOrigin = origin
        self.cSex = sex
        self.cArch = cArch
        self.version = 0        # version no. of Master. Used for saving
        self.isSaved = False    # indicates if Master has been saved recently
        self.isCamp = isCamp    
        self.sectionDict = {}   # holds LoreSections
        self.sectionNames = []  # holds LoreSection names

    # Returns meta data about LoreMaster

    def getMeta(self):
        return {
            "vNum": self.version,
            "page-total": self.getPageTotal(),
            "isSaved": self.isSaved,
            "section-total": len(self.sectionNames)
        }

    # Adds a new LoreSection to sectionDict as long as sectionName not
    # already in sectionDict. sectionName also added to sectionNames
    # section: LoreSection
    # returns: True of False depending on success

    # Note: Should return a {"success": bool, "reason": "error reason"} dict

    def addSection(self, section) -> bool:
        sName = section.sectionName
        if sName in self.sectionDict:
            return False
        self.sectionDict[sName] = section
        self.sectionNames.append(sName)
        return True

    # Deletes a LoreSection from SectionDict if it exists. sectionName
    # deleted from sectionNames on success
    # str sectionName: name of section to be deleted
    # returns bool: True of False depending on success

    # Note: Should return a {"success": bool, "reason": "error reason"} dict

    def delSection(self, sectionName) -> bool:
        if sectionName not in self.sectionDict:
            return False
        del self.sectionDict[sectionName]
        del self.sectionNames[self.sectionNames.index(sectionName)]
        return True

    # Prints LoreSection using LoreSection's print method
    # str sectionName: name of section to be printed
    # int bound: char limit for printed lines

    def printSection(self, sectionName, bound=80):
        if sectionName in self.sectionDict:
            self.sectionDict[sectionName].printSection(bound)

    # Returns total amount of pages present in all sectionDict
    # LoreSections

    def getPageTotal(self) -> int:
        if len(self.sectionNames) == 0:
            return 0
        return reduce(lambda x, y: x+y, list(map(lambda x: self.sectionDict[x].totalPages, self.sectionDict)))

    # Prints all fields, LoreSections and LorePages to terminal in nice format
    # int bound: char limit for printed lines
    # bool saving: Bool used by self.prettySave()

    def printLore(self, bound=80, saving=False):
        # Will not clear screen if pretty saving lore
        if not saving:
            os.system('clear')
        cType = "Campaign:" if self.isCamp else "Character:"
        print(f"<{{{{  {cType} {self.cName.title()}  }}}}>\n".center(bound))

        # cClass, cRace, cSex, cArch, and cOrigin only printed if Master
        # is a character, not a campaign

        if self.isCamp != True:
            print("Class:", self.cClass.title(), f"({self.cArch.title()})")
            print("Race:", self.cRace.title())
            print("Sex:", self.cSex.title())
            print("Origin:", self.cOrigin.title(), "\n")
        print(textwrap.fill(f"{self.cBio}", width=bound))
        print()
        # for LoreSection in sectionDict, call printSection() method
        for name, section in self.sectionDict.items():
            section.printSection(bound)

    # Returns a dictionary representation of LoreMaster. Useful when
    # wanting to save to json, or send as json

    def getMaster(self):
        return {
            "character-name": self.cName,
            "cBio": self.cBio,
            "cClass": self.cClass,
            "cRace": self.cRace,
            "cOrigin": self.cOrigin,
            "isCamp": self.isCamp,
            "cSex": self.cSex,
            "cArch": self.cArch,
            "vNum": self.version,
            "page-total": self.getPageTotal(),
            "section-names": self.sectionNames,
            "sections": list(map(lambda x: self.sectionDict[x].getSection(), self.sectionNames))
        }

    # Calls specific LoreSecti0ns .listSection() method if it's in sectionDict
    # str sectionName: name of section to be listed
    # returns bool: True of False depending on success

    # Note: Should return a {"success": bool, "reason": "error reason"} dict

    def listSection(self, sectionName) -> bool:
        if sectionName in self.sectionDict:
            self.sectionDict[sectionName].listSection()
            return True
        return False


    # Lists all LoreSections using their .listSection() methods

    def listAllSections(self):
        for name, section in self.sectionDict.items():
            section.listSection()

    # Saves LoreMaster to json file with .lore extension
    # str filePath: desired save path
    # returns bool: True or False depending on success

    # Note: Should return a {"success": bool, "reason": "error reason"} dict 

    def saveLore(self, filePath) -> bool:
        try:
            data = self.getMaster()
            with open(filePath, 'w+') as fd:
                json.dump(data, fd, indent=4)
        except Exception as e:
            print(e)
            return False

    # Sets all fields to the fields present in a .lore file
    # str filePath: path to .lore file
    # Searcher searcher: LoreSearcher object
    # returns bool: True of False depending on success

    # Note: Could use more error checking. Can currently attempt to
    # load non .lore files, or .lore files with wrong structure.
    # Should return a {"success": bool, "reason": "error reason"} dict

    def loadLore(self, filePath, searcher) -> bool:
        if not os.path.exists(filePath):
            print(f"ERROR: '{filePath}' could not be found")
            return False

        if os.path.isdir(filePath):
            print(f"ERROR: '{filePath}' is a directory")
            return False

        with open(filePath, 'r') as fd:
            data = json.load(fd)

        # atttributes set

        self.cName = data['character-name']
        self.cBio = data['cBio']
        self.cClass = data['cClass']
        self.cOrigin = data['cOrigin']
        self.cRace = data['cRace']
        self.isCamp = data['isCamp']
        self.cSex = data['cSex']
        self.cArch = data['cArch']
        self.version = data['vNum']
        self.sectionNames = data['section-names']

        sectionDict = {}

        # LoreSections and their LorePages added
        # Skips adding LorePages that could not be found with LoreSearcher
        # Note: should notify user of skipping in some way other than printing

        for section in data['sections']:
            newSection = Section(section['name'])
            for page in section['page-list']:
                tmpPage = searcher.searchID(page['id'])
                if tmpPage == None:
                    print(
                        f"Sorry, a page with id:{page['id']} could not be found, skipping...")
                    continue
                newSection.addPage(tmpPage)
            sectionDict[section['name']] = newSection

        self.sectionDict = sectionDict
        return True

    # Saves LoreMaster to a .txt file in a nicer format (printLore format)
    # str filePath: path to .txt file
    # int bound: char limit for printed lines
    # returns bool: True or False depending on success

    # Note: Should return a {"success": bool, "reason": "error reason"} dict 

    def prettySave(self, filePath, bound=80) -> bool:
        try:
            # redirecting stdout to file
            sys.stdout = open(filePath, 'w+')
            self.printLore(bound, saving=True)

            # closing file pointer and restoring stdout
            sys.stdout.close()
            sys.stdout = sys.__stdout__

            return True
        except:
            return False

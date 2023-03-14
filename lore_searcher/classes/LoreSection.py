""" Section is a key component to the Lorebook. It holds all LorePages
and acts as a convenient go-between the LoreMaster and LorePage. There
are several useful methods available to Section:

- addPage(page: Page)
- delPage(pageID: int)
- delSection(sectionName: str)
- printSection(bound: int)
- getSection()
- listSection()

You can read about these methods below
"""
class Section:

    # Initializes Section
    # sectionName: desired name of Section

    def __init__(self, sectionName):
        self.sectionName = sectionName
        self.pageDict = {}      # Holds LorePages
        self.pageIDs = []       # Holds LorePage id's
        self.totalPages = 0     # Total amount of LorePages in pageDict

    # Adds a LorePage to pageDict and page.id to pageIDs
    # Page page: LorePage to be added

    def addPage(self, page):
        if page.id not in self.pageDict:
            self.pageDict[page.id] = page
            self.pageIDs.append(page.id)
            self.totalPages += 1

    # Deletes a LorePage from pageDict and page.id from pageIDs
    # int pageID: id of LorePage to be deleted

    def delPage(self, pageID):
        if pageID in self.pageDict:
            del self.pageDict[pageID]
            del self.pageIDs[self.pageIDs.index(pageID)]
            self.totalPages -= 1

    # Prints LoreSection to terminal by calling LorePages .printSummary()
    # methods
    # int bound: char limit for printed lines

    def printSection(self, bound=80):
        title = f"\nSection: {self.sectionName.title()}"
        print(title)
        print(len(title)*"-")
        for id, page in self.pageDict.items():
            page.printSummary(bound)

    # Returns LoreSection in dictionary form. Useful for saving LoreSection
    # or sending LoreSection in json format

    def getSection(self):
        return {
            "name": self.sectionName,
            "total-pages": self.totalPages,
            "ids": self.pageIDs,
            "page-list": list(map(lambda x: self.pageDict[x].getFull(), self.pageIDs))
        }

    # Lists LorePages present in LoreSection to terminal

    def listSection(self):
        print("\n" + self.sectionName.title())
        print(len(self.sectionName)*"-")
        for id, page in self.pageDict.items():
            print(f"|- {page.pageName} (id:{id})")
        print()

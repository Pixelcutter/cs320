from os import path, remove, listdir, system
from sys import stdin
from .LoreSection import Section

# Simple help command reminder print statement

def helpErrorMsg():
    print("Enter 'help' or 'h' for more details")

# Prints Command usage to terminal
# usageStr = the expected arguments for a command

def usageMsg(usageStr):
    print(f"Invalid number of arguments\nUsage: {usageStr}")

# Clears the tmp.lore file from lore_files. Called whenever lore is saved
# with saveLore()

def clrTmp():
    tmpPath = path.join("lore_files", "tmp.lore")
    if path.exists(tmpPath):
        remove(tmpPath)

# Lore Session saved to tmp.lore, a backup of sorts. Called whenever the current
# session changes state.

def tmpSave(master):
    tmpPath = path.join("lore_files", "tmp.lore")
    master.saveLore(tmpPath)

# Adds a LoreSection to session LoreMaster.

def addSection(master, args):
    if len(args) != 1:
        usageMsg("<add_section / mks, sectionName>")
        helpErrorMsg()
        return
    newSection = Section(args[0])

    # Alerts user that they are trying to overwrite a LoreSection
    # and then returns before saving
    if master.addSection(newSection) == False:
        print(f"ERROR: Section '{args[0]}' already exists")
        return
    tmpSave(master)

# Prints full pages to terminal

def printPage(searcher, args):
    if len(args) != 1:
        return
    page = searcher.searchID(args[0])
    if page != None:
        system('clear')
        page.printFull()
    else:
        print(f"Sorry, no page with id: {args[0]} exists in index")

# Deletes LoreSection from session LoreMaster

def deleteSection(master, args):
    if len(args) != 1:
        usageMsg("<del_section / rms, sectionName>")
        helpErrorMsg()
        return
    if master.delSection(args[0]) == False:
        print(f"ERROR: No '{args[0]}' section found")
        return
    tmpSave(master)

# Lists LorePages associated with LoreSection 

def listSection(master, args):
    if len(args) != 1:
        usageMsg("<list_section / ls, sectionName>")
        helpErrorMsg()
        return
    if master.listSection(args[0]) == False:
        print(f"Section '{args[0]}' was not found")

# Searches provided index for relevant files
# start = let's search know if it's a new search or not

def search(searcher, args, start):
    argc = len(args)
    if argc < 1 or argc > 2:
        return
    query = args[0]

    # search type used
    # 'OR' = Disjunctive Search
    # 'AND' = Conjunctive Search (default)
    sType = args[1] if argc == 2 else 'AND' 
    pageno = 1 # current page number of results displayed


    # The main search loop. Will continue to loop, grabbing pages of results for
    # user as long as there are results. Will stop looping if current page num
    # is equal to total available pages for query, if the user enters 'n' when
    # prompted, or when there are no results for query

    while True:
        # results will contain a list of LorePages returned from LoreSearcher.search()
        results = searcher.search(query, pageNum=pageno, searchType=sType)
        if results['results'] == None:
            if start == False:
                # No results found for query, alert user and suggest a new query
                print(
                    f"0 results found for '{results['query']}', did you mean '{results['corrected']}'?")
                return False
            else:
                return False
        elif results['results'] != None and pageno == 1:
            system('clear')
        # page total = total_relavent_docs_in_index / results_per_page
        pageTot = results['total-pages']

        # summaries of results are printed to terminal using LorePage.printSummary()
        for result in results['results']:
            result.printSummary()
        if pageno == pageTot:
            if start == False:
                print(f"No more results for '{query}'")
            return True
        uinput = input(
            "Press [Enter] for more results, or [n] to stop: ").lower()
        while uinput not in ['', 'n']:
            uinput = input(
                "Press [Enter] for more results, or [n] to stop: ").lower()
        if uinput == "":
            pageno += 1
        else:
            return True

# Adds a LorePage object to a LoreSection. LorePage created from the ID of an
# index document

def addPage(master, searcher, args):
    if len(args) != 2:
        usageMsg("<add_page / mkp, sectionName, pageID>")
        helpErrorMsg()
        return

    # LoreSection name
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"ERROR: No section titled '{sName}' found")
        return

    # index doc ID
    pageID = args[1]
    page = searcher.searchID(pageID)
    if page == None:
        print(f"Sorry, a page with id:{pageID} could not be found")
        return

    master.sectionDict[sName].addPage(page)
    tmpSave(master)

# Deletes a LorePage from a LoreSection

def delPage(master, args):
    if len(args) != 2:
        usageMsg("<del_page / rmp, sectionName, pageID>")
        helpErrorMsg()
        return
    
    # LoreSection name
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"ERROR: No section titled '{sName}' found")
        return

    # index doc ID
    pageID = args[1]
    if pageID not in master.sectionDict[sName].pageIDs:
        print(f"ERROR: '{sName}' does not have that page")
        return

    master.sectionDict[sName].delPage(pageID)
    tmpSave(master)

# Saves current Lore Builder session to lore_files/master.cName.lore

def saveLore(master, args):
    meta = master.getMeta()
    filename = master.cName.replace(' ', '_').lower()
    v = meta['vNum']
    file = f"{filename}.lore" if v == 0 else f"{filename}({v}).lore"
    filePath = path.join("lore_files", file)

    # If this lore session hasn't already been saved, alert of potential .lore
    # file overwrite. If user does not want to overwrite, session will be saved
    # as lore_files/master.cName(version_num).lore
    if path.exists(filePath) and meta['isSaved'] == False:
        uinput = input(
            f"A file named '{file}' already exists\nWould you like to replace it (y/n): ").lower()
        while uinput not in ['y', 'n']:
            uinput = input("Enter 'y' for yes, or 'n' for no: ").lower()

        # finding highest version number present in lore_files, e.g
        # highest = max([file(1).lore, file(2).lore]) = 2
        # This is not a perfect way of doing this because the name of the file
        # is not considered
        if uinput == 'n':
            dirFiles = listdir('lore_files')
            vNums = [x[x.find('(') + 1:x.find(')')]
                     for x in dirFiles if "(" in x and ").lore" in x]
            maxV = int(max(vNums)) if len(vNums) != 0 else 0
            master.version = maxV + 1
            filePath = path.join(
                "lore_files", f"{filename}({master.version}).lore")

    if len(args) != 0:
        print("Invalid save command\nUsage: <save_lore / save>")
        helpErrorMsg()
        return
    if master.saveLore(filePath) == False:
        print(f"An error occured while attempting save to '{filePath}'")
        return
    
    # prevents tmp.lore being saved as tmp(1).lore, tmp(2).lore, etc
    # Also makes sure that user will not be prompted with potential overwrite
    # warnings

    master.isSaved = True if path.basename(
        filePath) != 'tmp.lore' else master.isSaved

    # session saved successfully, clear the tmp.lore file
    clrTmp()

# Saves Lore Builder session to a master.cName.txt file in a nicer format
# Format will be the same as what is printed to screen when user enters
# '> print_lore'

def prettySave(master, textBound, args):
    cleanName = master.cName.replace(' ', '_').lower()
    filename = cleanName if master.version == 0 else f"{cleanName}({master.version})"
    filePath = path.join("lore_files", f"{filename}.txt")
    if len(args) != 0:
        usageMsg("<pretty_save / psave>")
        helpErrorMsg()
        return
    if master.prettySave(filePath, textBound) == False:
        print(f"An error occured while attempting save to '{filePath}'")

# Imports a name.txt file generated from the random character generator to the
# current Lore session. Only called when -c option used on lore_builder.py's 
# startup. Will attempt to import any valid .txt file it does not check for 
# proper random generator format........

def loadChar(master, args):
    filePath = args[0]
    if not path.exists(filePath):
        print(f"ERROR: '{filePath}' could not be found")
        return False

    with open(filePath, 'r') as fd:
        charFile = fd.read()
    
    fields = charFile.split('\n')
    master.cName = fields[0]
    # subrace + race (e.g. 'Hill Giant')
    master.cRace = f"{fields[3]} {fields[2]}"
    master.cClass = fields[4]
    master.cArch = fields[5]

    # getting full bio
    bio = ""
    for string in fields[9:]:
        if string == "**":
            break
        bio += f"{string}\n"
    master.cBio = f"{fields[6].title()}: {bio}"

# Imports a name.lore file into the current session, overwriting current session.

def loadLore(master, searcher, args):
    if len(args) != 1:
        usageMsg("<load_lore / load, path_to_file>")
        helpErrorMsg()
        return False

    filePath = args[0]
    if not path.exists(filePath):
        print(f"ERROR: '{filePath}' could not be found")
        return False

    master.loadLore(filePath, searcher)

    # prevents tmp.lore being saved as tmp(1).lore, tmp(2).lore, etc
    # Also makes sure that user will not be prompted with potential overwrite
    # warnings

    master.isSaved = True if path.basename(
        filePath) != 'tmp.lore' else master.isSaved


# Prints specified LoreSection to terminal. All LorePages present in LoreSection
# will have their summaries printed to the terminal

def printSection(master, args):
    if len(args) != 1:
        usageMsg("<print_section / ps, sectionName>")
        helpErrorMsg()
        return
    sName = args[0]
    if sName not in master.sectionDict:
        print(f"Section '{sName}' not found")
        return
    master.sectionDict[sName].printSection()

# Lets user edit current session's LoreMaster attribute fields 

def editLore(master, args):
    argc = len(args)
    if argc < 1 or argc > 2:
        usageMsg("<edit, field> or <edit, field, new_value")
        helpErrorMsg()
        return

    field = args[0].lower()
    validFields = ['name', 'bio', 'class', 'race', 'sex', 'origin', 'type', 'archetype']
    if field not in validFields:
        print(f"Field '{field}' not recognized")
        print(f"Valid Fields: " + ', '.join(validFields))
        return

    # if 2nd arg present: set newVal to 2nd arg, else: set to user input
    # The bio attribute will have its own, special, input

    if argc == 2:
        newVal = args[1]
    elif field != 'bio' and argc == 1:
        newVal = input("Enter new value: ")

    # alerts user that an attribute has successfully been updated
    updateMsg = lambda x: print(f"{x} updated!")

    if field == 'name':
        master.cName = newVal
        updateMsg("Name")
    elif field == 'bio':
        if argc != 2:
            print("Enter Bio (press [ctrl/cmd + d] when done): ")
            newVal = stdin.read()
        master.cBio = newVal
        updateMsg("\nBio")
    elif field == 'class':
        master.cClass = newVal
        updateMsg("Class")
    elif field == 'archetype':
        master.cArch = newVal
        updateMsg("Archetype")
    elif field == 'race':
        master.cRace = newVal
        updateMsg("Race")
    elif field == 'sex':
        master.cSex = newVal
        updateMsg("Sex")
    elif field == 'origin':
        master.cOrigin = newVal
        updateMsg("Origin")
    else:
        # Special care is taken when user attempts to change from character to
        # campaign, or vice versa
        while newVal not in ['camp', 'char']:
            newVal = input("Enter [camp] or [char]: ").lower()
        master.isCamp = True if newVal == 'camp' else False
    tmpSave(master)


# Prints possible commands to terminal

def printHelp():
    print("""
Command Line Options:                                                                                                   
    -l <path/to/file.lore>  Loads found lore file to new session                                                        
    -c <path/to/char.txt>   Loads randomly generated character to new session                                           
                                                                                                                        
Session Commands:                                                                                                       
    edit_lore | edit, <field>, <new_value>  Changes field to new value                                                  
    load_lore | load, <path/to/file.lore>   Loads character/campaign from file (CURRENT SESSION LOST)                   
    save_lore | save                        Saves current session to name.lore file (Json format)                       
    pretty_save | psave                     Saves current session to name.txt file in print_lore format                 
    clear | clr                             Clears console                                                              
    help | h                                Prints command list
    q | quit                                Quits current session                                                         
                                                                                                                        
Section Commands:                                                                                                       
    add_section | mks, <section_name>           Creates a new section titled 'section_name'                             
    del_section | rms, <section_name>           Removes section and all section pages                                   
    list_section | ls, <section_name>           Lists the pages present in section                                      
    print_section | ps, <section_name>          Prints page summaries for section pages                                 
    add_page | mkp, <section_name>, <page_id>   Adds page associated with id to section                                 
    del_page | rmp, <section_name>, <page_id>   Removes page associated with id from section                            
    list_all | la                               Lists all sections and their pages                                      
                                                                                                                        
Page Commands:                                                                                                          
    print_page | pp, <page_id>  Prints full page to console                                                             
                                                                                                                        
Search Commands:                                                                                                        
    search | s, <search_terms>  Searches index and prints summaries of relevant pages found

REMEMBER: Command arguments should be seperated by COMMAS. Most prompts can be skipped with [ENTER]                                                              
Example: add_page, inspiration, 400  (Adds page associated with id=400 to inspiration section)
    """)

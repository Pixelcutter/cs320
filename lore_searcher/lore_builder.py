from sys import argv
import classes.cmdFuncs as cmdf
from os import system, path, remove
from classes.LoreSearcher import Searcher
from classes.LoreSection import Section
from classes.LoreMaster import Master

"""

Todo:
 - write help function
 - write setup
 - write editLore
 - update readme

"""

master = Master()

textBound = 80
ixPath = path.join("data", "index")
if not path.exists(ixPath):
    searcher = Searcher(ixPath, path.join("data", "pages.json"))
else:
    searcher = Searcher(ixPath)


def cmdFuncs(cmd, args):
    funcs = {
        ("add_section", "mks"): lambda: cmdf.addSection(master, args),
        ("print_page", "pp"): lambda: cmdf.printPage(searcher, args),
        ("del_section", "rms"): lambda: cmdf.deleteSection(master, args),
        ("list_section", "ls"): lambda: cmdf.listSection(master, args),
        ("search", "s"): lambda: cmdf.search(searcher, args, False),
        ("add_page", "mkp"): lambda: cmdf.addPage(master, searcher, args),
        ("del_page", "rmp"): lambda: cmdf.delPage(master, args),
        ("list_all", "la"): lambda: master.listAllSections(),
        ("save_lore", "save"): lambda: cmdf.saveLore(master, args),
        ("pretty_save", "psave"): lambda: cmdf.prettySave(master, textBound, args),
        ("load_lore", "load"): lambda: cmdf.loadLore(master, searcher, args),
        ("print_lore", "pl"): lambda: master.printLore(textBound),
        ("print_section", "ps"): lambda: cmdf.printSection(master, args),
        ("clear", "clr"): lambda: system('clear'),
        ("help", "h"): lambda: cmdf.printHelp(),
        ("edit_lore", "elore"): lambda: cmdf.editLore(master)
    }

    for pair in funcs:
        if cmd in pair:
            funcs[pair]()
            return
    print(
        f"Command '{cmd}' not recognized. Enter 'help' to see available commands")


def finalSave():
    print("Would you like to save your current session?")
    uinput = input("Press [y] for yes, anything else for no: ")
    if uinput == 'y':
        filename = master.cName.replace(' ', '_').lower()
        lorePath = path.join("lore_files", f"{filename}.lore")
        if master.saveLore(lorePath) == False:
            return

    uinput = input("Would you like to PRETTY save your current session (y): ")
    if uinput == 'y':
        filename = master.cName.replace(' ', '_').lower()
        lorePath = path.join("lore_files", f"{filename}.txt")
        if master.prettySave(lorePath) == False:
            return
    # program exit was normal, clear the tmp.lore file
    cmdf.clrTmp()

def introSearch():
    print("Lets first try a search that includes all of you traits")
    allTraits = ' '.join([master.cName, master.cRace, master.cClass, master.cOrigin])
    results = cmdf.search(searcher, [allTraits], True)
    if results == False:
        print("Sorry, we couldn't find anything that had all your traits")
        uinput = input("Want to try a broader search (y): ").lower()
        if uinput == 'y':
            results = cmdf.search(searcher, [allTraits, 'OR'], True)
            if results == False:
                print("Wow! We could'nt find a thing. You sure have a unique character!")


def printIntro():
    system('clear')
    title = f"<{{  Welcome to the Lore Builder, {master.cName.title()}  }}>\n"
    print(title)
    print("Reminder: Pressing [ENTER] will skip most prompts")

    # asking user if they would like to see some search results for the fields they entered at setup
    uinput = input("Would you like to see some search results for your characters traits (y/n): ").lower()
    while uinput not in ['y', 'n', '']:
        uinput = input("Enter 'y' for yes, or 'n'/[ENTER] for no: ").lower()
    if uinput == 'y':
        introSearch()

    print("Have fun exploring!")



def setupPrompts():
    print("\nWhat is this Lore Builder session going to be used for?")
    firstQ = input(
        "Enter [camp] for Campaign, [char] for Character, or [skip]: ").lower()
    while firstQ not in ['camp', 'char', 'skip', 's']:
        firstQ = input("Enter [camp], [skip / s], or [char]: ").lower()

    if firstQ == 'skip' or firstQ == 's':
        return

    if firstQ == 'camp':
        master.isCamp = True

    cName = input("Enter your Campain's name: ") if master.isCamp else input(
        "Enter your Character's: ")
    master.cName = cName if len(cName) != 0 else master.cName

    if master.isCamp == False:
        cRace = input("Race: ")
        master.cRace = cRace
        cClass = input("Class: ")
        master.cClass = cClass
        cArch = input("Archetype: ")
        master.cArch = cArch
        cSex = input("Sex: ")
        master.cSex = cSex
        cOrigin = input("Origin: ")
        master.cOrigin = cOrigin
        print("Bio (press [ctrl/cmd + d] when done): ")
        cBio = stdin.read()
        master.cBio = cBio

    cmdf.tmpSave(master)


def mainPrompts():
    printIntro()
    while True:
        uInput = input("> ").lower()
        if uInput in ['q', 'quit']:
            break
        if uInput == '':
            continue
        tmp = uInput.split(",")
        cmdFuncs(tmp[0], list(map(lambda x: x.strip().lower(), tmp[1:])))


def main(args):
    argc = len(args)
    isNew = True

    # loading .lore file on startup with 'python3 lore_builder.py -l some_file'
    if argc > 1:
        if argc != 3:
            print(
                "Invalid amount of arguments\nUsage: python(3) lore_builder.py <option> <input_file>")
            return
        if args[1] == '-l':
            if cmdf.loadLore(master, searcher, args[2:]) == False:
                return
        elif args[1] == '-c':
            if cmdf.loadChar(master, args[2:]) == False:
                return
            master.addSection(Section("inspiration"))
            cmdf.tmpSave(master)
        mainPrompts()

    # no lore file loaded on startup, create new lore
    if isNew:
        master.addSection(Section("inspiration"))
        setupPrompts()

    mainPrompts()
    finalSave()
    print("Goodbye!")


if __name__ == '__main__':
    main(argv)

import os.path
import array
import math
import random
import pathlib
from FunctionSetUp import *

class Character:
    def __init__(self, Name, Stats, CharClass, CharRace, Level, Archetype):
        self.Name = Name
        self.Stats = Stats
        self.CharClass = CharClass
        self.CharRace = CharRace
        self.Level = Level
        self.Archetype = Archetype


def chargen(name):
    fileExist = os.path.exists("CharDatabase/characters/" + name + ".txt")
    if fileExist:
        print("File Exists!")
        while True:
            editExist = input("Override? y/n: ")
            if editExist == "y":
                filetemp = open("CharDatabase/characters/" + name + ".txt", "w")
                break
            if editExist == "n":
                skipEnd = True
                print("No Override! Goodbye.")
                return 1 #  Goodbye exit.
            else:
                print("Please Answer only in y or n...")
    else:
        filetemp = open("CharDatabase/characters/" + name + ".txt", "x")
    choicelist =    ["0: Level",    "1: Race",  "2: Class",     "3: Background",    "4: Stats"]
    templist =      ['level', 'race', 'subrace', 'class', 'archetype', 'background', 'stats']
    #  =============================================================================================
    #       CHOOSING WHAT YOU WANT TO DO IN WHAT ORDER
    #  =============================================================================================
    while choicelist != []:
        choiceA = input("What do you want to do now?\n|"+str(choicelist)+"|\nEnter Here: ")
        #  ==========================================================================
        if (choiceA == "0") and ("0: Level" in choicelist):
            while True:
                try:
                    levelChoice = int(input("What Level do you want? (1-20): "))
                    if (levelChoice >= 1) and (levelChoice <= 20):
                        break
                    else:
                        print("Only Levels between 1 and 20 please!")
                except:
                    print("Not valid! Please choose a number between 1 and 20 only.")
            print("Level Chosen: "+str(levelChoice))
            templist[0] = levelChoice
            choicelist.pop(choicelist.index("0: Level"))
        #  ==========================================================================
        if (choiceA == "1") and ("1: Race" in choicelist):
            #  Action on getting a random Race
            #  (And sub race!)
            raceChoice, subChoice = fullrace()
            templist[1] = raceChoice
            templist[2] = subChoice
            choicelist.pop(choicelist.index("1: Race"))
        #  ==========================================================================
        if (choiceA == "2") and ("2: Class" in choicelist):
            classChoice, archChoice = fullclass()
            templist[3] = classChoice
            templist[4] = archChoice
            choicelist.pop(choicelist.index("2: Class"))
        #  ==========================================================================
        if (choiceA == "3") and ("3: Background" in choicelist):
            # Action on getting background.
            bgChoice = fullbg()
            templist[5] = bgChoice
            choicelist.pop(choicelist.index("3: Background"))
        #  ==========================================================================
        if (choiceA == "4") and ("4: Stats" in choicelist):
            #Action on getting stats.
            statChoice = fullstat()
            templist[6] = statChoice
            choicelist.pop(choicelist.index("4: Stats"))
        if (choiceA != "0") and (choiceA != "1") and (choiceA != "2") and (choiceA != "3") and (choiceA != "4"):
            print("Invalid! Try again!")
        print("- = - = - = - = - = - = - = - = - = - = - = - = - = - = -")
    #  =============================================================================================
    #      STAT AND EXTRA ALTERCATIONS HAPPEN HERE AFTER MAIN DETAILS HAVE BEEN GRABBED
    #  =============================================================================================
    templist[6] = racemod(templist[1],templist[6])
    print("Your Current Character: " + str(name) + " -> " + str(templist))
    i = 0
    filetemp.write(str(name)+"\n")
    while i < 7:
        filetemp.write(str(templist[i])+"\n")
        i += 1
    filetemp.write("**\n")
    #  =============================================================================================
    #      STAT AND EXTRA ALTERCATIONS HAPPEN HERE AFTER MAIN DETAILS HAVE BEEN GRABBED
    #  =============================================================================================
    filetemp.close()
    bgabbilitiesadd(name,templist[5])
    raceabilitiesadd(name,templist[1])
    classbaseadd(name,templist[3],templist[0])
    return 0


if __name__ == '__main__':
    chargen("Charlie")
import math
import random
import array
import os

class Character:
    def __init__(self, Name, Stats, CharClass, CharRace, Level, Archetype):
        self.Name = Name
        self.Stats = Stats
        self.CharClass = CharClass
        self.CharRace = CharRace
        self.Level = Level
        self.Archetype = Archetype


def statmod(n):
    return math.floor((n - 10) / 2)


def statrollFDS():
    y = array.array('i', [0, 0, 0, 0, 0, 0])
    i = 0
    for x in y:
        rolls = array.array('i', [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)])
        rolls.remove(min(rolls))
        SumNum = sum(rolls)
        y[i] = SumNum
        i+= 1
    z = y.tolist()
    q = map(statmod, z)
    #  print("Stats:   "+str(z))
    #  print("Mods:    "+str(list(q)))
    return z


def classchooser():
    try:
        classNum = 0
        classList = open("../CharDatabase/Class/$List.txt")
        classRead = classList.read()
        classEntries = classRead.split("\n")
        for j in classEntries:
            if j:
                classNum += 1
        ClassChosen = classEntries[random.randint(0, classNum-1)]
    finally:
        classList.close()
        return ClassChosen


def racechooser():
    try:
        raceNum = 0
        raceList = open("../CharDatabase/Race/$List.txt")
        raceRead = raceList.read()
        raceEntries = raceRead.split("\n")
        for i in raceEntries:
            if i:
                raceNum += 1
        RaceChoosen = raceEntries[random.randint(0, raceNum-1)]
    finally:
        raceList.close()
        return RaceChoosen


def fullstat():
    while True:
        myStat = statrollFDS()
        myMod = list(map(statmod, myStat))
        print("Current Stat: "+str(myStat))
        print("Current Mods: "+str(myMod))
        statFlag = False
        while True:
            incheck = input("Reroll? (y/n): ")
            if incheck == "n":
                statFlag = True
                break
            if incheck == "y":
                statFlag = False
                break
            else:
                print("Not Correct. 'y' or 'n' Only Please. ")
        if statFlag is True:
            break
    return myStat


def checkrace(name):
    fileExist = os.path.exists("CharDatabase/Race/" + name + ".txt")
    if fileExist:
        return True
    else:
        return False

def checkclass(name):
    fileExist = os.path.exists("CharDatabase/Class/" + name + ".txt")
    if fileExist:
        return True
    else:
        return False

def fullrace():
    while True:
        while True:
            myRace = racechooser()
            if checkrace(myRace):
                break
        print("Current Race: "+str(myRace))
        raceFlag = False
        while True:
            incheck = input("Reroll? (y/n): ")
            if incheck == "n":
                raceFlag = True
                break
            if incheck == "y":
                raceFlag = False
                break
            else:
                print("Not Correct. 'y' or 'n' Only Please. ")
        if raceFlag is True:
            break
    return myRace

def fullclass():
    while True:
        while True:
            myClass = classchooser()
            if checkclass(myClass):
                break
        print("Current Class: "+str(myClass))
        classFlag = False
        while True:
            incheck = input("Reroll? (y/n): ")
            if incheck == "n":
                classFlag = True
                break
            if incheck == "y":
                classFlag = False
                break
            else:
                print("Not Correct. 'y' or 'n' Only Please. ")
        if classFlag is True:
            break
    return myClass

if __name__ == '__main__':
    myStat = fullstat()
    myMod = list(map(statmod, myStat))
    myRace = fullrace()
    myClass = fullclass()
    print("- = - = - = - = - = - = - = - = - = - = - = - =")
    print("Stats:   "+str(myStat))
    print("Mods:    "+str(myMod))
    print(str(myRace)+" "+str(myClass))

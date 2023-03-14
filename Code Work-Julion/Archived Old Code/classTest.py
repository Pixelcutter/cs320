import math
import random
import array

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
        classList = open("Class/$List.txt")
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
        raceList = open("Race/$List.txt")
        raceRead = raceList.read()
        raceEntries = raceRead.split("\n")
        for i in raceEntries:
            if i:
                raceNum += 1
        RaceChoosen = raceEntries[random.randint(0, raceNum-1)]
    finally:
        raceList.close()
        return RaceChoosen


def classinfo():
    #  Info for class stuff
    print("Class Info: ")


def raceinfo():
    #  info for race stuff
    print("Race Info: ")


if __name__ == '__main__':
    myStat = statrollFDS()
    myMod = list(map(statmod, myStat))
    #  Go through loops until you get the stats you want.
    myRace = racechooser()
    #  Go through loops until you get the race you want.
    myClass = classchooser()
    #  Go through loops until you get the class you want.
    print("Stats:   "+str(myStat))
    print("Mods:    "+str(myMod))
    print(str(myRace)+" "+str(myClass))

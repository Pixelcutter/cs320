import os.path
import array
import math
import random
import pathlib
from chclass import *
from chrace import *
from chbackground import *

class Character:
    def __init__(self, Name, Stats, CharClass, CharRace, Level, Archetype, Subrace):
        self.Name = Name
        self.Stats = Stats
        self.CharClass = CharClass
        self.CharRace = CharRace
        self.Level = Level
        self.Archetype = Archetype
        self.Subrace = Subrace


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
    return z


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


if __name__ == '__main__':
    GiveName = input("Whats the person's name? Enter Here: ")
    GiveLevel = input("What is the person's Level? Enter Here: ")
    #  Create a function that checks input if int or str. Work into it.
    GiveClass, GiveArch = fullclass()
    GiveRace, GiveSub = fullrace()
    # GiveSub = subchoose(str(GiveRace))
    TheDude = Character(GiveName,fullstat(),GiveClass, GiveRace,GiveLevel,GiveArch, GiveSub)
    print(str(TheDude.Name)+" is a "+str(TheDude.Subrace)+" "+str(TheDude.CharRace)+" "+str(TheDude.CharClass)+", He is level "+str(TheDude.Level)+" and his archetype is "+str(TheDude.Archetype))
    print(str(TheDude.Name)+"'s Stats are: "+str(TheDude.Stats))
    print("- = - = - = - = - = - = - = - = - = - = -")
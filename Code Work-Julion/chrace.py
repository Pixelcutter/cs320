import random
import pathlib


def racechooser():
    try:
        raceNum = 0
        raceList = open("CharDatabase/Race/$List.txt")
        raceRead = raceList.read()
        raceEntries = raceRead.split("\n")
        for i in raceEntries:
            if i:
                raceNum += 1
        RaceChoosen = raceEntries[random.randint(0, raceNum-1)]
    finally:
        raceList.close()
        return RaceChoosen


def racerollertry(RaceChoosen):
    while True:
        racetest = RaceChoosen
        opentest = False
        racepath = "CharDatabase/Race/"+str(racetest)+".txt"
        path = pathlib.Path(str(racepath))
        if path.exists():
            #  print("😊 Race File Exists! -> "+str(racetest))
            opentest = True
        else:
            #  print("😢 Race File DOESNT Exist... -> "+str(racetest))
            opentest = False
            return False
        if opentest:
            break
    return racetest


def subchoose(racename):
    try:
        file = open("CharDatabase/Race/"+racename+".txt")
        raceread = file.read()
        raceLineList = raceread.split("\n")
        subraceList = raceLineList[6].split(", ")
        subnum = 0
        for i in subraceList:
            if i:
                subnum += 1
        gotsub = subraceList[random.randint(0,subnum-1)]
    except:
        print("Somehow an error in the subrace choosing!!")
    if gotsub == "0":
        gotsub = ""
    return str(gotsub)


def fullrace():
    while True:
        while True:
            myRace = racechooser()
            if racerollertry(myRace):
                sub = subchoose(myRace)
                break
        print("Current Race: "+str(sub)+" "+str(myRace))
        raceFlag = False
        while True:
            print("Yes / No / Choose My Own")
            incheck = input("Reroll? (y/n/c): ")
            if incheck == "n":
                raceFlag = True
                break
            if incheck == "y":
                raceFlag = False
                break
            if incheck == "c":
                myRace = pickrace()
                sub = subchoose(str(myRace))
                while True:
                    choosecheck = input("You have gotten " + str(sub) + " " + str(myRace) + ". Keep? (y/n): ")
                    if choosecheck == "y":
                        return myRace, sub
                    if choosecheck == "n":
                        break
                    else:
                        print("Only 'y' or 'n' please.")
            else:
                print("Not Correct. 'y' or 'n' Only Please. ")
        if raceFlag is True:
            break
    return myRace, sub

def pickrace():
    try:
        raList = open("CharDatabase/Race/$List.txt")
        raread = raList.read()
        raEntries = raread.split("\n")
        ranum = len(raEntries)
        raTrueList = []
        for x in raEntries:
            if racerollertry(str(x)):
                raTrueList.append(str(x))
        i = 0
        for y in raTrueList:
            print("Number ["+str(i)+"]: "+str(y))
            i = i+1
        while True:
            num = input("Enter Number You Want: ")
            if (int(num) <= i-1) and (int(num) >= 0):
                print("Chosen: " + str(raTrueList[int(num)]))
                return raTrueList[int(num)]
            else:
                print("Try Again.")
    finally:
        raList.close()

def racemod(myRace, myStats):
    try:
        racefile = open("CharDatabase/Race/"+str(myRace)+".txt")
        raceread = racefile.read()
        racesplit = raceread.split("\n")
        racestat = racesplit[1].split(", ")
        j = 0
        while (j<6):
            myStats[j] = int(myStats[j])+int(racestat[j])
            j += 1
    finally:
        racefile.close()
        return myStats

def raceabilitiesadd(filename,myrace):
    try:
        charfile = open("CharDatabase/characters/"+str(filename)+".txt",'a')
        racefile = open("CharDatabase/Race/"+str(myrace)+".txt")
        raceread = racefile.read()
        racesplit = raceread.split("\n")
        j = 8
        while racesplit[j] != "**":
            charfile.write(str(racesplit[j])+"\n")
            j += 1
    finally:
        charfile.write("**\n")
        racefile.close()
        charfile.close()


if __name__ == '__main__':
    stat = [14, 11, 13, 12, 11, 8]
    print(str(stat))
    Dstat = racemod("Dwarf",stat)
    print("Dwarf: "+str(Dstat))
    Estat = racemod("Elf",stat)
    print("Elf: "+str(Estat))
    Hstat = racemod("Human (Standard)",stat)
    print("Human: "+str(Hstat))
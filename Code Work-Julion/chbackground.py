import random
import pathlib

def bgchooser():
    try:
        bgnum = 0
        bgList = open("CharDatabase/Background/$List.txt")
        bgread = bgList.read()
        bgEntries = bgread.split("\n")
        for o in bgEntries:
            if o:
                bgnum += 1
        bgChosen = bgEntries[random.randint(0,bgnum-1)]
    finally:
        bgList.close()
        return bgChosen


def bgrollertry(bgChosen):
    while True:
        bgtest = bgChosen
        opentest = False
        bgpath = "CharDatabase/Background/"+str(bgtest)+".txt"
        path = pathlib.Path(str(bgpath))
        if path.exists():
            opentest = True
        else:
            opentest = False
            return False
        if opentest:
            break
    return bgtest

def fullbg():
    while True:
        while True:
            mybg = bgchooser()
            if bgrollertry(mybg):
                break
        print("Current Background: "+str(mybg))
        bgFlage = False
        while True:
            print("Yes / No / Choose My Own")
            incheck = input("Reroll? (y/n/c): ")
            if incheck == "n":
                bgFlag = True
                break
            if incheck == "y":
                bgFlag = False
                break
            if incheck == "c":
                mybg = pickbackground()
                while True:
                    choosecheck = input("You have gotten " + str(mybg) + ". Keep? (y/n): ")
                    if choosecheck == "y":
                        return mybg
                    if choosecheck == "n":
                        break
                    else:
                        print("Only 'y' or 'n' please.")
            else:
                print("Not Correct. 'y' or 'n' Only Please. ")
        if bgFlag is True:
            break
    return mybg

def bgabbilitiesadd(filename, bg):
    try:
        charfile = open("CharDatabase/characters/"+str(filename)+".txt",'a')
        bgfile = open("CharDatabase/Background/"+str(bg)+".txt")
        bgread = bgfile.read()
        bgsplit = bgread.split("\n")
        j = 7
        while bgsplit[j] != "**":
            charfile.write(str(bgsplit[j])+"\n")
            j += 1
    finally:
        charfile.write("**\n")
        bgfile.close()
        charfile.close()

def pickbackground():
    try:
        bgList = open("CharDatabase/Background/$List.txt")
        bgread = bgList.read()
        bgEntries = bgread.split("\n")
        bgnum = len(bgEntries)
        bgTrueList = []
        for x in bgEntries:
            if bgrollertry(str(x)):
                bgTrueList.append(str(x))
        i = 0
        for y in bgTrueList:
            print("Number ["+str(i)+"]: "+str(y))
            i = i+1
        while True:
            num = input("Enter Number You Want: ")
            if (int(num) <= i-1) and (int(num) >= 0):
                print("Chosen: "+str(bgTrueList[int(num)]))
                return bgTrueList[int(num)]
            else:
                print("Try Again.")
    finally:
        bgList.close()
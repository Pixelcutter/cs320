import os.path
import array
import math
import random
import pathlib


def classchooser():
    try:
        classNum = 0
        classList = open("CharDatabase/Class/$List.txt")
        classRead = classList.read()
        classEntries = classRead.split("\n")
        for j in classEntries:
            if j:
                classNum += 1
        ClassChosen = classEntries[random.randint(0, classNum-1)]
    finally:
        classList.close()
        return ClassChosen


def classrollertry(ClassChoosen):
    while True:
        classtest = str(ClassChoosen)
        opentest = False
        classpath = "CharDatabase/Class/"+str(classtest)+".txt"
        path = pathlib.Path(str(classpath))
        if path.exists():
            #  print("😊 Class File Exists! -> "+str(classtest))
            opentest = True
        else:
            #  print("😢 Class File DOESNT Exist... -> "+str(classtest))
            opentest = False
            return False
        if opentest:
            break
    return classtest


def archchoose(classname):
    #  Chooses archetype based on class.
    #  print("Choosing archetype. . .")
    try:
        file = open("CharDatabase/Class/"+classname+".txt")
        classRead = file.read()
        classLineList = classRead.split("\n")
        archetypeList = classLineList[8].split(", ")
        archnum = 0
        for i in archetypeList:
            if i:
                archnum += 1
        gotarch = archetypeList[random.randint(0, archnum-1)]
        return str(gotarch)
    except:
        print("Somehow an error in the archetype choosing!!")


def fullclass():
    while True:
        while True:
            myClass = classchooser()
            if classrollertry(myClass):
                arch = archchoose(myClass)
                break
        print("Current Class: "+str(arch)+" "+str(myClass))
        classFlag = False
        while True:
            print("Yes / No / Choose My Own")
            incheck = input("Reroll? (y/n/c): ")
            if incheck == "n":
                classFlag = True
                break
            if incheck == "y":
                classFlag = False
                break
            if incheck == "c":
                myClass = pickclass()
                arch = archchoose(str(myClass))
                while True:
                    choosecheck = input("You have gotten " + str(arch) + " " + str(myClass) + ". Keep? (y/n): ")
                    if choosecheck == "y":
                        return myClass, arch
                    if choosecheck == "n":
                        break
                    else:
                        print("Only 'y' or 'n' please.")
            else:
                print("Not Correct. 'y' or 'n' Only Please. ")
        if classFlag is True:
            break
    return myClass, arch

def pickclass():
    try:
        clList = open("CharDatabase/Class/$List.txt")
        clread = clList.read()
        clEntries = clread.split("\n")
        clnum = len(clEntries)
        clTrueList = []
        for x in clEntries:
            if classrollertry(str(x)):
                clTrueList.append(str(x))
        i = 0
        for y in clTrueList:
            print("Number ["+str(i)+"]: "+str(y))
            i = i+1
        while True:
            num = input("Enter Number You Want: ")
            if (int(num) <= i-1) and (int(num) >= 0):
                print("Chosen: " + str(clTrueList[int(num)]))
                return clTrueList[int(num)]
            else:
                print("Try Again.")
    finally:
        clList.close()

def classbaseadd(filename, myclass, level):
    try:
        charfile = open("CharDatabase/characters/"+str(filename)+".txt",'a')
        classfile = open("CharDatabase/Class/" + str(myclass) + ".txt")
        classread = classfile.read()
        classsplit = classread.split("\n")
        j = 11
        while (j-11) < level:
            charfile.write("Level ["+str(j-10)+"]: "+str(classsplit[j])+"\n")
            j += 1
    finally:
        charfile.write("**\n")
        classfile.close()
        charfile.close()
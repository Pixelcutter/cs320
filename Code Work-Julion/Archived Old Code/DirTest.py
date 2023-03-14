import random
import array
import os

if __name__ == '__main__':

    test = 0

    try:
        raceNum = 0
        classNum = 0
        raceList = open("Race/$List.txt")
        classList = open("Class/$List.txt")
        raceRead = raceList.read()
        classRead = classList.read()
        raceEntries = raceRead.split("\n")
        classEntries = classRead.split("\n")
        for i in raceEntries:
            if i:
                raceNum += 1
        for j in classEntries:
            if j:
                classNum += 1
        raceRand = raceEntries[random.randint(0, raceNum)]
        classRand = classEntries[random.randint(0, classNum)]
        print(str(raceRand + " " + classRand))


    finally:

        raceList.close()
        classList.close()

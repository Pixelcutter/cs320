import math
import random
import array

def infocheck(cra, name):
    print("Please Enter: '"+ cra + "' And '"+name+"'...")
    ArchCheck = infoget()
    return ArchCheck

def checktest():
    # Requires Manual input, will have print statements as well to help lead user in testing.
    assert infocheck("c","fighter") == ['Battle Master', 'Champion', 'Samurai', 'Gunslinger']
    assert infocheck("c","wizard") == ['Illusion', 'Necromancy', 'War Magic', 'Evocation']
    assert infocheck("a","NONE NEEDED") == "Archetype goes here when implemented."
    #  no archetypes been implemented yet, but will require testing.
    assert infocheck("r", "human") == "Got a Race!"

    print("Checks were true!")


def infoget():
    while True:
        infoInput = input("Class or Race or Archetype? (c/r/a): ")
        check = 0
        if str(infoInput) == "c":
            #  Class checking.
            check = 1
            break
        if str(infoInput) == "r":
            #  race checking
            check = 2
            break
        if str(infoInput) == "a":
            #  archetype checking
            check = 3
            break
        else:
            print("Nah you wrong. Try again.")

    if check == 1:
        #  CLASS
        while True:
            className = input("What Class? Enter: ")
            try:
                classFile = open("Class/"+className+".txt")
                break
            except IOError:
                print("Nah, that dont exist. Try again.")

        classFile = open("Class/"+className+".txt")

        classRead = classFile.read()
        classLineList = classRead.split("\n")
        statPriority = classLineList[1].split(", ")
        saveProficiency = classLineList[2].split(", ")
        armorProficiency = classLineList[3].split(", ")
        weaponProficiency = classLineList[4].split(", ")
        toolProficiency = classLineList[5].split(", ")
        skillNum = int(classLineList[6])
        skillList = classLineList[7].split(", ")
        archetypeList = classLineList[8].split(", ")
        hitDice = int(classLineList[9])
        #  ========================================================
        print("Hit Dice:            "+str(hitDice))
        print("Stats in Order:      [STR, DEX, CON, INT, WIS, CHA]")
        print("Stat Priority:       "+str(statPriority))
        print("Save Proficiency:    " + str(saveProficiency))
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        if armorProficiency[3] == "1":
            armorProficiency[3] = "Shields"
        else:
            armorProficiency.pop(3)
        if armorProficiency[2] == "1":
            armorProficiency[2] = "Heavy"
        else:
            armorProficiency.pop(2)
        if armorProficiency[1] == "1":
            armorProficiency[1] = "Medium"
        else:
            armorProficiency.pop(1)
        if armorProficiency[0] == "1":
            armorProficiency[0] = "Light"
        else:
            armorProficiency.pop(0)
        if not armorProficiency:
            armorProficiency.append("None")
        print("Armor Proficiency:   "+str(armorProficiency))
        #  ================================================
        if weaponProficiency[0] == "1":
            weaponProficiency[0] = "Simple"
            wpSimFlag = True
        else:
            wpSimFlag = False
        if weaponProficiency[1] == "1":
            weaponProficiency[1] = "Martial"
            wpMarFlag = True
        else:
            wpMarFlag = False
        if wpMarFlag is False:
            weaponProficiency.pop(1)
        if wpSimFlag is False:
            weaponProficiency.pop(0)
        if not weaponProficiency:
            weaponProficiency.append("None")
        print("Weapon Proficiency:  "+str(weaponProficiency))
        #  ================================================
        if toolProficiency[0] == "":
            toolProficiency.pop(0)
        if not toolProficiency:
            toolProficiency.append("None")
        print("Tool Proficiency:    "+str(toolProficiency))
        #  ================================================
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("Number of Skills to Choose: "+str(skillNum))
        print("Skills:              "+str(skillList))
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("Archetype Options:   "+str(archetypeList))
        return archetypeList


    if check == 2:
        raceName = input("What Race? Enter: ")
        raceFile = open("Race/"+raceName+".txt")
        print(raceFile.read())
        return "Got a Race!"

    if check == 3:
        return "Archetype goes here when implemented."

if __name__ == '__main__':
    checktest()
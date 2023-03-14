import math
import random
import array
import os.path

def roll(num):
    if not num:
        return random.randint(1, 20)
    return random.randint(1, num)


def isnum(num):
    if not num:
        return False
    if isinstance(num,int):
        return True
    else:
        return False


def rollmax(num):
    if not num:
        return 20
    if isnum(num):
        return int(num)


def modcheck(num):
    if isnum(num):
        return num
    if not num:
        return "0"


def continuetoroll():
    while True:
        num = input("Dice Size? Enter: ")
        if num == "q":
            break
        if isnum(num) or (not num):
            result = roll(num)
            mod = input("Modifier for it? Enter:")
            mod = modcheck(mod)
            max = rollmax(num)
            output = int(result)+int(mod)
            print("Total outcome: "+str(result)+" + "+str(mod)+" = "+str(output))
            if (result == 1):
                print("Critical Fail! Boo!")
            if(result == max):
                print("Critical Rolled! Woo!")
            print("- = - = - = - = - = - = - = - = -")
        if (num != "q") and (isnum(num) is False) and str(num):
            print("Not q or number. Try again.")
    return "Done"


def singleroll(num=20, inputmod=0):
        if num == "q":
            return (-1)
        if isnum(num) or (not num):
            result = roll(num)
            mod = modcheck(inputmod)
            max = rollmax(num)
            output = int(result)+int(mod)
            print("Total outcome: "+str(result)+" + "+str(mod)+" = "+str(output))
            if (result == 1):
                print("Critical Fail! Boo!")
            if(result == max):
                print("Critical Rolled! Woo!")
            print("- = - = - = - = - = - = - = - = -")
        if (num != "q") and (isnum(num) is False) and num:
            print("Not q or number. Try again.")


if __name__ == '__main__':
    singleroll()
    singleroll(100,20)
    beep = continuetoroll()
    if beep == "Done":
        print("Exiting full program.")

    else:
        print("Oh shit somehow we fucked up.")
import math
import random
import array
import os.path

def isnum(input=None):
    #checks to see if the input is a number, and only a number
    try:
        if input is None:
            return False
        if isinstance(input, list):
            if len(input) == 1:
                if isnum(input[0]):
                    return True
            return False
        int(input)
        numeric = str(input)
        if numeric.isnumeric():
            return True
        else:
            return False
    except ValueError:
        return False

def isstring(input=None):
    #  Checks to see if its a string, not numbers solely.
    try:
        if input is None:
            return False
        if isinstance(input, list):
            if len(input) == 1:
                if isstring(input[0]):
                    return True
            return False
        numeric = str(input)
        if numeric.isnumeric():
            return False
        return True
    except ValueError:
        return False


def diceroll(num=20):
    #  Does a Dice Roll, if none, automatically assume 20 sided dice.
    #  If num is NOT a number, returns ValueError.
    if isnum(num):
        return random.randint(1, num)
    else:
        return ValueError


def rollmany(amount="missing",dice=20):
    #  Tries to roll many dice, and place into a list.
    #  If amount is empty, will return a "Missing Argument" String
    try:
        if amount == "missing":
            return ["Missing Argument"]
        if isnum(amount):
            i = 0
            list =[]
            while i < amount:
                list.append(diceroll(dice))
                i += 1
            return list
    except TypeError:
        return ["TypeError"]



if __name__ == '__main__':
   print(str(rollmany(5,100)))
   print(str(rollmany()))
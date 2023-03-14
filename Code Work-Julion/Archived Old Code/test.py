import math
import random
import array


def statmod(n):
    return math.floor((n - 10) / 2)

def assgn1(variable):
    positive = [18,17,16,15,14]
    if variable in positive:
        return True
    else:
        return False

def assgn2(variable):
    negative = [9,8,7,6,5,4,3]
    if variable in negative:
        return True
    else:
        return False

def assgn3(variable):
    neutral = [13,12,11,10]
    if variable in neutral:
        return True
    else:
        return False

if __name__ == '__main__':
    debug = 0
    assignment = 1
    if debug == 1:
        print("Hello World!\n")  # Testing Print Statements
    x = random.randint(1, 6)  # Testing the random Int workings, Low-to-High as variables.
    if debug == 1:
        print("Just a random number:", x)  # Shows the random number.
    y = array.array('i', [0, 0, 0, 0, 0, 0])  # Sets up the array to hold the 6 stats.
    i = 0  # My brain is so new to python, I'm using an int to count upwards on the for loop to match Array.
    for x in y:
        rolls = array.array('i',
                            [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)])
        if debug == 1:
            print("Full Array list of Rolls:", rolls)  # Output array('i', [1, 2, 3, 4]) Some numbers
        if debug == 1:
            print("First Rolled Item:", rolls[0])  # Outputs single/1st number in array.
        rolls.remove(min(rolls))  # Removes the lowest number in array.
        if debug == 1:
            print("Removed Lowest.\nFull Array list of Rolls:", rolls)  # Output array('i', [2, 3, 4])
        SumNum = sum(rolls)  # Sums the roll array into single int.
        y[i] = SumNum  # saves SumNum into Stat array
        i += 1  # Increments so smooth brain me can work through arrays in python.
        if debug == 1:
            print("Sum of current Rolls:", SumNum)  # Shows SumNum as debug assurance.
    if debug == 1:
        print(y)  # Prints full Array Output: array('i', [1, 2, 3, 4, 5, 6])
    print("Stat and Mods are as follows:")  # Sets up actual posted content.
    z = y.tolist()  # Transfer's arrays into lists.
    print(z)  # Print said list.
    q = map(statmod, z)  # Maps Z to modding Definition
    print(list(q))  # Prints said modded list.
    # ========================================
    # For "Do a functional refactor on your cool cam." Use above Map as well for the assignment.
    # ========================================
    if assignment == 1:
        filtered = filter(assgn1, z)
        print("Your good rolls:")
        for s in filtered:
            print(s)
        filtered = filter(assgn3, z)
        print("Your average rolls:")
        for s in filtered:
            print(s)
        filtered = filter(assgn2, z)
        print("Your bad rolls:")
        for s in filtered:
            print(s)
        # There should be an easier way to do this, but for simplicity, I did it three times to make sure all rolls are
        # accounted for.
    # ========================================
    #
    # ========================================
    # End of File

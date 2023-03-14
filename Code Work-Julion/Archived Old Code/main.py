# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import random
import array


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class SetStat:
    def __init__(self, str, dex, con, int, wis, cha):
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha

    def show(self):
        print("Stats are show as the following:" + str(self.str) + str(self.dex) + str(self.con) + str(self.int) + str(
            self.wis) + str(self.cha))


# dont use above for coding, it was only for testing


def generate():
    rolls = []
    for rolls in range(4):
        x = random.randint(1, 6)
        rolls.__add__(x)
    del rolls[rolls.index(min(rolls))]
    num = sum(rolls)
    return num


class Stat:
    def __init__(self, num):
        self.num = num


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print(f'this is a test')
    y = SetStat(1, 2, 3, 4, 5, 6)
    y.show()
    i = array.array('d', (0 for d in range(0,5)))
    i[0] = generate()
    i[1] = generate()
    i[2] = generate()
    i[3] = generate()
    i[4] = generate()
    i[5] = generate()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

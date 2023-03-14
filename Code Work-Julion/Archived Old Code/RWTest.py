import math
import random
import array

if __name__ == '__main__':

    test = 3

    try:
        f = open("thing.txt")
        # Test General Reading/Telling.
        if test == 0:
            print(f.read(20))  # Reads 20 characters
            print(f.tell())  # Says what spot its on. Should be 21.
            print("- - - - - - -")  # Separating
            print(f.read())  # If not specified, read to end.
            print(f.tell())  # Should Read final spot.
            print("- - - - - - -")
            f.seek(0)  # Goes to beginning.
            print(f.read())  # Rereading all of it.
            f.seek(0)
        # =======================================================
        #Tests Line by Line Reading, Replacing.
        if test == 1:
            print("==NEW TESTING==\n==LINE BY LINE==")
            for line in f:
                print(line, end='')
            f.seek(0)
            print("\n")
            # =======================================================
            print("==NEW TESTING==\n==Grab and Put Rewrite==")
            g = open("write.txt", "w")  # THIS WILL REPLACE FILE CONTENT IN THERE.
            fLine = f.readline()
            g.write(fLine)
            g.close()
            g = open("write.txt")
            print(g.read())
            f.seek(0)
        # =======================================================
        # Test Line Reading, Amending.
        if test == 2:
            print("==NEW TESTING==\n==Grab and Put Append==")
            g = open("write2.txt", "a")  # THIS WILL ADD ON I BELIEVE
            fLine = f.readline()
            g.write(fLine)  # Will Append to a new line bellow.
            g.close()
            g = open("write2.txt")
            print(g.read())
            f.seek(0)
            g.close(0)
        # =======================================================
        # Line Splitting & Counting
        if test == 3:
            Counter = 0
            Content = f.read()
            ConList = Content.split("\n")
            for i in ConList:
                if i:
                    Counter += 1
            print("ConList: ")
            print(ConList)  # Shows the separated Lines.
            point = ConList[Counter]
            print("Final Line of "+str(Counter+1)+":")  # Shows int to string capability.
            print(point)
            print("Counter: ")
            print(Counter+1)  # Counter will show 3, meaning 0,1,2,3 . . . +1 Shows amount of lines.

    finally:
        f.close()

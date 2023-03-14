import pathlib

def opentest(filename, type):
    if not filename:
        return "No File Given."
    if not type:
        return "No Type Given."
    if not isstring(filename):
        return "Filename Not A String!"
    if type == "race":
        if racerollertry(filename):
            return "Race File Found!"
        else:
            return "Race File NOT Found!"
    if type == "class":
        if classrollertry(filename):
            return "Class File Found!"
        else:
            return "Class File NOT Found!"
    if type == "bg":
        if bgrollertry(filename):
            return "BG File Found!"
        else:
            return "BG File NOT Found!"
    if (type != "bg") and (type != "class") and (type != "race"):
        return "ENTERED WRONG TYPE, Try again!"

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


def classrollertry(ClassChoosen):
    while True:
        classtest = ClassChoosen
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


if __name__ == '__main__':
    assert opentest("Dwarf","race")     == "Race File Found!"
    assert opentest("Mimic", "race")    == "Race File NOT Found!"
    assert opentest("fighter","class")  == "Class File Found!"
    assert opentest("Jester", "class")  == "Class File NOT Found!"
    assert opentest("criminal", "bg")   == "BG File Found!"
    assert opentest("memelord","bg")    == "BG File NOT Found!"
    assert opentest("","class")         == "No File Given."
    assert opentest("fighter","")       == "No Type Given."
    assert opentest("fighter","help me")== "ENTERED WRONG TYPE, Try again!"
    assert opentest(15,"class")         == "Filename Not A String!"
    assert opentest("whatever",90082)   == "ENTERED WRONG TYPE, Try again!"
    #======================================================================
    # Testing TRUE AND FALSE situations in these. The 'Not's have no matching file with that name.
    # ======================================================================
    assert racerollertry("Dwarf")
    assert not racerollertry("Mimic")
    assert classrollertry("fighter")
    assert not classrollertry("Supreme God Lord")
    assert bgrollertry("criminal")
    assert not bgrollertry("Programmer")
    # ======================================================================
    assert isstring("This is a string.")
    assert not isstring("123123")
    assert not isstring(123123)
    # ======================================================================
    print("All statements above should be done correctly. Bellow statements in code should FAIL.")
    Failtest = opentest("Fail","Fail")
    assert Failtest == False, \
        f"Its not False!! Its {Failtest}"
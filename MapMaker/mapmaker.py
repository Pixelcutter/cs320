import pygame
import sys
import random
from math import *
from textwrap import fill

pygame.init()

screen = pygame.display.set_mode([1500, 800]) #sets screen size

random.seed(None) #initializes random number generator, with a seed of the current system date

#have 2028 tiles.
WATERTOTAL = random.randrange(200, 1500) #min of about 10% water, to a maximum of about 75%
RUNBEFORE = False
FILEBUFFER = 51

clock = pygame.time.Clock()
baseFont = pygame.font.Font(None, 20)
userInput = ''
pygame.display.set_caption('Map Maker - V 0.1')

#color definitions
BLACK = (00,00,00)
WHITE = (255,255,255)
RED = (255, 139, 148) #extra color if needed
GREEN = (120, 201, 113) #grass
MOREGREEN = (59, 128, 54) #forest
BLUE = (101, 114, 247) #water
TANCOLOR = (201, 200, 113) #deserts
WHITECOLOR = (253, 243, 236) #tundra
TANCOLORTWO = (196, 127, 35) #beach
PINK = (255, 170, 165) #background
GREY = (115, 122, 133) #color
BLUECOLOR = (32, 85, 168)

#font definitions
titleFont = pygame.font.Font(None, 40)
otherFont = pygame.font.Font(None, 25)

#define locations for where the text will be going for hex info.
textTitleBox = (1500/2-80, 570)

textLocBox = (10, 600)
textLocBoxResponse = (10, 615)
textBiomeBox = (10, 640)
textBiomeBoxResponse = (10, 655)
textTOneBox = (1500/2-300, 600)
textTOneBoxResponse = (1500/2-300, 615)
textTTwoBox = (1500/2-300, 640)
textTTwoBoxResponse = (1500/2-300, 655)
textTThreeBox = (1500/2-300, 680)
textTThreeBoxResponse = (1500/2-300, 695)
textTFourBox = (1500/2, 600)
textTFourBoxResponse =  (1500/2, 615)
textTFiveBox = (1500/2, 640)
textTFiveBoxResponse = (1500/2, 655)
textTSixBox = (1500/2, 680)
textTSixBoxResponse = (1500/2, 695)
textDescBox = (10, 700)
textDescBoxResponse = (10, 715)
textDescBoxResponseTwo = (10, 730)
textDescBoxResponseThree = (10, 745)
exitButton = (1200, 570, 100, 50)
refreshButton = (1200, 630, 100, 50)
exitButtonText = (1220, 582)
refreshButtonText = (1200, 642)

#define the text that is static and unchanging
textTitle = titleFont.render('Info Pane', True, BLACK, None)
textLoc = otherFont.render('Location', True, BLACK, None)
textBiome = otherFont.render('Biome', True, BLACK, None)
textTOne = otherFont.render('Trait One:', True, BLACK, None)
textTTwo = otherFont.render('Trait Two:', True, BLACK, None)
textTThree = otherFont.render('Trait Three:', True, BLACK, None)
textTFour = otherFont.render('Trait Four:', True, BLACK, None)
textTFive = otherFont.render('Trait Five:', True, BLACK, None)
textTSix = otherFont.render('Trait Six:', True, BLACK, None)
textDesc = otherFont.render('Description', True, BLACK, None)
textExit = titleFont.render('Exit', True, BLACK, None)
textRefresh = titleFont.render('Restart', True, BLACK, None)

active = True #declares that the program is actively running
trigger = False
map = []

class HexBox: #this is the hex boxes which compose the map
    def __init__(self, radius, x, y):
        self.x = x
        self.y = y
        self.xPoint = [0,0,0,0,0,0] #list of the points that make up the hexagon
        self.yPoint = [0,0,0,0,0,0] #list of the points that make up the hexagon
        self.traits = ['','','','','',''] #empty list ready to hold the traits that compose the hex
        self.traitDescription = ''
        self.number = 0 #blank identifier for the number of the hex, assigned when the hex is drawn.
        self.biome = '' #string to hold the biome name
        self.active = False #not current active (clicked on)
        self.color = GREEN #assigns a color for the lines
        self.radius = radius
        self.location = '-'

    def traitAssign(self):
        global WATERTOTAL
        #if water total max isn't reached, this can also be a water tile, so random between 1 - 6 biomes
        biomeNum = random.randrange(100)
        if(WATERTOTAL != 0):
            #this can be a water tile, so it has a 30% chance of being one, until max is reached.
            #Aquatic - 30%
            #Beach - 10%
            #Grassland - 25%
            #Forest - 25%
            #Desert - 5%
            #Tundra - 5%
            if(biomeNum < 31): #aquatic
                self.biome = 'Aquatic'
                self.color = BLUE
                WATERTOTAL = WATERTOTAL - 1
            elif(biomeNum < 41): #Beach
                self.biome = 'Beach'
                self.color = TANCOLORTWO
            elif(biomeNum < 66): #grassland
                self.biome = 'Grassland'
                self.color = GREEN
            elif(biomeNum < 91): #Forest
                self.biome = 'Forest'
                self.color = MOREGREEN
            elif(biomeNum < 96): #Desert
                self.biome = 'Desert'
                self.color = TANCOLOR
            else: #Tundra
                self.biome = 'Tundra'
                self.color = WHITECOLOR
        else: #if water total has been reached, this cannot be a water tile, so random between 1 - 5 biomes
            #Beach - 14%
            #Grassland - 36%
            #Forest - 36%
            #Desert - 7%
            #Tundra - 7%
            if(biomeNum < 15): #Beach
                self.biome = 'Beach'
                self.color = TANCOLORTWO
            elif(biomeNum < 51): #grassland
                self.biome = 'Grassland'
                self.color = GREEN
            elif(biomeNum < 87): #Forest
                self.biome = 'Forest'
                self.color = MOREGREEN
            elif(biomeNum < 94): #Desert
                self.biome = 'Desert'
                self.color = TANCOLOR
            else: #Tundra
                self.biome = 'Tundra'
                self.color = WHITECOLOR

        #now that biome is assigned, we need to read in the biome text file & assign traits
        if(self.biome == 'Aquatic'):
            path = 'AquaticFeatures.txt'
        elif(self.biome == 'Beach'):
            path = 'BeachFeatures.txt'
        elif(self.biome == 'Grassland'):
            path = 'GrasslandFeatures.txt'
        elif(self.biome == 'Forest'):
            path = 'ForestFeatures.txt'
        elif(self.biome == 'Desert'):
            path = 'DesertFeatures.txt'
        else:
            path = 'TundraFeatures.txt'
        if sys.platform == 'Windows':
            path = os.path.join('MapMaker', path)
        file = open(path, 'r')
        content = file.readlines()

        #first 10 lines describe the first 3 traits, use 3 random numbers to pick the traits, ensure they don't match
        firstTrait = random.randrange(8)
        secondTrait = random.randrange(8)
        thirdTrait = random.randrange(8)

        if(secondTrait == firstTrait):
            secondTrait = random.randrange(8)

        if(thirdTrait == firstTrait or thirdTrait == secondTrait):
            thirdTrait = random.randrange(8)

        #First 7 of these have 2 options each
        if(firstTrait > 6):
            string = content[firstTrait]
            string = string[:-1]
            self.traits[0] = string
            i = 0
            searchPhrase = '- ' + string
            for words in content:
                if searchPhrase in words:
                    string = content[(i+1)]
                    string = string[:-1]
                    self.traitDescription += string
                    self.traitDescription += ' '
                i = i + 1
        else:
            flip = random.randrange(1,2)
            list = content[firstTrait].split(',')
            if(flip == 1):
                self.traits[0] = list[0]
                i = 0
                searchPhrase = '- ' + list[0]
                for words in content:
                    if searchPhrase in words:
                        string = content[(i+1)]
                        string = string[:-1]
                        self.traitDescription += string
                        self.traitDescription += ' '
                    i = i + 1

            elif(flip == 2):
                string = list[1]
                self.traits[0] = string[0:len(string)-1:1]
                list[1] = string[0:len(string)-1:1]
                i = 0
                searchPhrase = '- ' + list[1]
                for words in content:
                    if searchPhrase in words:
                        string = content[(i+1)]
                        string = string[:-1]
                        self.traitDescription += string
                        self.traitDescription += ' '
                    i = i + 1

        if(secondTrait > 6):
            string = content[secondTrait]
            string = string[:-1]
            self.traits[1] = string
            i = 0
            searchPhrase = '- ' + string
            for words in content:
                if searchPhrase in words:
                    string = content[(i+1)]
                    string = string[:-1]
                    self.traitDescription += string
                    self.traitDescription += ' '
                i = i + 1
        else:
            flip = random.randrange(1,2)
            list = content[secondTrait].split(',')
            if(flip == 1):
                self.traits[1] = list[0]
                i = 0
                searchPhrase = '- ' + list[0]
                for words in content:
                    if searchPhrase in words:
                        string = content[(i+1)]
                        string = string[:-1]
                        self.traitDescription += string
                        self.traitDescription += ' '
                    i = i + 1
            elif(flip == 2):
                string = list[1]
                self.traits[1] = string[0:len(string)-1:1]
                list[1] = string[0:len(string)-1:1]
                i = 0
                searchPhrase = '- ' + list[1]
                for words in content:
                    if searchPhrase in words:
                        string = content[(i+1)]
                        string = string[:-1]
                        self.traitDescription += string
                        self.traitDescription += ' '
                    i = i + 1

        if(thirdTrait > 6):
            string = content[thirdTrait]
            string = string[:-1]
            self.traits[2] = string
            i = 0
            searchPhrase = '- ' + string
            for words in content:
                if searchPhrase in words:
                    string = content[(i+1)]
                    string = string[:-1]
                    self.traitDescription += string
                    self.traitDescription += ' '
                i = i + 1
        else:
            flip = random.randrange(1,2)
            list = content[thirdTrait].split(',')
            if(flip == 1):
                self.traits[2] = list[0]
                i = 0
                searchPhrase = '- ' + list[0]
                for words in content:
                    if searchPhrase in words:
                        string = content[(i+1)]
                        string = string[:-1]
                        self.traitDescription += string
                        self.traitDescription += ' '
                    i = i + 1
            elif(flip == 2):
                string = list[1]
                self.traits[2] = string[0:len(string)-1:1]
                list[1] = string[0:len(string)-1:1]
                i = 0
                searchPhrase = '- ' + list[1]
                for words in content:
                    if searchPhrase in words:
                        string = content[(i+1)]
                        string = string[:-1]
                        self.traitDescription += string
                        self.traitDescription += ' '
                    i = i + 1

        #13 - 20 describe the next 2
        fourthTrait = random.randrange(10,20)
        fifthTrait = random.randrange(10,20)

        if(fourthTrait == fifthTrait):
            fifthTrait = random.randrange(10,20)

        if(fourthTrait > 16):
            self.traits[3] = 'None'
        else:
            string = content[fourthTrait]
            string = string[:-1]
            self.traits[3] = string
            i = 0
            searchPhrase = '- ' + string
            for words in content:
                if searchPhrase in words:
                    string = content[(i+1)]
                    string = string[:-1]
                    self.traitDescription += string
                    self.traitDescription += ' '
                i = i + 1

        if(fifthTrait > 16):
            self.traits[4] = 'None'
        else:
            string = content[fifthTrait]
            string = string[:-1]
            self.traits[4] = string
            i = 0
            searchPhrase = '- ' + string
            for words in content:
                if searchPhrase in words:
                    string = content[(i+1)]
                    string = string[:-1]
                    self.traitDescription += string
                    self.traitDescription += ' '
                i = i + 1

        #22-28 describe last one
        sixthTrait = random.randrange(19, 40)
        #sixthTrait = 20

        if(sixthTrait > 23):
            self.traits[5] = 'None'
        else:
            string = content[sixthTrait]
            string = string[:-1]
            self.traits[5] = string
            i = 0
            searchPhrase = '- ' + string
            #print(searchPhrase)
            for words in content:
                if searchPhrase in words:
                    string = content[(i+1)]
                    string = string[:-1]
                    self.traitDescription += string
                    self.traitDescription += ' '
                i = i + 1

        file.close()

    def draw(self, screen, x, y, q):
        self.location = q
        for i in range(6): #this draws the colored polygon
            self.xPoint[i] = x + self.radius * cos(2 * pi * i / 6)
            self.yPoint[i] = y + self.radius * sin(2 * pi * i / 6)
        pygame.draw.polygon(screen, self.color, [(self.xPoint[0],self.yPoint[0]),
            (self.xPoint[1],self.yPoint[1]),
            (self.xPoint[2],self.yPoint[2]),
            (self.xPoint[3],self.yPoint[3]),
            (self.xPoint[4],self.yPoint[4]),
            (self.xPoint[5],self.yPoint[5])])
        for i in range(6): #this draws the outline on the polygon
            self.xPoint[i] = x + self.radius * cos(2 * pi * i / 6)
            self.yPoint[i] = y + self.radius * sin(2 * pi * i / 6)
        pygame.draw.polygon(screen, BLACK, [(self.xPoint[0],self.yPoint[0]),
            (self.xPoint[1],self.yPoint[1]),
            (self.xPoint[2],self.yPoint[2]),
            (self.xPoint[3],self.yPoint[3]),
            (self.xPoint[4],self.yPoint[4]),
            (self.xPoint[5],self.yPoint[5])], width = 1)

def mapDraw(width, height, radius): #this runs all the required information to generate the hex map
    #initial width draw
    global map
    c = 1
    r = 1
    q = (c, r)
    x = radius
    y = radius
    for a in range(0, height):
        x = radius
        c = 1
        for i in range(0, width):
            currBox = HexBox(radius, x, y)
            currBox.traitAssign()
            q = (c, r)
            currBox.draw(screen, x, y, str(q))
            map.append(currBox)
            c = c + 2
            x = radius*3 + x
            i = i + 1
        y = (radius*2 + y)-4
        a = a + 2
        r = r + 2

    #have to repeat above code to do the offset hexes
    c = 2
    r = 2
    y = radius*2 - 2
    for a in range(0, height):
        x = radius*2.5
        c = 2
        for i in range(0, (width)):
            currBox = HexBox(radius, x, y)
            currBox.traitAssign()
            q = (c, r)
            currBox.draw(screen, x, y, str(q))
            map.append(currBox)
            c = c + 2
            x = radius*3 + x
            i = i + 1
        y = (radius*2 + y)-4
        a = a + 2
        r = r + 2

def cleanScreen():
    screen.fill(GREY, (10, 615, 600, 26))
    screen.fill(GREY, (10, 655, 600, 26))
    screen.fill(GREY, (1500/2-300, 600, 600, 26))
    screen.fill(GREY, (1500/2-300, 615, 600, 26))
    screen.fill(GREY, (1500/2-300, 655, 600, 26))
    screen.fill(GREY, (1500/2-300, 695, 600, 26))
    screen.fill(GREY, (1500/2, 615, 600, 26))
    screen.fill(GREY, (1500/2, 655, 600, 26))
    screen.fill(GREY, (1500/2, 695, 600, 26))
    screen.fill(GREY, (10, 715, 1490, 26))
    screen.fill(GREY, (10, 730, 1490, 26))
    screen.fill(GREY, (10, 745, 1490, 26))

    pygame.draw.rect(screen, RED, exitButton)
    pygame.draw.rect(screen, RED, refreshButton)
    screen.blit(textExit, exitButtonText)
    screen.blit(textRefresh, refreshButtonText)

#main stuff below here
def main():
    global active
    global map
    global screen
    global WATERTOTAL

    screen.fill(GREY)
    mapDraw(39, 26, 12.5)

    while active: #while the program is running...
        #textBox1 = TextBox(100, 100, 140, 32)
        #textBox2 = TextBox(100, 300, 140, 32)
        #textBoxes = [textBox1, textBox2]
        debug = 100,100

        #now add in all the static text
        screen.blit(textTitle, textTitleBox)
        screen.blit(textLoc, textLocBox)
        screen.blit(textBiome, textBiomeBox)
        screen.blit(textTOne, textTOneBox)
        screen.blit(textTTwo, textTTwoBox)
        screen.blit(textTThree, textTThreeBox)
        screen.blit(textTFour, textTFourBox)
        screen.blit(textTFive, textTFiveBox)
        screen.blit(textTSix, textTSixBox)
        screen.blit(textDesc, textDescBox)
        pygame.draw.rect(screen, RED, exitButton)
        pygame.draw.rect(screen, RED, refreshButton)
        screen.blit(textExit, exitButtonText)
        screen.blit(textRefresh, refreshButtonText)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False

            if event.type == pygame.MOUSEBUTTONUP:
                mousePosX, mousePosY = pygame.mouse.get_pos()
                #(1200, 570, 100, 50)
                #refreshButton = (1200, 630, 100, 50)

                #check if within exit exitButton
                if(mousePosX <= 1300 and mousePosX >= 1200 and mousePosY <= 620 and mousePosY >= 570):
                    active = False

                #check if within refresh Button
                if(mousePosX <= 1300 and mousePosX >= 1200 and mousePosY <= 680 and mousePosY >= 630):
                    map = []
                    WATERTOTAL = random.randrange(200, 1500) #min of about 10% water, to a maximum of about 75%
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #i = 0
                cleanScreen()
                mousePosX, mousePosY = pygame.mouse.get_pos()
                unroundedRow = mousePosY/11
                column = round(mousePosX/18)
                row = round(mousePosY/11)

                #parse the column and row variable to match the way it's parsed in my map

                if(column % 2 == 0 and row % 2 != 0):
                    #The row cannot be odd
                    if(unroundedRow > row):
                        row = row + 1
                    else:
                        row = row - 1
                elif(column % 2 != 0 and row % 2 == 0):
                    #This row cannot be even
                    if(unroundedRow > row):
                        row = row + 1
                    else:
                        row = row - 1


                if column <= 0:
                    column = column + 1
                if row <= 0:
                    row = row + 1

                #print(str(column) + " " + str(row)) #DEBUG
                tester = (column, row)

                for hex in map: #now we've identified that mouse is over a specific hex.
                    #print(hex.location)
                    if(str(tester) == hex.location):
                        pygame.draw.rect(screen, RED, exitButton)
                        pygame.draw.rect(screen, RED, refreshButton)
                        screen.blit(textExit, exitButtonText)
                        screen.blit(textRefresh, refreshButtonText)
                        #render the text
                        #print(str(hex.location))
                        textLocResponse = otherFont.render(hex.location , True, BLUECOLOR, None)
                        textBiomeResponse = otherFont.render(hex.biome, True, BLUECOLOR, None)
                        textTOneResponse = otherFont.render(hex.traits[0] , True, BLUECOLOR, None)
                        textTTwoResponse = otherFont.render(hex.traits[1] , True, BLUECOLOR, None)
                        textTThreeResponse = otherFont.render(hex.traits[2] , True, BLUECOLOR, None)
                        textTFourResponse = otherFont.render(hex.traits[3] , True, BLUECOLOR, None)
                        textTFiveResponse = otherFont.render(hex.traits[4] , True, BLUECOLOR, None)
                        textTSixResponse = otherFont.render(hex.traits[5] , True, BLUECOLOR, None)
                        textDescResponse  = otherFont.render(hex.traitDescription[:150] , True, BLUECOLOR, None)
                        if(len(hex.traitDescription) > 149):
                            textDescResponseTwo = otherFont.render(hex.traitDescription[150:300] , True, BLUECOLOR, None)
                            screen.blit(textDescResponseTwo, textDescBoxResponseTwo)
                        if(len(hex.traitDescription) > 299):
                            textDescResponseThree = otherFont.render(hex.traitDescription[300:450] , True, BLUECOLOR, None)
                            screen.blit(textDescResponseThree, textDescBoxResponseThree)
                        #put the text on screen
                        screen.blit(textLocResponse, textLocBoxResponse)
                        screen.blit(textBiomeResponse, textBiomeBoxResponse)
                        screen.blit(textTOneResponse, textTOneBoxResponse)
                        screen.blit(textTTwoResponse, textTTwoBoxResponse)
                        screen.blit(textTThreeResponse, textTThreeBoxResponse)
                        screen.blit(textTFourResponse, textTFourBoxResponse)
                        screen.blit(textTFiveResponse, textTFiveBoxResponse)
                        screen.blit(textTSixResponse, textTSixBoxResponse)
                        screen.blit(textDescResponse, textDescBoxResponse)
                    else:
                        continue

            #for box in textBoxes:
                #box.handle_event(event)
                #for box in textBoxes:
                    #box.update()
                    #screen.fill((255, 211, 211))
                #for box in textBoxes:
                    #box.draw(screen)
                    #pygame.display.flip()
                    #clock.tick(30)

            #if event.type == pygame.MOUSEBUTTONDOWN:
                #if textBox.collidepoint(event.pos):
                #    active = True
                #else:
                #    active = False

            #if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_BACKSPACE:
            #        userInput = userInput[:-1]
            #    else:
            #        userInput += event.unicode

        #screen.fill((211, 211, 211)) #fills background with a nice grey

        #pygame.draw.rect(screen, color, textBox)
        #textSurface = baseFont.render(userInput, True, (255, 255, 255))

        #screen.blit(textSurface, (textBox.x+5, textBox.y+5))

        #textBox.w = max(100, textSurface.get_width()+10)
        #pygame.display.flip()
        #refreshes screen, to show any updates
        pygame.display.flip()
    pygame.quit()

main()

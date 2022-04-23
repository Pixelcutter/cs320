import pygame
import sys
import random
from math import *

pygame.init()

screen = pygame.display.set_mode([1500, 800]) #sets screen size

random.seed(None) #initializes random number generator, with a seed of the current system date

#have 2028 tiles.
WATERTOTAL = random.randrange(200, 1500) #min of about 10% water, to a maximum of about 75%
RUNBEFORE = False

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
BLUE = (54, 101, 128) #water
TANCOLOR = (201, 200, 113) #deserts
WHITECOLOR = (253, 243, 236) #tundra
TANCOLORTWO = (227, 226, 148) #beach
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
textDescBox = (10, 680)
textDescBoxResponse = (10, 695)

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

active = True #declares that the program is actively running
trigger = False
map = []

class HexBox: #this is the hex boxes which compose the map
    def __init__(self, radius, x, y):
        self.x = x
        self.y = y
        self.xPoint = [0,0,0,0,0,0] #list of the points that make up the hexagon
        self.yPoint = [0,0,0,0,0,0] #list of the points that make up the hexagon
        self.traits = ['TraitOne','TraitTwo','TraitThree','TraitFour','TraitFive','TraitSix'] #empty list ready to hold the traits that compose the hex
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

    #change trait text of this biome


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

#main stuff below here
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            #i = 0
            cleanScreen()
            mousePosX, mousePosY = pygame.mouse.get_pos()

            column = round(mousePosX/18)
            row = round(mousePosY/11)

            #parse the column and row variable to match the way it's parsed in my map

            if(column % 2 == 0 and row % 2 != 0):
                #The row cannot be odd, so minus 1 from row if it doesn't match
                row = row - 1
            elif(column % 2 != 0 and row % 2 == 0):
                #This row can only be odd, so minus 1 from row if it doesn't match
                row = row - 1

            if column <= 0:
                column = column + 1
            if row <= 0:
                row = row + 1

            print(str(column) + " " + str(row)) #DEBUG
            tester = (column, row)

            for hex in map: #now we've identified that mouse is over a specific hex.
                #print(hex.location)
                if(str(tester) == hex.location):
                    #render the text
                    print(str(hex.location))
                    textLocResponse = otherFont.render(hex.location , True, BLUECOLOR, None)
                    textBiomeResponse = otherFont.render(hex.biome, True, BLUECOLOR, None)
                    textTOneResponse = otherFont.render(hex.traits[0] , True, BLUECOLOR, None)
                    textTTwoResponse = otherFont.render(hex.traits[1] , True, BLUECOLOR, None)
                    textTThreeResponse = otherFont.render(hex.traits[2] , True, BLUECOLOR, None)
                    textTFourResponse = otherFont.render(hex.traits[3] , True, BLUECOLOR, None)
                    textTFiveResponse = otherFont.render(hex.traits[4] , True, BLUECOLOR, None)
                    textTSixResponse = otherFont.render(hex.traits[5] , True, BLUECOLOR, None)
                    textDescResponse  = otherFont.render('-' , True, BLUECOLOR, None)

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

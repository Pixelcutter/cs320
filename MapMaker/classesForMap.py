#class TextBox:
#    def __init__(self, x, y, w, h, text=''):
#        self.Rect = pygame.Rect(x, y, w, h)
#        self.color = PASSIVECOLOR
#        self.text = text
#        self.textSurface = baseFont.render(text, True, (255, 255, 255))
#        self.active = False
#
#    def handle_event(self, event):
#        if event.type == pygame.MOUSEBUTTONDOWN:
#            if self.Rect.collidepoint(event.pos):
#                self.active = True
#            else:
#                self.active = False
#            self.color = ACTIVECOLOR if self.active else PASSIVECOLOR
#
#        if event.type == pygame.KEYDOWN:
#                if self.active:
#                    if event.key == pygame.K_BACKSPACE:
#                        self.text = self.text[:-1]
#                    else:
#                        self.text += event.unicode
#                    # Re-render the text.
#                    self.textSurface = baseFont.render(self.text, True, self.color)
#
#    def update(self):
#        self.w = max(100, self.textSurface.get_width()+10)
#
#    def draw(self, screen):
#        screen.blit(self.textSurface, (self.Rect.x+5, self.Rect.y+5)) #Update the text
#        pygame.draw.rect(screen, self.color, self.Rect, 2) #Update the rect

class HexBox:
    def __init__(self, radius, x, y):
        self.x = x
        self.y = y
        self.xPoint = [0,0,0,0,0,0]
        self.yPoint = [0,0,0,0,0,0]
        self.traits = ['','','','','','']
        self.number = 0
        #self.biome = class for biome call here
        self.active = False
        self.color = pygame.Color('chartreuse4')

#    def handle_event(self, event):
#        if event.type == pygame.MOUSEBUTTONDOWN:
#            if self.polygon.collidepoint(event.pos):
#                self.active = True
#            else:
#                self.active = False

    def draw(self, screen, x, y):
        for i in range(6):
            self.xPoint[i] = x + radius * cos(2 * pi * i / 6)
            self.yPoint[i] = y + radius * sin(2 * pi * i / 6)
        pygame.draw.polygon(surface, color, [(xPoint[0],yPoint[0]),
            (xPoint[1],yPoint[1]),
            (xPoint[2],yPoint[2]),
            (xPoint[3],yPoint[3]),
            (xPoint[4],yPoint[4]),
            (xPoint[5],yPoint[5])], width = 1)

    #def assignTraits():
        #there's nothing here yet

#class Map:
#    def __init__(self, width, height):
#        self.tiles = []
#        self.waterAmount = 0
#        self.width = width
#        self.height = height
#        self.seed = randint(100000,999999)

#    def drawMap(self, radius):
#        random.seed(self.seed) #set the random seed to match the map's seed.
#
#        x = radius
#        y = radius
#        for a in range(0, height):
#            x = radius
#            for i in range(0, width):
#                #new HexBox(radius, x, y)??
#                x = radius*3 + x
#                i = i + 1
#            y = (radius*2 + y)-4
#            a = a + 2
        #self.tiles[a] = the hex returned?
        #have to repeat above code to do the offset hexes
#        y = radius*2 - 2
#        for a in range(0, height):
#            x = radius*2.5
#            for i in range(0, (width-1)):
#                #call hex class here
#                x = radius*3 + x
#                i = i + 1
#            y = (radius*2 + y)-4
#            a = a + 2

class Biome:
    def __init__(self):
        self.biomeName = ''
        self.traits = ['','','','','','']

    def assignTraits(self):
        fileName = filePicker(self)
        if fileName == "E":
            error = True
            #handle the error (maybe quit?)
        textFile = open(fileName, "r") #open appropriate textfile
        content = textFile.readlines() #now read in the file so I handle the traits by line.
        #now parse the file and assign traits.

        fileName.close() #close the file now that I'm done with it.

    #def filePicker(biomeName): #this returns the text file as a string to the assignTraits function
        #switcher ={
            #"Grassland": "GrasslandFeatures.txt"
            #"Tundra": "TundraFeatures.txt"
            #"Aquatic": "AquaticFeatures.txt"
            #"Beach": "BeachFeatures.txt"
            #"Forest": "ForestFeatures.txt"
        #}
        #return switcher.get(self.biomeName, "E")

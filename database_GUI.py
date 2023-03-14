import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import itemCMD as icmd
import gui.Classes.gui_classes as gc

pygame.init()
pygame.display.init()
pygame.font.init()

# python does NOT support constants, but these will be defined here for the idea of constants
# Window size - maybe should depend on screen resolution?
WIN_WIDTH = 900
WIN_HEIGHT = 600

# To keep boxes uniform stored here
BOX_WIDTH = int(WIN_WIDTH * .15)
BOX_HEIGHT = int(WIN_HEIGHT * .05)
# Frames per Second - we likely won't even need this many for a GUI. Consider downscaling
FPS = 30

DEFAULT_FONT = 32

WIDTH_SPACER = 12
HEIGHT_SPACER = 10

# rename the window
pygame.display.set_caption("D&D Cool Cam")

# Colors that will be used, so I don't have to reference the RGB value every time
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (175, 175, 175)

# create the window var
MAIN_WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

COLOR_INACTIVE = BLACK
COLOR_ACTIVE = WHITE


"""
This is where Peter database GUI would be.
I am not versed enough in python to know if I can access his database information,
    Peter does everything from `if __name__ == '__main__'` which to me, means that I can't
    access anything under that function, because as an module that gets imported, I am not __main__
    Need to request Peter to make a main() function, or otherwise I need to learn Python better.
    
I will do the work of building the initial window, but it doesn't do any calls to his actual database

All set up is needed in this instance of lore_GUI, main_GUI, and this program (database_GUI), as they are all meant to be
    stand alone GUI's if wanted, and every new instance of pygame needs to have all initializations and window building
    as pygame doesn't even support multiple windows currently - 4/29
"""
def main():
    items = icmd.itemDB()
    items.updateList()

    # Cannot access Peters functions for now. See above

    clock = pygame.time.Clock()
    main_window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    text = 'not implemented yet!'
    w, h = pygame.font.Font(None, DEFAULT_FONT).size(text)
    not_implemented = gc.TextBox((WIN_WIDTH/2) - (w/2), (WIN_HEIGHT/2) - h, w, h, text, False, DEFAULT_FONT, BLACK, WHITE)

    run = True
    while run:

        main_window.fill(LIGHT_GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # update should always be last (other than clock tick)
        not_implemented.draw(main_window)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()

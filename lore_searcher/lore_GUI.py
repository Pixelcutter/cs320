import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
from classes.LoreSearcher import Searcher

# from lore_searcher.classes.LorePage import Page

# look, is it what I want to do? Change my python PATH? No
# is it what I need to do? Probably also no
# But here I go doing it.
path_to_add = os.path.abspath('..') + '/'
sys.path.append(path_to_add)
import gui.Classes.gui_classes as gc

sys.path.remove(path_to_add)

pygame.init()
pygame.display.init()
pygame.font.init()

# python does NOT support constants, but these will be defined here for the idea of constants
# Window size - maybe should depend on screen resolution?
WIN_WIDTH = 900
WIN_HEIGHT = 600

# To keep boxes uniform stored here
# Might be moved inside main(), shouldn't ever change, so I treat it as a macro, but since math is done,
#   maybe it should not be a global
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

COLOR_INACTIVE = BLACK
COLOR_ACTIVE = WHITE

"""
lore_GUI is a completely different GUI than what I worked on originally. It is very bare bones as time was a factor,
    but as a proof of concept, I think it works well! The button in the bottom left of the corner should scroll
    through entries, though only the first entry is shown right now.
    
    Text wrapping also proved to be an issue. Pygame has an 'easy' way to do this, but more work is needed to see
    how that text is split and sent. Jared also showed me to a python module that may do this as well, but as of now,
    the 'blurbs' is omitted until that can be figured out.
    
All Globals are repasted here. This is not to inflate lines, this is is just naturally how building a standalone GUI
    should probably go. There's no reason that the size of the window of main_GUI should the same size as this window
    inits need to happen every time pygame is started as this is an entirely new session of pygame pygame.init, 
    display.init, and font.init() are needed in every instance.
"""


def main():
    clock = pygame.time.Clock()
    path = os.path.join("data", "index")
    searcher = Searcher(path)
    if len(sys.argv) < 2:
        print("Error, not enough arguments sent. Are you sure you sent something?")
        exit(1)

    results = searcher.search(sys.argv[1])
    """
    for result in results['results']:
        result.getPage()
    """

    # x = WIN_WIDTH/2
    # y = WIN_HEIGHT/2
    # text = "TESTING"
    # w, h = pygame.font.Font(None, DEFAULT_FONT).size(text)
    # box = gc.TextBox(x, y, w, h, 'text', False, DEFAULT_FONT)

    data = []

    if results['results'] is None:
        print('String not found in the database!')
        exit(0)

    for result in results['results']:
        data.append(result.getSummary())
        # result.printSummary()

    main_window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # SHOW IN THIS ORDER
    # id
    # name
    # blurb
    # topic
    # url

    # blurb missing for demo. Need to recursively find where to wrap the text box. I just dont have time rn

    tags_ordered = ['id', 'name', 'topics', 'url']

    next_button_pressed = True
    cur_box_index = 0
    y_height = 20

    all_boxes = []

    font_size = DEFAULT_FONT

    text = 'next entry '
    w, h = pygame.font.Font(None, DEFAULT_FONT).size(text)
    next_button = gc.Button((WIN_WIDTH - w - 20), (WIN_HEIGHT - h - 20), w, h, text)

    assert next_button_pressed,  'Error, please ensure next_button_pressed = True to start'

    run = True
    while run:

        main_window.fill(WHITE)

        if next_button_pressed:
            all_boxes = []
            # need to change out the values of the boxes
            for tag in tags_ordered:
                info = data[cur_box_index][tag]
                info = ' '.join(info)
                text_field = tag + ': ' + info

                w, h = pygame.font.Font(None, font_size).size(text_field)
                if w > WIN_WIDTH:
                    font_size = 25
                    w, h = pygame.font.Font(None, font_size).size(text_field)
                x = 25
                if tag == 'url':
                    info = info.replace(' ', '')
                    text_field = tag + ': ' + info
                    cur_box = gc.WebButton(x, y_height, w, h, text_field, info)
                else:
                    cur_box = gc.TextBox(x, y_height, w, h, text_field, False, font_size)

                all_boxes.append(cur_box)
                y_height += h + (WIN_HEIGHT / (len(tags_ordered) * 1.5))
                font_size = DEFAULT_FONT

            cur_box_index += 1

            text = 'Page Number ' + str(cur_box_index) + ' of ' + str(results['total-results']) + ' '
            w, h = pygame.font.Font(None, font_size).size(text)
            page_num_box = gc.TextBox((WIN_WIDTH / 2) - (w / 2), WIN_HEIGHT - 75, w, h, text)

            # revert the flag
            next_button_pressed = False

        for event in pygame.event.get():
            # IDE gives an error, but this should be guaranteed to be true. I will add an assert for now I suppose.
            if next_button.handle_event(event):
                # next_button_pressed = True
                print('Can only print the first entry currently')
                pass
            for box in all_boxes:
                box.handle_event(event)

            if event.type == pygame.QUIT:
                run = False

        next_button.draw(main_window)

        for box in all_boxes:
            box.draw(main_window)

        page_num_box.draw(main_window)

        # update should always be last (other than clock tick)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

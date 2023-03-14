import pygame
import os
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
SAND = (215, 208, 94)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 120, 0)
PINK = (255, 0, 255)
CYAN = (0, 255, 255)

# Import background image
BACKGROUND_LARGE = pygame.image.load(
    os.path.join('gui', 'Assets/desert.jpg'))
BACKGROUND_SCALED = pygame.transform.scale(
    BACKGROUND_LARGE, (WIN_WIDTH, WIN_HEIGHT))

COLOR_INACTIVE = BLACK
COLOR_ACTIVE = WHITE


"""
ACTUAL METHODS START HERE
They appear in order that the windows appear in. All of the classes can be found in gui/Classes/gui_classes.py
All of these Windows are similar, but pygame doesn't allow us to have more than one window open at a time natively
A workout around can be done in main_window, where a system call is made to pygame to make a new version entirely.
These windows were designed to be standalone and as such error checking for init is done on all of them. I regularly
bypassed everything but the main_window.

Opening Window only calls text boxes. It makes the background black, otherwise you would see the boxes.
No work was done to make text without boxes, classes were attempted to be used as needed.

There are a lot of magic numbers in here. In the future it's possible this could be a dynamically sized window,
But I would need to be more comfortable with pygame and GUI's in general. For the most part, this reinvents the wheel.
There are programs that exist already where you don't have to do that, but this was good practice.
"""
def opening_window():
    if not pygame.display.get_init():
        pygame.display.init()

    # Opening Window closes itself a set period of time, I have it set to 4 seconds.
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(BLACK)
    run = True

    all_boxes = []

    # Box doesn't size to fit text, so we have to plug in magic numbers to format
    # there is a magic "random" number at the end here to better center. Not precise.
    # Later, I started using pygame.font.Font().size() to make the boxes better fit text
    # This seems inefficient. We could get where we wanted the text centered on, but I could never
    # guarantee that's how I wanted it formatted. I just use that function many times.
    x = (WIN_WIDTH / 2) - (BOX_WIDTH / 2) - 25
    y = BOX_HEIGHT
    welcome_box = gc.TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, "Welcome!", False, 52)
    all_boxes.append(welcome_box)

    # magic number based on how long the text is, not the size of the box really
    x = (WIN_WIDTH / 2) - (BOX_WIDTH / 2) - 200
    y = BOX_HEIGHT * 3
    cool_cam_intro = gc.TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, "To Dungeons, Dragons, and Code", False, 52)
    all_boxes.append(cool_cam_intro)

    x = (WIN_WIDTH / 2) - (BOX_WIDTH / 2)
    y = WIN_HEIGHT - (BOX_HEIGHT * 8)
    credits_box = gc.TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, "Credits", False, 52)
    all_boxes.append(credits_box)

    our_names = []
    # ALPHABETICAL BY LAST NAME - list used even though I could inflate. That just sucks though.
    # Jared Diamond
    # Garett Loghry
    # Julion Oddy
    # Levicy Radeleff
    # Peter Wanner
    names = ["Jared Diamond,", "Garett Loghry,", "Julion Oddy,", "Levicy Radeleff,", "Peter Wanner"]
    y = WIN_HEIGHT - (BOX_HEIGHT * 6)
    x = 30

    for name in names:
        cur_person = gc.TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, name, False, DEFAULT_FONT)
        x += cur_person.box.outer_rect.width
        our_names.append(cur_person)
        all_boxes.append(cur_person)

    timer = 0

    while run:
        for event in pygame.event.get():
            for box in all_boxes:
                box.handle_event(event)         # Boxes don't handle any events right now, but they may handle url clicks in the future
            if event.type == pygame.QUIT:
                run = False

        for box in all_boxes:
            box.txt_surface = box.font.render(box.text, True, WHITE)        # manually change the color of the box
            box.draw(screen)

        # update should always be last (other than clock tick)
        pygame.display.update()
        clock.tick(FPS)

        # Check to see if it's been more than 4 seconds
        if timer > 4:
            # Close this window if > than timer
            run = False
        else:
            # increment timer and wait 1 second
            pygame.time.wait(1000)
            timer += 1


"""
main, sometimes referred to (on accident) as 'main window' is where a bulk of the work takes place
It creates text boxes on the left, and buttons to my peers cool cams on the right

TEXT BOXES:
    Text boxes use the 'TextBox' class found in gui/Classes/gui_classes.py
    They are pre-filled with 6 different categories that can either be entered manually (have to click the box)
        or by pressing the 'Generate Character ' button on the left.
    Names are pretty self explanatory, they pull from a variety of different sources since Julion and I both worked
        on this section. We can get: Name, Race, Gender, Class, Quirk, and Background
        Name, Gender, and Quirk are exclusively mine and can be found in gui/Names and gui/Quirks respectively.
        Gender is just a function. At some point it was thought to have non binary, but this doesn't fit with how names
        are generated.
    Names are based on BOTH Race and Gender and text files can be found according in the gui/Names dir
    There is a 1:4 chance that your character could get a title. Titles include things like 'the mad'. Only a small amount
    was added.
    All fields populate and are still editable after clicking on 'Generate Character'.
    
BUTTONS:
    Buttons (usually) use the 'Button' class found in gui/Classes/gui/classes.py
        There is a variant called WebButton that is used to take you to a website, but I think this is only used in
        my GUI used for Jared's cool cam (lore searcher).
    'Search for lore here! ' Button is a linker to Jared's cool cam (lore searcher). This could have been really cool
        if Jared and I didn't procrastinate quite so much. There were a lot of ideas for this, but currently my button
        opens a new instance of pygame. I have to rebuild a new window from scratch, pygame doesn't support multiple
        windows. While I was happy for the extra lines, there was really no way I could think to avoid this. It also
        means that you can run my GUI for his cool cam (called lore_GUI.py found in lore_searcher/) by its self.
        Though be warned that you must give an argument in the command line. Only basic error checking is done on
        the argument.
        
        Issues with lore_GUI can be found in it's file, of which there are more than I'd like to admit.
    'Generate Character ' is mostly Julion's cool cam (random character generator), though it only utilizes a small portion of it. In the future
        I would want the GUI to show more accurately his cool cam. He takes in to consideration levels,
        and does 're-rolls' to get stats again. My boxes don't implement stats, and are more for just ideas. I would
        like to open a entirely new window for Julion, but time didn't allow for this.
    'Generate Map ' is all Levicy's cool cam. I think it's fair to say she worked the most consistently of all of us
        on her cool cam, and I think it really shows. She did a great job. All my GUI does is do system calls to open
        her GUI. There was an issue with file ingestion issues between Linux and Windows that I had to solve, but
        They are assumed to be solved. I don't have a windows machine to boot usually, and for the sake of this project
        it seems to work well enough. She also used pygame, but none of the GUI in that section was written by me.
    'Open Database ' is probably the thing I wish I had the most time to work on. I feel really bad that Peter and I
        weren't able to collaborate more and get this working, but this feature has not been implemented yet. If more time
        my GUI would send and receive values for the amount of things in the database, if it's found, or other stats.
        My GUI doesn't even attempt a system call at current standpoint, the button does nothing.
"""
def main():
    if not pygame.display.get_init():
        pygame.display.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # Window is filled in case the image cannot/will not load. I don't want WHTIE or BLACK or RED or whatever default is
    screen.fill(SAND)

    # My things are on the left, buttons to other cool cams are on the right. Buttons are blue, boxes typically black
    # NEED TO ACCOUNT FOR A BARE MINIMUM OF:
    # NAME                          1
    # RACE                          2
    # GENDER                        3
    # CLASS                         4
    # QUIRKS                        5
    # BACKGROUND                    6
    #   SUB BACKGROUND - OCCUPATION 7 ?
    x = margin = WIN_HEIGHT / 10
    height_offset = int(WIN_HEIGHT - margin)
    # width_offset = WIN_WIDTH - margin
    y = increment = int(height_offset / 7)

    input_boxes = []
    # occupation not used yet/ever
    box_texts = ['Name: ', 'Race: ', 'Gender: ', 'Class: ', 'Quirk: ', 'Background: ']  # , 'Occupation: ']

    for text in box_texts:
        input_box = gc.TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, text, True, DEFAULT_FONT)
        y += increment
        input_boxes.append(input_box)

    """
    input_boxes[0].text = 'Name'
    input_boxes[1].text = 'Race'
    input_boxes[2].text = 'Gender'
    input_boxes[3].text = 'Class'
    input_boxes[4].text = 'Quirks'
    input_boxes[5].text = 'Background'
    input_boxes[6].text = 'Occupation'
    """

    # buttons link to other cool cams (not peters right now)
    # Buttons are (typically) blue, indicating they can be clicked on
    buttons = []
    button_text_list = ['Generate Character ', 'Generate Map ', 'Open Database ']
    last_button_height = 0
    # There are lots of things like this 'spacer'. I wish I had a better way to store a buffer/margin/spacer
    y_spacer = 15

    # manually find the size of the font, so we can move it away from the edge of the screen
    for string in button_text_list:
        w, h = pygame.font.Font(None, DEFAULT_FONT).size(string)
        w, h = (w + WIDTH_SPACER), (h + HEIGHT_SPACER)
        button = gc.Button(WIN_WIDTH - w - 30, (WIN_HEIGHT / 2) + last_button_height, w, h, string, DEFAULT_FONT)
        buttons.append(button)
        last_button_height += h + y_spacer

    # Search bar is in the top right (idk it just felt right?) and is handled separately
    w, h = pygame.font.Font(None, DEFAULT_FONT).size('Search for lore here! ')
    search_box = gc.SearchBox(WIN_WIDTH - w - margin, margin, w, h)

    run = True
    while run:
        # need to blint the window, it's actually an image
        screen.blit(BACKGROUND_SCALED, (0, 0))
        for event in pygame.event.get():
            for box in input_boxes:
                box.handle_event(event)
                box.update(screen)
            for button in buttons:
                ret = button.handle_event(event)
                if ret is not None:
                    for i in range(len(input_boxes)):
                        input_boxes[i].text = box_texts[i] + ret[i]
                        input_boxes[i].update(screen)
            search_box.handle_event(event)

            if event.type == pygame.QUIT:
                run = False

        for box in input_boxes:
            box.draw(screen)
        for button in buttons:
            button.draw(screen)
        search_box.draw(screen)

        # update should always be last (other than clock tick)
        pygame.display.update()
        clock.tick(FPS)


"""
Closing Window just displays the link to our cool cams github. The Repo is fully public, though depending on others
projects, I can only guarantee my code source will free always. It is a group project after all.
"""
def closing_window():
    if not pygame.display.get_init():
        pygame.display.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    screen.fill(BLACK)
    run = True

    all_boxes = []

    goodbye = 'Link to our github: '
    w, h = pygame.font.Font(None, 52).size(goodbye)
    x = (WIN_WIDTH / 2) - (w / 2)
    y = (WIN_HEIGHT / 4)
    goodbye_box = gc.TextBox(x, y, w, h, goodbye, False, 52)
    all_boxes.append(goodbye_box)

    link = 'https://github.com/gloghry/cs320/tree/master '
    w, h = pygame.font.Font(None, 52).size(link)
    x = (WIN_WIDTH / 2) - (w / 2)
    y += h + 10
    link_box = gc.TextBox(x, y, w, h, link, False, 52)
    all_boxes.append(link_box)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for box in all_boxes:
            box.txt_surface = box.font.render(box.text, True, WHITE)
            box.draw(screen)

        # update should always be last (other than clock tick)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    opening_window()
    main()
    closing_window()

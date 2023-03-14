import pygame
import os
import random
import webbrowser

pygame.init()
pygame.display.init()
pygame.font.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

COLOR_INACTIVE = BLACK
COLOR_ACTIVE = WHITE

WIDTH_SPACER = 12
HEIGHT_SPACER = 10

DEFAULT_FONT = 32


"""
SearchBox is the link to Jared cool cam (lore_searcher). He scrapes website(s) and creates an index of that information
    My GUI uses a search bar to send strings into his cool cam. We check to see if it exists and any information
    in the lore_GUI.py
    
Takes minimal arguments. No way to change text color or box color.
x position (top), y position (left), width, height, and text
    text is default built for one button, since this is more a one and done button.
    
SearchBox will adjust it's own width and height to fit the text given (default if none supplied)
    Static box sizes were an issue for me for a long time. x and y are only calculated in the top left accordingly.
    Ergo you will need to do the math ahead of time if you want x and y in a specfic spot.
    
SearchBox clears its own text after the first click, but maintaines it's size. The box does not grow to fit long entires,
    But I believe even long strings can be sent to lore_searcher even if they're out of bounds. 
    
I chose to make Search Blue to show that you could interact with it, and that it takes you to Jared's cool cam. It's not
    a button however, this is the rare exception.
"""
class SearchBox:
    def __init__(self, x, y, w, h, text='Search for lore here! '):
        if w < 0 or h < 0:
            raise ValueError("Not a valid window size!")
        self.x_pos = x
        self.y_pos = y

        self.color = BLUE
        self.color_text = WHITE
        self.active = False

        self.text = text
        self.font = pygame.font.Font(None, DEFAULT_FONT)
        self.txt_surface = self.font.render(text, True, self.color_text)
        w, h = self.font.size(self.text)
        self.first_click = True

        self.box = BorderedBox(x, y, (w + WIDTH_SPACER), (h + HEIGHT_SPACER), self.color, WHITE)

    """
    handle_event takes notice to mouse clicks and key entries.
        Interestingly, it doesn't like the RETURN on a num pad a a K_RETURN
        In the future it would be nice if that RETURN was accounted for and
        Delete. Currently we don't check for deletes, only backspaces
    """
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box.handle_event(event):
                self.active = not self.active
                if self.first_click:
                    self.text = ''
                    self.first_click = False
                return True
            else:
                self.active = False
                return False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    print("Running the search function")
                    os.system("cd lore_searcher; python3 lore_GUI.py " + self.text)
                else:
                    self.text += event.unicode
                return True

        self.txt_surface = self.font.render(self.text, True, self.color_text)

    def draw(self, screen):
        # Background of the box
        self.box.draw(screen)
        # Transparent box, would like to fill, but need the reverse color

        # Text formatted inside the box
        screen.blit(self.txt_surface, (self.x_pos + 5, self.y_pos + 5))

"""
TextBox was designed to be a one size fits all for boxes, but this quickly turned out to not work.
    From needing to handle specific types (like the search bar) to becoming so general that it's __init__
    is 120 characters long. I should have done more research on how other general interfaces do it, but
    looking at something like Swing for Java felt counter productive since Java is so verbose anyway.
    
TextBox will adjust it's own width and height if a string is supplied to the 'text' field as the same with
    SearchBox. TextBoxes are black by default with white text.
    
Work was done to make TextBox have a border. It does this by using another custom class, BorderBox. Found below.
    TextBox manages the work for BorderBox, and BorderBox is very bare bones.
"""
class TextBox:
    def __init__(self, x, y, w, h, text='', editable=False, font_size=DEFAULT_FONT, color=COLOR_INACTIVE, text_color=WHITE):
        if w < 0 or h < 0:
            raise ValueError("Not a valid window size!")
        self.x_pos = x
        self.y_pos = y

        self.color = color
        self.color_text = text_color

        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, self.color_text)

        self.active = False
        self.editable = editable

        if not text == '':
            w, h = self.font.size(self.text)
            # definitely some magic numbers below. The font.size needs to have extra padding to fit the box.
            # this is what I found works the best.
            self.box = BorderedBox(x, y, (w + WIDTH_SPACER), (h + HEIGHT_SPACER))
        else:
            self.box = BorderedBox(x, y, w, h)

    """
    TextBox looks to see if it is active. If it isn't, any events are ignored other than to set it to active.
    If this box is active, it adjusts the box based on user input.
    The box can be updated to fit new strings set to the text field of TextBox with .update()
    """
    def handle_event(self, event):
        if self.editable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # box is part of the BorderBox class. Returns a bool
                if self.box.handle_event(event):
                    self.active = not self.active
                else:
                    self.active = False
                # return True
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    # return True
            self.txt_surface = self.font.render(self.text, True, self.color_text)

    """
    Update is typically used when something fills the TextBox other than itself. This mainly happens with the use of
    'Generate Character ' Button. It will rescale the box to fit around the new string, and redraws the box for you.
    It lets BorderBox.update() handle the outer and inner boxes.
    """
    def update(self, screen):
        # If update has been called, there should be text in the box now
        if self.text == '':
            raise ValueError('Error, text box is too small')
        w, h = self.font.size(self.text)
        self.box.update(self.x_pos, self.y_pos, (w + WIDTH_SPACER), (h + HEIGHT_SPACER))

        self.box.draw(screen)
        self.draw(screen)

    """
    TextBox really only handles the blit, it throws the draw boxes to the BorderBox class, since it
    has an inner and outer box.
    """
    def draw(self, screen):
        # Background of the box
        self.box.draw(screen)
        # Transparent box, would like to fill, but need the reverse color

        # Text formatted inside the box
        screen.blit(self.txt_surface, (self.x_pos + 5, self.y_pos + 5))


"""
BorderBox is meant to be used with TextBox. It takes a given x, y, w, h and makes TWO boxes.
    The first one is filled to the background_color (defaults to black) and the second one is a rectangle that borders
    the first box. The border is set to the same color as the background color, only appearing when the box is clicked
    on (default white). Since no text is handled in this class it is really just two rectangles acting as a pair.
"""
class BorderedBox:
    def __init__(self, x, y, w, h, background_color=COLOR_INACTIVE, border_color=COLOR_ACTIVE):
        self.inner_rect = pygame.Rect(x, y, w, h)
        self.outer_rect = pygame.Rect(x, y, w, h)
        self.active = False
        self.inner_color = background_color
        self.outer_color = background_color
        self.border_color = border_color

    """
    Even though both rectangles should occupy the same space, I was always worried about collision issues. We check
    both the inner box and the outer box for a collision. A bool is returned (T/F) of whether the click happened
    within it's bounds.
    """
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.inner_rect.collidepoint(event.pos) or self.outer_rect.collidepoint(event.pos):
                collision = True
                self.active = not self.active
            else:
                collision = False
                self.active = False
            # Change the current color of the input box.
            if self.active:
                self.outer_color = self.border_color
            else:
                self.outer_color = self.inner_color

            return collision

    def draw(self, screen):
        pygame.draw.rect(screen, self.inner_color, self.inner_rect, 0)
        pygame.draw.rect(screen, self.outer_color, self.outer_rect, 2)

    """
    if we update the TextBox, we need to update both the inner and outer boxes as well.
    Probably self does not need to be returned, but it doesn't break anything right now.    
    """
    def update(self, x, y, w, h):
        self.inner_rect = pygame.Rect(x, y, w, h)
        self.outer_rect = pygame.Rect(x, y, w, h)
        return self

"""
Button class makes a clickable button. Currently we check for very specific button values within the class itself.
    This seems not great and likely violates a whole host of SOLID principles, but for my small GUI, it works okay.
    
Buttons have a counterpart, WebButton which specifically handle clicks that take us to a url. This is done because
The url must be stored as well as the title of the button, and adding 'url' to a default button seems terrible.
"""
class Button:
    def __init__(self, x, y, w, h, text='', font_size=DEFAULT_FONT):
        if w < 0 or h < 0:
            raise ValueError("Not a valid window size!")
        self.text = text
        self.font_size = font_size
        self.color = BLUE
        self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, WHITE)
        if not text == '':
            w, h = self.font.size(self.text)
            self.rect = pygame.Rect(x, y, (w + WIDTH_SPACER), (h + HEIGHT_SPACER))
        else:
            self.rect = pygame.Rect(x, y, w, h)

    """
    We look for specific buttons and their title. I'm sure this is... not good, but for the sake of my sanity it is
    being used either way.
    
    The return statements here are not actually needed on the GUI, it handles just fine without them #NOTE
        #NOTE other than 'next entry ' we look to see if that's a real button and return true on collision
        
        They are really useful for unittestting though, and can be used to test functionality
        
    In the future inheritance should be used, but hard coded was easier for the few buttons I had.
    """
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.text == 'Generate Map ':
                    print("Opening and running Map Maker")
                    # os.system use C for system calls. You can run multiple commands with ;
                    os.system("cd MapMaker; python3 mapmaker.py")
                elif self.text == 'Generate Character ':
                    print('Loading files....')
                    return generate_new_character()
                elif self.text == 'Search ':
                    # Search has its own SearchBox now
                    return False
                elif self.text == 'next entry ':
                    return True
                elif self.text == 'Open Database ':
                    # Sadge
                    os.system('python3 database_GUI.py')
                else:
                    # ???
                    print("That button isn't recognized...")
                    return None

    def draw(self, screen):
        # Background of the box
        # Width (last tuple value) 0 = fill
        pygame.draw.rect(screen, self.color, self.rect, 0)
        # Transparent box, would like to fill, but need the reverse color

        # Text formatted inside the box
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

"""
Welcome to the World Wide Net kid.
WebButton opens a web browser when you click on the button on the screen. It may open your default browser? I didn't do
    much checking into it once it worked. This is used wtih Jared's cool cam (lore_searcher) to click on web links.
    
WebButton is very similar to Button, but we still need to use the Button class. Python doesn't
    > extend < or > implement <  in the same way as Java so this is what worked for what I did.
"""
class WebButton:
    def __init__(self, x, y, w, h, text='', url=None, font_size=DEFAULT_FONT):
        if w < 0 or h < 0:
            raise ValueError("Not a valid window size!")
        self.color = BLUE

        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, WHITE)
        self.url = url
        if not text == '':
            w, h = self.font.size(self.text)
            self.rect = pygame.Rect(x, y, (w + WIDTH_SPACER), (h + HEIGHT_SPACER))
        else:
            self.rect = pygame.Rect(x, y, w, h)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.url is not None:
                    print('click!')
                    webbrowser.open(self.url)
                    return True
                else:
                    # Not sure if valid link checking is needed
                    print("Could not open link :( ")
                    return False

    def draw(self, screen):
        # Background of the box
        # Width (last tuple value) 0 = fill
        pygame.draw.rect(screen, self.color, self.rect, 0)
        # Transparent box, would like to fill, but need the reverse color

        # Text formatted inside the box
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

"""
Everything done below this point is used with the
'Generate Character ' Button. It is a list of functions and system calls that look at files and do some random int work
    on the lines of those files. Return order matters quite a lot here.
    _class is sent because the keyword class is taken
"""
def generate_new_character():
    gender = generate_gender()
    race = generate_race()
    name = generate_name(race, gender)
    _class = generate_class()
    background = generate_background()
    quirk = generate_quirk()

    # print(name, race, gender, _class, background, quirk)

    return name, race, gender, _class, quirk, background


def generate_gender():
    _gender = random.randint(1, 2)  # Range should be increased to 3 for NB
    if _gender == 2:
        gender = 'Male'
    elif _gender == 1:
        gender = 'Female'
    else:
        gender = 'NB'
        # Used for error checking right now, could be used for NB in the future
        # files not implemented for NB
    return gender


def generate_race():
    race_path = os.path.join('Code Work-Julion', 'CharDatabase', 'Race', '$List.txt')
    try:
        with open(race_path, 'r+') as race_file:
            all_races = race_file.readlines()  # store the entire file in mem (should be small)
            count = len(all_races)  # line count
            race = all_races[(random.randint(1, count) - 1)].rsplit('\n', 1)[0]  # get one of the random lines
            if 'Human' in race:  # Remove whether standard or variant human subtype
                race = 'Human'
    except FileNotFoundError:
        print("Race file moved, deleted, or otherwise changed. Check position")
        race = 'ERR'
    return race


def generate_name(race, gender):
    if race == 'ERR' or race is None or gender is None: return "ERR"

    if random.randint(1, 4) == 1:
        use_title = True
    else:
        use_title = False

    name_filename = '' + str(race) + '_' + str(gender) + '.txt'
    name_path = os.path.join('gui', 'Names', name_filename)
    try:
        with open(name_path, 'r+') as name_file:
            all_names = name_file.readlines()  # store the entire file in mem. I won't have more than maybe 15 names per file
            count = len(all_names)
            name = all_names[(random.randint(1, count) - 1)].rsplit('\n', 1)[0]
    except FileNotFoundError:
        name = "Boaty McBoatface"

    if use_title:
        title_path = os.path.join('gui', 'Titles', 'Titles')
        try:
            with open(title_path, 'r+') as title_file:
                all_titles = title_file.readlines()
                count = len(all_titles)
                title = all_titles[(random.randint(1, count) - 1)].rsplit('\n', 1)[0]
                name += " " + title
        except FileNotFoundError:
            print("Titles file moved, or otherwise unreadable")

    return name


def generate_class():
    _class_path = os.path.join('Code Work-Julion', 'CharDatabase', 'Class', '$List.txt')
    try:
        with open(_class_path, 'r+') as _class_file:
            all_classes = _class_file.readlines()  # store the entire file in mem (should be small)
            count = len(all_classes)  # line count
            _class = all_classes[(random.randint(1, count) - 1)].rsplit('\n', 1)[0]  # get one of the random lines
    except FileNotFoundError:
        print("Class file moved, deleted, or otherwise changed. Check position")
        _class = 'ERR'

    return _class


def generate_background():
    background_path = os.path.join('Code Work-Julion', 'CharDatabase', 'Background', '$List.txt')
    try:
        with open(background_path, 'r+') as background_file:
            all_backgrounds = background_file.readlines()  # store the entire file in mem (should be small)
            count = len(all_backgrounds)  # line count
            background = all_backgrounds[(random.randint(1, count) - 1)].rsplit('\n', 1)[
                0]  # get one of the random lines
    except FileNotFoundError:
        print("Class file moved, deleted, or otherwise changed. Check position")
        background = 'ERR'

    return background


def generate_quirk():
    quirk_path = os.path.join('gui', 'Quirks', 'Quirks.txt')
    try:
        with open(quirk_path, 'r+') as quirk_file:
            all_quirks = quirk_file.readlines()  # store the entire file in mem (should be small)
            count = len(all_quirks)  # line count
            quirk = all_quirks[(random.randint(1, count) - 1)].rsplit('\n', 1)[0]  # get one of the random lines
    except FileNotFoundError:
        print("Class file moved, deleted, or otherwise changed. Check position")
        quirk = 'You stare into the void... Often...'

    return quirk

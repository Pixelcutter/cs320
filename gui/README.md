# Summary
This project is part of WSU's CS320 course given during the spring of 2022. 
This was a group project, you can find all credits and implementations of every one else's cool cam there. 
This directory is exclusively used by Garett Loghry as part of the multiple GUI's that are built as part of the project.  
All code in this directory and lower is guaranteed to be written by Garett Loghry.

# The GUI
My portion of this code to write and display was the GUI. The master GUI, `main_GUI.py` may open 
    multiple instances of pygame. This is normal and to be expected. Pygame in its current implementation, 
    2.1.2, does not support the use of multiple windows.  

This means I must start and handle all my own windows. 
    As such, when some buttons are pressed on within the `main_GUI.py`, it has the possibility of opening a few 
    instances of pygame. Two are GUI's by me, `lore_GUI.py` and `database_GUI.py`. It should be noted 
    That very little work was done to `database_GUI.py` and is more of a place holder as of now.  

Another instance of pygame should start when you press `Generate Map`. This was *not* written by me, it was written 
    by another team member Levicy Radeleff. My GUI just calls it thorugh the `sys` supplied by python. 

# Other Projects
My project implements my other team members projects. Below you can find a list of their projects

### Map Creation - Levicy Radeleff
Levicy's cool cam is making a map for DM's to use. It's randomly generated and pulls 
    from a whole list of requirements and specifications. My project just calls her program.  

Levicy also uses pygame. As a game editor, it was a somewhat lower level approach to doing rendering. 
    It's not as low as OpenGL, but it's much lower than Unity.

### Random Character Generator - Julion Oddy
Julion's cool cam is a randomly generated character. Originally we both wanted to do this project, 
    but julion had already done one version of it and wanted to expand on his work. This meant 
    that I was looking for a cool cam. It was decided that I would try to link all the other cool cams! 

I think this worked well, Julion and I worked the most closely of the group in my opinion. 
    Julion and I worked well together, and we were the two main people who advocated for meeting as a group.  

I wish I was able to select a character and make a specific GUI for Julion as well. We hadn't communicated 
    doing this, but it would be nice for everyone to have their own window in my opinion.


### Web Scraper and Indexer - Jared Diamond
Jared's cool cam was to implement an information retrieval program that scrapes a website, 
    I believe it was Fandom.com, and creates an index of the information within that website. 
    It can then be retrieved by his program, and he does work to display it.  

My GUI works with his `seacher()`. It is assumed that the information has already been retrieved. 
    Only one page is displayed, unfortunately. Jared and I collaborated too late to effectively link our cool cams.  

There is an important section called 'blurbs' that my GUI omits. This is omitted because of text wrapping. 
    By in large, I can assume most incoming data will not be longer than the length of the window. 
    If text *does* go past the window, the text should wrap itself. This was never implemented.

### Database System - Peter Wanner
Peter's cool cam was to create, maintain, and manage a database. This was quite an undertaking and with 
    Peter's busy schedule and my procrastination, we weren't able to flesh out a GUI for his cool cam.  

We did a little bit of work to make his database ingestable by my GUI, but this is a future 
    implementation. Given more time I would like to have all the GUI's work, and feel better, 
    but Peter's is the one I would work on most immediately. 


# Credits
**Owner:** Garett Loghry  
**Contact:** garett.loghry@wsu.edu  
**Disclaimer:** I do not own in full this repository. It is a group project, and is such no guarantees are made to 
        whether code works, or if code will be maintained. All portions of my code will be free, always.  

# Notes
* This is really a proof of concept. While it may be useful for someone, somewhere, this is just code writen by 
    students looking to learn. 
* My main GUI `main_GUI.py` found in the parent directory to this one, is the master GUI for this project
* `main_GUI.py` could open multiple instances of pygame. This is normal. All projects GUI's were intended 
  to stand alone and work by themselves. 
* I, Garett Loghry, did *not* write the map maker GUI. That was designed and written by Levicy (see above)
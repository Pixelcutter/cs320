# Lore Builder 
##### _A D&D (Forgotten Realms) Lore Search Engine and Inspiration Tool_  
 
Lore Builder consists of two main parts: the **Lorebook** and the **Search Engine**. The goal of Lore Builder is to give users an easy way to search for relevant D&D information for their characters, and then save their search results to personalized sections. In filling their Lorebook with lore found through the search engine, it is my hope that users may gain inspiration when coming up with their next character or campaign.  

## The Lorebook
***
The Lorebook is the where all of the characters attribute information is stored, and where all saved search pages are stored. It consists of three main parts:
- Lore Master: Holds character attribute information, meta information, and Lore Sections. Its class can be found in `classes/LoreMaster.py`.
- Lore Section: Holds Lore Pages and meta information for the section. Its class can be found in `classes/LoreSection.py`.
- Lore Page: Holds all information of a search result returned from the Lore Search Engine. Its class can be found in `classes/LorePage.py`.

#### Lorebook Structure
```
Lore Master
    |- Character Attributes
    |- Lore Sections
           |- Lore Pages
    
```
## The Search Engine
***
The Lore Search Engine takes a user query and then returns results in the form of Lore Pages related to the query. There are currently 5054 documents available for the user to search through. All searchable data came from the [Forgotten Realms Fandom Wiki](https://forgottenrealms.fandom.com/wiki/Main_Page). The search engine class can be found in `classes/LoreSearcher.py`. It is dependent on the [Whoosh](https://whoosh.readthedocs.io/en/latest/index.html) search engine python library. 
## Running Lore Builder From Terminal
***
If you do not want to import the lore builder classes into your own project, you can simply run the py file lore_builder.py and start an interactive session with the lorebook and search engine. After completing the setup prompts, you will be able to
start searching and building your lorebook. lore_builder.py includes an auto-save feature just in case a problem occurs when running the program. 
> **Auto-Save Note:** All session data will be auto-saved to a tmp.lore file located in the lore_files directory. The tmp.lore file will be deleted on a successful ```save``` or ```lore_save``` command, and added again whenever your lorebooks state changes.

#### Preparing Your Python Environment
To successfully run lore_builder.py, you will need the Whoosh search engine library. To Install it, and start a Lore Builder session, run the following commands:  

___Creating Virtual Environment and Installing Dependencies___
```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
___Starting Lore Builder Session___
```bash
python3 lore_builder.py
```

## Lore Builder Session Commands
***
There are quite a few commands available during a lore_builder.py session. The most useful would be `search`, `add_section`, `add_page`, `print_lore`, `edit`, and `save`. **All commands and their arguments should be seperated by commas**.

#### Command Line Options                                                                                                   
    lore_builder.py -l <path/to/file.lore>  Loads found lore file to new session                                                        
    lore_builder.py -c <path/to/char.txt>   Loads randomly generated character file to new session                                                                                                                                
#### Session Commands                                                                                                       
    edit_lore | edit, <field>, <new_value>  Changes field to new value                                                  
    load_lore | load, <path/to/file.lore>   Loads character/campaign from file (CURRENT SESSION LOST)                   
    save_lore | save                        Saves current session to name.lore file (Json format)                       
    pretty_save | psave                     Saves current session to name.txt file in print_lore format                 
    clear | clr                             Clears console                                                              
    help | h                                Prints command list
    q | quit                                Quits current session                                                         
                                                                                                                        
#### Section Commands                                                                                                       
    add_section | mks, <section_name>           Creates a new section titled 'section_name'                             
    del_section | rms, <section_name>           Removes section and all section pages                                   
    list_section | ls, <section_name>           Lists the pages present in section                                      
    print_section | ps, <section_name>          Prints page summaries for section pages                                 
    add_page | mkp, <section_name>, <page_id>   Adds page associated with id to section                                 
    del_page | rmp, <section_name>, <page_id>   Removes page associated with id from section                            
    list_all | la                               Lists all sections and their pages                                      
                                                                                                                        
#### Page Commands                                                                                                          
    print_page | pp, <page_id>  Prints full page to console                                                             
                                                                                                                        
#### Search Commands                                                                                                        
    search | s, <search_terms>  Searches index and prints summaries of relevant pages found
    
## Example Pretty Save
***

The following output comes from a randomly generated character named Charlie that has one Lore Section containing two Lore Pages. Charlie was generated from Julion's Cool Cam, and was imported into lore_builder with the following command:
```bash
$ python3 lore_builder.py -c data/Charlie.txt
```
Once two pages were added to Charlie's inspiration section, Charlie decided to "Pretty Save" his current lore ideas with the following command:
```bash
> pretty_save
```
> **Note:** Charlie could have also entered ```psave``` to pretty save

### Pretty Save File Contents
```
                         <{{  Character: Charlie  }}>
                          
Class: Fighter (Battle Master)
Race: Hill Dwarf
Sex: 
Origin: 

Criminal: You have access to a contact/liaison to get connected to other
criminals. Specifically, you know the local messengers, corrupt caravan masters,
and seedy travelers. You are considered 1 of these: Blackmailers, Burglar,
Enforcer, Fence, Highway Robber, Hired Killer, Pickpocket, Smuggler


Section: Inspiration
---------------------
********************************************************************************

                         Venturer%27S Rest (id: 3636)
                          

Topics Included: structure, interior, atmosphere, services, history
Description: From the exterior, the inn appeared as hole-in-the-wall
establishment of little acclaim. It was tucked away in an unremarkable corner of
the city, built into...

Source-URL: https://forgottenrealms.fandom.com/wiki/Venturer%27s_Rest
Img-URL: https://static.wikia.nocookie.net/forgottenrealms/images/b/ba/Old_Dirty
_Dwarf_Ext.png/revision/latest/scale-to-width-down/350?cb=20210205165036

********************************************************************************
********************************************************************************

                      Grand Army Of The Tuigan (id: 1092)
                      

Topics Included: organization, activities, tactics, base of operations
Description: Formed mostly of horsemen, Yamun Khahan's army was fast, efficient,
and lethal. The army was organized as follows:  Yamun Kahan's army numbered over
300,000 ...

Source-URL: https://forgottenrealms.fandom.com/wiki/Grand_Army_of_the_Tuigan
Img-URL: default.png

********************************************************************************
```
## A Note About the Lore Builder Classes
***
The LoreMaster, LoreSection, and LorePage classes have a print method and a get method. Use the print methods when planning to make a terminal application, and the get methods when planning to capture Lore components in dictionary form and enter their contents into a GUI, Website, etc.
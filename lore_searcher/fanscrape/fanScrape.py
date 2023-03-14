import requests
import re
from bs4 import BeautifulSoup as bs
import json
from time import sleep
import random

# loading target dictionary
with open("data/targets.json", "r") as fd:
    targetDB = json.load(fd)

# Dumps master dictionary into file: data/pages.json
def dumpDict(masterDict):
    with open("data/pages.json", "w+") as fd:
        json.dump(masterDict, fd, indent = 4)

# Grabs table of contents found on most pages. Returned list is used to grab
# pages contents
def getToC(source):

    # if page does not contain a table of contents, return None, signified
    # by attribute error
    try:
        items = source.find(class_='toc').find_all('li')
    except AttributeError:
        return None

    toc = list(map(lambda item: item.find(class_ = 'toctext').text, items))
    
    # if 'Appendix' in toc: delete it, and every toc item after it
    # else: return None
    if 'Appendix' in toc:
        del toc[toc.index('Appendix'): ]
    else:
        return None

    return toc

# Strips all sub strings that resemble '[n]'
def stripSrcNum(string):
    return re.sub(r"\[\d+\]", "", string).strip()

# Grab image url found in right side table of page.
# It's not garaunteed that a page will have an image url present
# or even a right side table present
def getImg(source):
    link = ""
    try:
        link = source.aside.img.get('src')
    except:
        link = "default.png"

    return link

# Grabs list that was found between headers (toc topics)
def getList(ul):
    newList = list(map(lambda x: stripSrcNum(x.text), ul.find_all('li')))
    
    return newList

# Grabs paragraphs and lists found between headers
def getContent(source, target, nextTarget):
    plist = source.find_all('p')
    tmp = source.find('span', id = target.replace(' ', '_')).find_parent()
    cur = tmp.next_sibling
    end = source.find('span', id = nextTarget.replace(' ', '_')).find_parent()
    
    paras = []
    lists = []

    while cur and cur != end:
        if cur not in plist:
            # unordered list found, grab its contents and then continue
            # looking for paragraphs
            if cur.name == 'ul':
                lists.append(getList(cur))

            cur = cur.next_sibling
            continue
        text = cur.text.strip()
        if len(text):
                paras.append(stripSrcNum(text))
        cur = cur.next_sibling

    return {'paras': '\n\n'.join(paras) if len(paras) else None,
            'lists': lists if len(lists) else None}

# Grabs first descriptive paragraph found on page... sometimes
def getBlurb(source, target):
    cur = source.b
    
    # this traversal hinges on the first instance of <b>target</b>
    # being in the summary paragraph of a page. It's not garaunteed
    # this will always be the case since these are wiki pages and
    # formatting guidelines are loose
    try:
        targetBFound =  bool(re.search(rf"[.*]?{target}", cur.text, re.IGNORECASE))
        while targetBFound != True and cur.text.lower() != target.lower():
            cur = cur.find_next('b')
            targetBFound =  bool(re.search(rf"[.*]?{target}", cur.text, re.IGNORECASE))
    except AttributeError:
        return None

    return stripSrcNum(cur.find_parent().text)

# Grabs a pages contents and then returns a json object
def getPage(src, target, url):
    pageDict = {}
    soup = bs(src, 'html.parser')
    toc = getToC(soup)

    if toc == None or len(toc) == 0:
        return None

    pageDict['topic-name'] = target
    pageDict['source-url'] = url
    pageDict['img-url'] = getImg(soup)
    pageDict['blurb'] = getBlurb(soup, target)
    pageDict['toc'] = list(map(lambda x: x.lower(), toc))

    # grab content (paragraphs and lists) from each toc topic
    # and store it in page dictionary as 'topic':'content'
    i = 0
    for subject in toc[0:len(toc)-1]:
        pageDict[subject.lower()] = getContent(soup, toc[i], toc[i + 1]) 
        i += 1

    # last topic is taken care of outside of loop
    pageDict[toc[-1].lower()] = getContent(soup, toc[-1], 'Appendix')

    return pageDict

def main():
    pagesCollected = 0
    totalTargets = targetDB['total']
    targetList = targetDB['targets']

    masterDict = {'total-pages': 0, 'pages': []}
    
    for target in targetList:
        url = "https://forgottenrealms.fandom.com/wiki/" + target
        page = requests.get(url)

        print(f"Grabbing: {target}")
        # if page exists and it has table of contents: add new page to master
        # dictionary, else: continue
        if page.status_code == 200:
            newPage = getPage(page.text, target.replace('_', ' '), url)
            if newPage:
                masterDict['pages'].append(newPage)
            else:
                print(f"SKIPPING {target}!")
                continue
        else:
            print(f"SKIPPING {target}!")
            continue

        pagesCollected += 1
        masterDict['total-pages'] += 1
        print(f"Page Collected: {target}\nPage Count: {pagesCollected}/{totalTargets}\n")

        dumpDict(masterDict)
        # letting the wiki servers relax a little
        sleep(random.randint(1,3))

main()

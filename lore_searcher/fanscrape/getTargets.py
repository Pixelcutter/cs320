import requests
import random
from bs4 import BeautifulSoup as bs
import re
from time import sleep
import json

random.seed()

targetDict = {'total': 0, 'targets': []}

categoryList = ["Locations_in_", "Inhabitants_of_", "Organizations_in_",
                "Settlements_in_", "Events_in_", "Food_and_drink_from_",
                "Items_from_"]

regionList = ["Faerûn", "Kara-Tur", "Maztica", "Zakhara", "Laerakond"]

# cleans up targetDict's target list, updates total entry count and 
# then dumps its contents into a file (targets2.json in this case)
# targets.json is used by fanscrape.py to grab pages
def dumpDict():
    targetDict['targets'] = list(set(targetDict['targets']))
    targetDict['total'] = len(targetDict['targets'])
    with open("data/targets.json", "w+") as fd:
        json.dump(targetDict, fd, indent = 4)

# will return true if all list entries are already in targetDict['targets']
def listAcountedFor(tmpList):
    for item in tmpList:
        if item not in targetDict['targets']:
            return False

    return True

# Looks for links present on a category page and then returns a list
# containing all links found
def getLinks(srcPage):
    linkList = []
    soup = bs(srcPage.text, 'html.parser')
    divs = soup.find_all(class_ = 'category-page__members-wrapper')
    for div in divs:
        ul = div.find('ul')
        linkList.extend(list(map(lambda x: x.get('href').replace('/wiki/', ''), ul.find_all('a'))))

    lastLink = linkList[-1]
    return {'linkList': linkList, 'lastLink': linkList[-1]}

def main():
    lastLink = ""
    lastList = []
    fromHere = "?from="
    baseURL = "https://forgottenrealms.fandom.com/wiki/Category:"

    # this loop attempts to crawl through all entries for
    # a category + region combo. It is far from perfect, as
    # some items are skipped due to how the wiki alphabetizes
    # its entries.
    for region in regionList:
        for category in categoryList:
            url = baseURL + category + region + fromHere + lastLink
            page = requests.get(url)
            if page.status_code != 200:
                print(f"page: {url} not found")
                continue
           
            linkListMeta = getLinks(page)
            lastList = linkListMeta['linkList']

            while len(lastList) > 1:
                targetDict['targets'].extend(lastList)
                lastLink = linkListMeta['lastLink'].replace('_', '+')
                url = baseURL + category + region + fromHere + lastLink

                print(f"\nGrabbing {url}...")
                page = requests.get(url)
                linkListMeta = getLinks(page)
                lastList = linkListMeta['linkList']
                print("success")

                # this check ends up skipping some entries.
                # need to find a different way of checking
                if listAcountedFor(lastList):
                    dumpDict()
                    break
                
                # sleeping to reduce load on server
                sleep(random.randint(1,3))
                dumpDict()

            lastLink = "" 

main()

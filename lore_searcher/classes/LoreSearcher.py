from .LorePage import Page
import os.path
import json
from math import ceil
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser as mfp
from whoosh.qparser import OrGroup
from whoosh.qparser import QueryParser
from whoosh.fields import *


""" Searcher serves as the inspiration for any Lorebook. Searcher
utilizes the Whoosh search engine library to search over an indexed
database of scraped D&D webpages. There a couple methods available
to Searcher:

- indexDB(dataPath: str)
- searchID(pageID: int)
- search(userQuery: str, pageNum: int, limit: int, searchType: str)

You can read about these methods below
"""

class Searcher(object):

    # Initializes Searcher
    # str ixPath: path to Whoosh index
    # str dataPath: path to database file

    def __init__(self, ixPath, dataPath=None):
        self.ix = getIX(ixPath)
        if dataPath != None:
            self.indexDB(dataPath)

    # Adds json database to Woosh index (self.ix)
    # str dataPath: path to json database

    def indexDB(self, dataPath):
        writer = self.ix.writer()

        with open(dataPath, 'r') as fd:
            data = json.load(fd)

        # Indexing all pages found in database

        for page in data['pages']:
            doc = getDoc(page)
            writer.add_document(
                id=str(page['id']),
                title=page['topic-name'],
                docText=doc[0],
                blurb=doc[1].split('<>')[5],
                toc=getToc(page['toc']),
                link=page['source-url'],
                img=page['img-url'],
                _stored_docText=doc[1]
            )

        # commit additions to whoosh database
        writer.commit()

    # Searches index for a document with id equal to pageID
    # int pageID: id of desired document
    # returns Page: LorePage initialized with found docs contents

    def searchID(self, pageID):
        with self.ix.searcher() as searcher:
            result = searcher.document(id=str(pageID))
            if result == None:
                return None
            return Page(result['docText'])

    
    # The main method of LoreSearcher. Searches Whoosh index for documents
    # that contain query search terms and then returns what it found
    # str userQuery: user query with search terms
    # int pageNum: desired page of results to return
    # int limit: amount of results Whoosh searcher will return
    # str searchType: how inclusive Whoosh searcher is
    # returns dict: dict object containing search results and search meta data
   
    def search(self, userQuery, pageNum=1, limit=10, searchType="AND"):
        resultDict = {"query": userQuery, "results": []}

        # Conjunctive search if searchType == AND
        # Disjunctive search if searchType == OR
        # Both search types search over multiple indexed fields:
        # title, document text, and document blurb 

        with self.ix.searcher() as searcher:
            if searchType == "AND":
                parser = mfp(['title', 'docText', 'blurb'],
                             schema=self.ix.schema)
            else:
                parser = mfp(['title', 'docText', 'blurb'], schema=self.ix.schema,
                             group=OrGroup)

            # parse query and search the database
            query = parser.parse(userQuery.strip())
            results = searcher.search_page(
                query, pagenum=pageNum, pagelen=limit, terms=True)

            # total number of relevant docs in database
            numResults = len(results)

            # no results found, suggest a different query and then return
            # {"results": None, "corrected": "corrected_query"}
            if numResults == 0:
                corrected = searcher.correct_query(query, userQuery).string
                resultDict['results'] = None
                resultDict['corrected'] = corrected
                return resultDict

            # for every result returned, append a LorePage object containing all
            # indexed/stored (according to schema) data to resultDict['results']
            for result in results:
                termHits = list(
                    map(lambda x: x[1].decode(), result.matched_terms()))
                resultDict['results'].append(Page(result['docText'], termHits))

            resultDict['total-results'] = numResults
            # total pages available for search query (keeping same limit)
            resultDict['total-pages'] = ceil(numResults/limit)
            # how many results were returned
            resultDict['topN'] = len(resultDict['results'])

        # succesful search, return results and all meta data

        return resultDict


# Returns a Whoosh index object. If no index database is found at ixPath,
# it will create one and then return it.
# str ixPath: path to Whoosh index
# returns Index: Whoosh index object

def getIX(ixPath):
    if not os.path.exists(ixPath):
        os.mkdir(ixPath)
        ix = create_in(ixPath, getSchema())
    else:
        ix = open_dir(ixPath)

    return ix

# Returns a json databases page table of contents field as a single string
# This string will be stored with indexed document
# toc str: list of strings

def getToc(toc):
    if toc == None or len(toc) == 0:
        return None
    else:
        return ', '.join(list(map(lambda x: x, toc)))

# Helper function that returns the first paragraph found on page. 
# Used if no blurb was found on page
# dict page: json database page object

def firstPara(page):
    for topic in page['toc']:
        if page[topic]['paras']:
            return page[topic]['paras']
    return ""

# Helper function that creates custom string that represents the json document
# This custom string will be stored in the index.
# dict page: dict representation of a page found in json database
# returns str: custom formatted string

def getDoc(page):
    rawDoc = "" # string indexed over
    doc = ""    # custom string thats stored with indexed doc

    if 'toc' not in page or page['toc'] == None:
        return None

    doc += str(page['id']) + "<>"  # page id
    doc += page['topic-name'] + "<>"  # page name
    doc += page['source-url'] + "<>"  # src url
    doc += page['img-url'] + "<>"  # image url
    doc += ','.join(page['toc']) + "<>"  # table of contents
    doc += firstPara(page) + "<>"  # blurb

    # adding topics from page to custom string

    for topic in page['toc']:
        rawDoc += topic + ' '
        doc += topic + '<NAME>'
        paras = page[topic]['paras']
        lists = page[topic]['lists']

        if paras:
            doc += paras + '<PARAS>'
            rawDoc += paras + ' '
        if lists:
            for list in lists:
                for li in list:
                    doc += li + '<LI>'
                    rawDoc += li + ' '
                doc += '<LIST>'
        doc += '<TOPIC>'
    return (rawDoc, doc)

# Helper function that returns Whoosh schema object

def getSchema():
    schema = Schema(
        id=ID(stored=True),
        title=TEXT(stored=True,
                   field_boost=2.0,
                   analyzer=None),
        docText=TEXT(stored=True),
        blurb=TEXT(stored=True),
        toc=STORED,
        link=STORED,
        img=STORED)

    return schema

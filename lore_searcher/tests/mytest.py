import unittest
import requests
from bs4 import BeautifulSoup as bs
from ../searcher import * 
from ../misc/fanScrape import * 

# searcher.py tests
class testSearch(unittest.TestCase):

	# acceptence test
	def test_getToc(self):
		li = ['hello', 'world']
		result = getToc(li)
		self.assertEqual(result, 'hello, world')
	
	# acceptence test
	def test_getToc_None(self):
		li = None
		result = getToc(li)
		self.assertEqual(result, None)

	# acceptance test
	def test_firstPara(self):
		testpara = "hello<NAME>correct para\nnot correct\nnot correct\n<PARAS><TOPIC>world<NAME>not correct<PARAS><TOPIC>"
		result = firstPara(testpara)
		self.assertEqual(result, "correct para")

	# acceptance test
	def test_firstPara_None(self):
		testpara = "hello world"
		result = firstPara(testpara)
		self.assertIsNone(result)

	# getDoc() method being white-box tested:
	"""
	returns a tuple containing all text on page. First element of tuple contains
	raw text, second element contains custom formatted/seperated text for easy
	parsing later

	def getDoc(page):
	    rawDoc = ""
	    doc = ""
	
	    if 'toc' not in page or page['toc'] == None:
	        return None
	
	    for topic in page['toc']:
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
	"""

	# acceptence test
	def test_getDoc(self):
		testDict = {
				"toc": ['hello', 'world'],
				"hello": {
						"paras": "it is a good day",
						"lists": [["to", "live"]]
					},
				"world": {
						"paras": "it is a good day",
						"lists": [["to", "live"]]
					}
			}
		
		result = getDoc(testDict)
		self.assertEqual(result, (
			"it is a good day to live it is a good day to live ",
			"hello<NAME>it is a good day<PARAS>to<LI>live<LI><LIST><TOPIC>world<NAME>it is a good day<PARAS>to<LI>live<LI><LIST><TOPIC>"
		))

	# covers no lists present in testdict
	def test_getDoc_noList(self):
		testDict = {
				"toc": ['hello', 'world'],
				"hello": {
						"paras": "it is a good day",
						"lists": None
					},
				"world": {
						"paras": "it is a good day",
						"lists": None
					}
			}
		
		result = getDoc(testDict)
		self.assertEqual(result, (
			"it is a good day it is a good day ",
			"hello<NAME>it is a good day<PARAS><TOPIC>world<NAME>it is a good day<PARAS><TOPIC>"
		))

	# covers no paragraphs present in testdict
	def test_getDoc_noPara(self):
		testDict = {
				"toc": ['hello', 'world'],
				"hello": {
						"paras": None,
						"lists": [["to", "live"]]
					},
				"world": {
						"paras": None,
						"lists": [["to", "live"]]
					}
			}
		
		result = getDoc(testDict)
		self.assertEqual(result, (
			"to live to live ",
			"hello<NAME>to<LI>live<LI><LIST><TOPIC>world<NAME>to<LI>live<LI><LIST><TOPIC>"
		))
		
	# covers no paragraphs OR lists present in testdict
	def test_getDoc_noPara_noList(self):
		testDict = {
				"toc": ['hello', 'world'],
				"hello": {
						"paras": None,
						"lists": None
					},
				"world": {
						"paras": None,
						"lists": None
					}
			}
		
		result = getDoc(testDict)
		self.assertEqual(result, (
			"",
			"hello<NAME><TOPIC>world<NAME><TOPIC>"
		))

	# covers no toc key present in testdict
	def test_getDoc_no_toc(self):
		testDict = {"no": None, "table": None}
		result = getDoc(testDict)
		self.assertIsNone(result)

	# covers toc key having no value in testdict
	def test_getDoc_toc_None(self):
		testDict = {"toc": None}
		result = getDoc(testDict)
		self.assertIsNone(result)


# fanscrape.py tests
class testFan(unittest.TestCase):
	
	# acceptence test
	def test_stripSrcNum(self):
		teststr = "hello[007]"
		result = stripSrcNum(teststr)
		self.assertEqual(result, "hello")

	# Bottom-Up integration test for stripSrcNum() and getList()
	def test_getList(self):
		page = "<div><ul><li>hello[007]</li><li>world[89]</li></ul></div>"
		src = bs(page, 'html.parser')
		result = getList(src)
		self.assertEqual(result, ['hello', 'world'])



if __name__=='__main__':
	unittest.main()

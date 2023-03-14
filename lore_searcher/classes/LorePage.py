import textwrap


""" Page is the main content of any Lorebook. Page's contain all of
data returned from a LoreSearcher.search() call. There are several
useful methods available to Page:

- getSummary()
- getFull()
- printSummary(bound: int)
- printFull(bound: int)
- printFooter(bound: int)

You can read about these methods below
"""
class Page:

	# Initializes Page
	# doc: indexed and formatted document string
	# termHits: terms matched when returned from LoreSearcher.search() 

	def __init__(self, doc, termHits=[]):
		tmp = doc.split('<>')
		self.termHits = set(termHits)
		self.id = tmp[0]  					# document id
		self.pageName = tmp[1] 				# document name
		self.srcURL = tmp[2] 				# source url for document
		self.imgURL = tmp[3] 				# image url for document
		self.toc = tmp[4].split(',') 		# table of contents
		self.blurb = tmp[5] 				# first paragraph present in document
		self.topics = parseTopics(tmp[6]) 	# topics included in document

	# Returns a summary of LorePage in dict form. Useful for saving LorePage,
	# or sending LorePage in json format. A summary does not include the
	# the text of the topics it contains, only their names.

	def getSummary(self):
		tmpdict = {
			'id': self.id,
			'name': self.pageName,
			'img': self.imgURL,
			'url': self.srcURL,
			'blurb': self.blurb,
			'topics': self.toc
		}
		if len(self.termHits) > 0:
			tmpdict['matched-terms'] = self.termHits
		return tmpdict

	# Returns full LorePage in dict form. Useful for saving LorePage,
	# or sending LorePage in json format. A full LorePage includes
	# all topics and their text

	def getFull(self):
		tmpdict = {
			'id': self.id,
			'name': self.pageName,
			'img': self.imgURL,
			'url': self.srcURL,
			'blurb': self.blurb,
			'topics': self.toc,
			'topic-list': self.topics
		}
		if len(self.termHits) > 0:
			tmpdict['matched-terms'] = self.termHits
		return tmpdict

	
	# Prints a summary of LorePage to terminal.
	# int bound: char limit for printed lines

	def printSummary(self, bound=80):
		print(bound*"*" + "\n")
		title = f"{self.pageName.title()} (id: {self.id})\n"
		print(title.center(bound) + '\n')

		tmpTopics = ', '.join(self.toc)

		# will truncate topic name string if its length exceeds bound
		topicStr = tmpTopics[:bound - (len("Topics Included:") + 3)] + "..." if len(tmpTopics) > bound else tmpTopics
		print("Topics Included:", topicStr)

		# will truncate LorePage.blurb if its length exceeds 2 * bound
		blurb = self.blurb[:(bound*2) - 3] + "..." if len(self.blurb) > (bound*2) else self.blurb
		print(textwrap.fill(f"Description: {blurb}", width=bound))

		self.printFooter(bound)

	# Prints all LorePage fields to terminal
	# int bound: char limit for printed lines

	def printFull(self, bound=80):
		print(bound*"*" + "\n")
		title = f"{self.pageName.title()} (id: {self.id})\n"
		print(title.center(bound))
		print("Table of Contents:")

		# topic names printed in a 'table of contents; style
		print(len("Table of Contents:")*"-")
		for t in self.toc:
			print(f"|- {t.title()}")
		print("\n")

		for topic in self.topics:
			printTopic(topic, bound)

		self.printFooter(bound)

	# Prints termHits, srcURL, and imgURL to terminal. Called in both
	# both print methods. termHits will only be printed for pages returned
	# from a search
	# int bound: char limit for printed lines

	def printFooter(self, bound):
		print()
		if len(self.termHits) > 0:
			print("Matched Terms:", ", ".join(self.termHits))
		print(textwrap.fill(f"Source-URL: {self.srcURL}", width=bound))
		print(textwrap.fill(f"Img-URL: {self.imgURL}", width=bound))
		print("\n" + bound*"*")

# Helper function that prints a topics content to terminal.
# int bound: char limit for printed lines

def printTopic(topic, bound=80):
	topicName = topic['topic-name']
	topicParas = topic['paras'].strip() + "\n" if 'paras' in topic else ""
	topicLists = topic['lists'] if 'lists' in topic else []
	print(f"{topicName.title()}")
	print(bound*"-")
	
	# printing paragraphs found in topic
	if len(topicParas):
		print(textwrap.fill(topicParas, width=bound) + "\n")
	
	# printing any lists present in topic
	for tList in topicLists:
		for li in tList:
			print(textwrap.fill(f"- {li.strip()}", width=bound))

		print("\n")

# Helper function that parses an index documents topics. topicList will
# be initialized with parsed doc topics contents. Indexed doc topics have 
# a custom format: "topic_name<NAME>paragraph<PARAS>list_item<LI><LIST><TOPIC>"
# str topicDoc: index document to be parsed

def parseTopics(topicDoc):
	topics = []

	if '<TOPIC>' in topicDoc:
		tmpTopics = topicDoc.split('<TOPIC>')
	else:
		return topics

	for topic in tmpTopics:
		tmpDict = {}

		if '<NAME>' not in topic:
			continue

		tmpDict['topic-name'], docStr = topic.split('<NAME>')
		
		if '<PARAS>' in docStr:
			tmpDict['paras'], docStr = docStr.split('<PARAS>')

		if '<LIST>' in docStr:
			lists = docStr.split('<LIST>')[0:-1]
			tmpDict['lists'] = list(map(lambda x: x.split('<LI>')[0:-1], lists))

		topics.append(tmpDict)

	return topics


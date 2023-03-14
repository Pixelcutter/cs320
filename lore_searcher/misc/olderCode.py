# search session user configurations
# 'topN' = how many results to display after a search
# 'searchType' = type of search (AND = conjunctive, OR = disjunctive)
usrConfig = {"topN": 10, "searchType": "AND"}

def isQuit(usrInput):
	if usrInput.lower() == 'q':
		print("Goodbye")
		exit()
	
	return


# Prints out all results returned from a searched query to the console.

def printResults(resultDict):
	print("\n")
	totalResults = f"{resultDict['total-results']} results for '{resultDict['query']}'"
	title = f"< There are {totalResults}, here are the top {resultDict['topN']} >\n"
	print(title.center(80))

	i = 1

	for result in resultDict['results']:
		print(80*"*" + "\n")
		resultNum = f"{i}/{str(resultDict['topN'])}"
		print(resultNum.center(80) + "\n")
		print(f"ID: {str(result['id'])}")
		print(f"Name: {result['name'].title()}")
		print(f"Included Topics: {result['toc'].title()}")
		print(f"Source-URL: {result['link']}")
		print(f"Img-URL: {result['img']}")
		print(textwrap.fill("Description: " + result['blurb'], width=80) + "\n")

		i += 1

	print(80*"*" + "\n")

# Configures the behavior of the search engine. Configurations are stored in usrConfig, 
# and are used by getResults() serve up the appropriate query results. The configs can
# be changed at any time by typing 'CONFIG' into the query prompt

def getConfigs():
	searchType = input("Enter 'AND' for conjunctive search, or 'OR' for disjunctive search: ")
	isQuit(searchType)
	
	# while searchType != AND or OR, continue to prompt user 
	while searchType != 'AND' and searchType != 'OR':
		searchType = input("Please, only enter 'AND' or 'OR': ")
		isQuit(searchType)			

	# Search behavior set
	usrConfig['searchType'] = searchType

	limit = input("Enter the amount of results you want displayed from a search: ")

	# while limit != a positive integer, continue to prompt user
	while True:
		isQuit(limit)
		try:
			limit = int(limit)
			if limit < 0:
				limit = input("Enter only positive integers: ")
				continue
			break
		except:
			limit = input("Enter only positive integers: ")
			continue

	# Amount of results to return set
	usrConfig['topN'] = limit
	# done with configs, continue on to getting queries
	print("Done with setting up configs")
	print("Type 'CONFIG' into query prompt any time you want to change settings\n")
	
# Will continue to prompt user for a new query until they input 'q'
# Each query will be searched for in the index and it's returned results will
# be printed out to the console

def getQueries(ix):
	while True:
		userQuery = input("Enter a query (or type 'q' to quit): ")
		isQuit(userQuery)

		if userQuery == 'CONFIG':
			getConfigs()
			continue
		
		# query is searched for in index and its return results are printed
		# out to the console
		results = getResults(userQuery, ix)
		if len(results['results']):
			printResults(results)
		else:
			print("Did You Mean:", results['query'])
	

	


from classes.LorePage import Page
from classes.LoreSearcher import Searcher

# base of all searching (see LoreSearcher.py for def)
# '../data/index' is the directory path to indexed database
searcher = Searcher('data/index')

# will hold top three (limit) results found for search term 'tower twilight'
results = searcher.search('tower twilight', limit=3)

# prints out the summaries of pages returned from search to console
# if no results were found (results = None), searcher will attempt to fix query and offer a suggested query 
# saved under the 'corrected' key
print("------------------ summary print --------------------")
results = searcher.search('tower twilight', pageNum=1, limit=3)
if results['results'] == None:
    print(f"0 results found for '{results['query']}', did you mean '{results['corrected']}'?")
else:
    for result in results['results']:
        result.printSummary(80)

# prints full pages
print("\n------------------ full page print --------------------")
results = searcher.search('tower twilight', pageNum=2, limit=3)
if results['results'] == None:
	print(f"0 results found for '{results['query']}', did you mean '{results['corrected']}'?")
else:
	for result in results['results']:
		result.printFull(80)

# results will hold json objects representing page summaries returned from search
print("\n------------------ get summary page --------------------")
results = searcher.search('tower twilight', limit=3)
if results['results'] == None:
    print(f"0 results found for '{results['query']}', did you mean '{results['corrected']}'?")
else:
    for result in results['results']:
        print(result.getSummary())

# results will hold json objects representing full pages returned from search
print("\n------------------ get full page --------------------")
results = searcher.search('tower twilight', limit=3)
if results['results'] == None:
    print(f"0 results found for '{results['query']}', did you mean '{results['corrected']}'?")
else:
    for result in results['results']:
        print(result.getFull())

# no results returned for query, new query suggested and printed to console
print("\n------------------ bad query --------------------")
results = searcher.search('twer twlght', limit=3)
if results['results'] == None:
    print(f"0 results found for '{results['query']}', did you mean '{results['corrected']}'?")
else:
    for result in results['results']:
        result.printFull(80)

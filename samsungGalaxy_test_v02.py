import twitter
import json
from prettytable import PrettyTable
#------------------------------------------------------------------
#Authorisation stuff: - you might need to replace this with your own keys
#------------------------------------------------------------------
CONSUMER_KEY = 'SIeOam4mLD8sZWr7QHmE67zHi'
CONSUMER_SECRET = '444wPQutVPhns6ff8gdiWCrifgxkw4A6itsiPl3EQw5MhcQRDc'
OAUTH_TOKEN = '29954818-FRyNn2iHYP9QsK1srs2SQTWdxRPBygkm1mb6Fda2x'
OAUTH_TOKEN_SECRET = 'RUk8dVC5QJaXK9um6ADZvPSuGlzRiOSpusYs8SACRN6Yq'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)
#------------------------------------------------------------------

q = '#SamsungGalaxy'
print "query is: " + q + "\n"

#start timer not done yet

count = 1000

# See https://dev.twitter.com/docs/api/1.1/get/search/tweets
search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']

for _ in range(1000):
  #print "Length of statuses", len(statuses)
  try:
    next_results = search_results['search_metadata']['next_results']
  except KeyError, e: # No more results when next_results doesn't exist
    break
  #key word arguments
  #[1:] means from results 1 to how ever many there are
  kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
  search_results = twitter_api.search.tweets(**kwargs)
  #for each find - add the 'lists' to the array 'statuses' (bit different to c++ or java lists)
  statuses += search_results['statuses']

#print the results (unformatted)
#print json.dumps(statuses[0], indent=1)

#make more lists for the types of results
#txt - the human readable txt of the tweet - 

status_texts = [ status['text']
  for status in statuses ]

#screen name - the tweeter's account name
screen_names = [ user_mention['screen_name']
  for status in statuses
    for user_mention in status['entities']['user_mentions'] ]
      
hashtags = [ hashtag['text']
  for status in statuses
      for hashtag in status['entities']['hashtags'] ]

# Compute a collection of all words from all tweets
words = [ w
	  for t in status_texts
	    for w in t.split() ]

# Freq distribution - needs to be tabulated
from collections import Counter

for item in [words, screen_names, hashtags]:
  c = Counter(item)
print "**freq distribution - most common tweets**"
#print c.most_common()[:25]# top 25
#print

#number of results ie top 10
num = 10

for label, data in (('Word', words),
  ('Screen Name', screen_names),
  ('Hashtag', hashtags)):
  pt = PrettyTable(field_names=[label, 'Count'])
  c = Counter(data)
  [ pt.add_row(kv) for kv in c.most_common()[:10] ]
  pt.align[label], pt.align['Count'] = 'l', 'r' # Set column alignment
  print pt
  
  

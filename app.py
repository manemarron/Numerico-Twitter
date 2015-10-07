__author__ = 'manemarron'
import sys
from TwitterUtils import TwitterUtils,fix_tweets

twitter = TwitterUtils()
tweets = fix_tweets(twitter.search(sys.argv[1], result_type="recent", count=100))
print(tweets[0])
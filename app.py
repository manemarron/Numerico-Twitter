import sys
from TwitterUtils import TwitterUtils, fix_tweets
from DbUtils import DbUtils

twitter = TwitterUtils()
db = DbUtils()

q = str(sys.argv[1]).strip()
tweets = fix_tweets(twitter.search(q, result_type="recent", count=100))
query_id = db.insert(table="query", columns=["query"], values=[(q,)], returning="id")
ids = [(query_id, x[0]) for x in tweets]
db.insert(table="tweets", columns=["id", "text", "created_at", "user_id"], values=tweets)
db.insert(table="query_tweets",columns=["id_query", "id_tweet"], values=ids)

db.close()

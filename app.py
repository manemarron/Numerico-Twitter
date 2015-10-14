import sys
from TwitterUtils import TwitterUtils, fix_tweets
from DbUtils import DbUtils

twitter = TwitterUtils()
db = DbUtils()

q = str(sys.argv[1]).strip()
columns, update_columns, tweets = fix_tweets(twitter.search(q, result_type="recent", count=2))
query_id = db.selsert(table="query",insert_columns=["query"],insert_values=[(q,)],returning="id")
ids = db.upsert(table="tweets", columns=columns, update_columns=update_columns, values=tweets, returning="id")
ids = [(query_id, x[0]) for x in ids]
db.insert(table="query_tweets",columns=["id_query", "id_tweet"], values=ids)

db.close()

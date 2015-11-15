import argparse

from DbUtils import DbUtils
from TwitterUtils import TwitterUtils, fix_tweets

parser = argparse.ArgumentParser(description="Tweet options")
parser.add_argument('q', help="query")
parser.add_argument('-n', dest="n", type=int, default=1, help="Number of requests")
parser.add_argument('-result-type', dest="result_type", default="mixed", help="Result type")
parser.add_argument('-max-id', dest="max_id", default=None, help="Maximum Id from which to start searching")
parser.add_argument('-until', dest="until", default=None, help="Last date")
parser.add_argument('-lang', dest="lang", default=None, help="Language")
args = parser.parse_args()
q = args.q
n = args.n
result_type = args.result_type
max_id = args.max_id
until = args.until
lang = args.lang

twitter = TwitterUtils()
db = DbUtils()

next_results = {"q": q, "count": 100}
if result_type is not None:
    next_results["result_type"] = result_type
if max_id is not None:
    next_results["max_id"] = max_id
if until is not None:
    next_results["until"] = until
if lang is not None:
    next_results["lang"] = lang
db.cursor = db.conn.cursor()
try:
    for i in range(0, n):
        print("Request: %d" % (i+1,))
        result = twitter.search(**next_results)
        columns, update_columns, tweets = fix_tweets(result)
        db.upsert(table="tweets", columns=columns, update_columns=update_columns, values=tweets)

        if 'next_results' in result['search_metadata']:
            next_results = str(result['search_metadata']['next_results'][1:]).split('&')
            aux = dict()
            for x in next_results:
                x = x.split("=")
                aux[x[0]] = x[1]
            next_results = aux
            next_results['q'] = q
        else:
            break
except Exception as e:
    print(e)
finally:
    db.conn.commit()
    db.cursor.close()
    db.conn.close()

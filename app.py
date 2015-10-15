from TwitterUtils import TwitterUtils, fix_tweets
from DbUtils import DbUtils


class App:
    def __init__(self):
        self.twitter = TwitterUtils()
        self.db = DbUtils()

    def search(self, q, n=50):
        query_id = self.db.selsert(table="query", insert_columns=["query"], insert_values=[(q,)], returning="id")
        next_results = {"q": q, "result_type": "recent", "count": 100}
        for i in range(0, n):
            result = self.twitter.search(**next_results)
            columns, update_columns, tweets = fix_tweets(result)
            ids = self.db.upsert(
                table="tweets", columns=columns, update_columns=update_columns,
                values=tweets, returning="id"
            )
            ids = [(query_id, x[0]) for x in ids]
            self.db.insert(table="query_tweets", columns=["id_query", "id_tweet"], values=ids)

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

    def close(self):
        self.db.close()

from datetime import datetime
from urllib.parse import quote
from application_only_auth import Client

CONSUMER_KEY = "PXQXSszSKiWc5C1Zd2ntLfPWN"
CONSUMER_SECRET = "9cfmxsKUwQVzG3YStaTWlNjMMm2EIiFDIoWugdR9VQOdhyQ80g"

API_URL = "https://api.twitter.com/1.1"

URLS = {
    "search": "/search/tweets.json"
}


def fix_date(date):
        return datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')


def fix_tweets(tweets):
    columns = ["id", "text", "created_at", "user_id", "favorite_count", "retweet_count",
               "in_reply_to_status_id", "latitude", "longitude"]
    update_columns = ["favorite_count", "retweet_count"]
    values = []
    for t in tweets["statuses"]:
        value = (t["id_str"], t["text"], fix_date(t["created_at"]), t["user"]["id_str"],
                 int(t["favorite_count"]), int(t["retweet_count"]), t["in_reply_to_status_id_str"])
        if t["coordinates"] is not None:
            value += (float(t["coordinates"]["coordinates"][0]), float(t["coordinates"]["coordinates"][1]))
        else:
            value += (None, None)
        values.append(value)
    return columns, update_columns, values


class TwitterUtils:
    def __init__(self):
        self.__client = Client(CONSUMER_KEY, CONSUMER_SECRET)

    def __request(self, url, kwargs):
        url = "%s%s" % (API_URL, url)
        query = self.__generate_query(kwargs)
        result = self.__client.request(url + "?" + query)
        return result

    def search(self, q, **kwargs):
        url = URLS["search"]
        kwargs["q"] = q
        return self.__request(url, kwargs)

    @staticmethod
    def __generate_query(kwargs):
        s = ""
        for key in kwargs:
            val = quote(str(kwargs[key]), safe='')
            s += "%s=%s&" % (key, val)
        if len(s) > 0:
            s = s[:-1]
        return s

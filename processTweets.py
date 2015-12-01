from DbUtils import DbUtils
import re
db = DbUtils()

tweets = db.fetchall("tweets", ("text",), sort="id DESC")

tweets = [re.sub(r'http(s?).* ?', '', x[0]).strip().lower() for x in tweets]
tweets = list(set(tweets))
print("Tweets: " + str(len(tweets)))

words = [  # "star", "wars", "awakens", "force",
         "starwars", "r2", "k2", "jedi", "VII", "episode", "win",  "tickets", "december",
         "love", "hate", "can't", "cannot", "wait", "abrams", "excited", "trailer",
         "theforceawakens","new","rt", "!!","kylo ren", "no","spot", "rumours", "movie", "best", "huge",
         "premiere", "mistake", "spoiler", "lightsaber", "days", "counting", "ready", "upcoming",
         "bring", "soundtrack", "disney", "watching", "teaser", "believe", "video", "details",
         "nerd", "only", "looks", "ouch", "countdown", "holy shit", "come", "poster",
         "cool", "fuck", "exciting", "honest", "like", "cry", "epic", "need", "really",
         "chance", "only", "official", "pumped", "sucks"
         ]

with open("term_freq.csv","w") as f:
    f.write("i,j,x\r\n")
    for i in range(len(tweets)):
        for j in range(len(words)):
            cont = tweets[i].count(words[j])
            if cont > 0:
                f.write(str(i+1) + "," + str(j+1) + "," + str(cont) + "\r\n")

with open("words.csv","w") as f:
    f.write("id,word\r\n")
    for i in range(len(words)):
        f.write(str(i) + "," + words[i] + "\r\n")

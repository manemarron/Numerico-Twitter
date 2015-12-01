from DbUtils import DbUtils
import numpy as np
import re
db = DbUtils()

tweets = db.fetchall("tweets", ("text",), sort="id DESC")

print(len(tweets))
tweets = [re.sub(r'http(s?).* ?', '', x[0]).strip().lower() for x in tweets]
tweets = list(set(tweets))
print(len(tweets))

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
i_vector = []
j_vector = []
x_vector = []
for i in range(len(tweets)):
    for j in range(len(words)):
        cont = tweets[i].count(words[j])
        if cont > 0:
            i_vector.append(i+1)
            j_vector.append(j+1)
            x_vector.append(cont)
g = np.transpose(np.array([i_vector, j_vector, x_vector]))
np.savetxt("term_freq.csv", g, delimiter=",", header="i,j,x")

with open("words.csv","w") as f:
    f.write("id,word\r\n")
    for i in range(len(words)):
        f.write(str(i) + "," + words[i] + "\r\n")

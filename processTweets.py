from DbUtils import DbUtils
import re
import sys
db = DbUtils()

tweets = db.fetchall(sys.argv[2], ("text",), sort="id DESC")

tweets = [re.sub(r'http(s?).* ?', '', x[0]).strip().lower() for x in tweets]
tweets = list(set(tweets))
print("Tweets: " + str(len(tweets)))

with open(sys.argv[1]) as f:
    words = f.read().splitlines()

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

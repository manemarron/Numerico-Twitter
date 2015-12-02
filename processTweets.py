from DbUtils import DbUtils
import re
import sys
db = DbUtils()

tweets = db.fetchall(sys.argv[3], ("text",), sort="id DESC")

tweets = [re.sub(r'http(s?).* ?', '', x[0]).strip().lower() for x in tweets]
tweets = list(set(tweets))



with open("resources/stopwords.txt","rb") as f:
    stopwords = f.read().splitlines()

with open("resources/" + sys.argv[2], "w") as f:
    f.write("i,j,x\r\n")
    for i in range(len(tweets)):
        for j in range(len(words)):
            cont = tweets[i].count(words[j])
            if cont > 0:
                f.write(str(i+1) + "," + str(j+1) + "," + str(cont) + "\r\n")

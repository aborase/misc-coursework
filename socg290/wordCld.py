#!/usr/bin/env python2
"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""
import pickle
from os import path
from wordcloud import WordCloud,STOPWORDS


review_list = pickle.load(open("/home/abhitrip/Courses/SOCG290/Kitty_Ninja.data","rb"))

review_txt = open("/home/abhitrip/Courses/SOCG290/kitty.txt","w")


for each in review_list:
    review = each['review']
    review = ''.join([i  for i in review if ord(i)<128])
    each['review'] = str(review)
    review_txt.write(each["review"])
review_txt.close()




d = "/home/abhitrip/Courses/SOCG290/socg_data"

# Read the whole text.
text = open(path.join(d, 'Audiophiles.txt')).read()

STOPWORDS.add("headphone")
STOPWORDS.add("headphones")

STOPWORDS.add("button")
STOPWORDS.add("SOUND")
STOPWORDS.add("sound")
STOPWORDS.add("volume")



# Generate a word cloud image
wordcloud = WordCloud(background_color='black',max_words=400,stopwords=STOPWORDS,width=1280,height=720)
wordcloud.generate(text)
wordcloud.to_file(path.join(d,"Audiophiles.png"))
# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
# take relative word frequencies into account, lower max_font_size
#plt.figure()
#plt.imshow(wordcloud,cmap=plt.cm.gray)
#plt.axis("off")
#plt.show()

# The pil way (if you don't have matplotlib)
#image = wordcloud.to_image()
#image.show()

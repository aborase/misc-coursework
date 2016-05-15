#import urllib2
import pickle
from sets import Set
import numpy as np
import lda
#from bs4 import BeautifulSoup
import string
#import math

from nltk.tokenize import RegexpTokenizer
# To remove stop words
from stop_words import get_stop_words

from nltk.stem.porter import PorterStemmer
tokenizer = RegexpTokenizer(r'\w+')

from wordcloud import WordCloud,STOPWORDS
#tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')

all_reviews=[]
page_no=1
total_reviews=-1
max_page=100

review1     = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/AudioTechnica','rb'))
review2     = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/BoseHigh','rb'))
review3     = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/BoseMid','rb'))
review4     = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/Panasonic','rb'))
review5     = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/Philips','rb'))
review6     = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/Sennheiser-202','rb'))
review7     = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/SennHigh','rb'))
review8     = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/SkullcandyHesha','rb'))
review9     = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/SonyLow','rb'))
review10    = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/VModa','rb'))
review11    = pickle.load(open('/home/amit/Desktop/socg290/final/all_reviews/vModaHigh','rb'))

all_reviews = review1[0:300]+review2[0:300]+review3[0:300]+review4[0:300]+review5[0:300]+ \
              review6[0:300]+review7+review8[0:300]+review9[0:300]+review10[0:300]+review11[0:300]

#all_reviews=[rev in all_reviews]

for each in all_reviews:
    review_text = each['review']
    review_text= ''.join([i  for i in review_text if ord(i)<128])
    each['review'] = str(review_text)

texts = []
# To get the stop words like you're,can.myself,itself,i etc
en_stop = get_stop_words('en')
en_stop.extend(['wireless','bluetooth','sennheiser','skullcandy'])

review_set = []
tokens = []

new_idx = []
ind = 0
for each in all_reviews:
    review_str = each['review']
    review_str.decode('unicode_escape').encode('ascii','ignore')
    review_list = tokenizer.tokenize(review_str)
    ind = ind + 1
    if len(review_list)>50:
        review_set.append(review_str)
        new_idx.append(ind)

p_stemmer = PorterStemmer()
num_of_reviews = len(review_set)
# Tokenizing each review and removing stop words
bigram = []
unigram = []
texts = []
for each in review_set:
    lower_case_review = each.lower()
    lower_case_review=''.join([i for i in lower_case_review if i not in string.punctuation])
    tokens = tokenizer.tokenize(lower_case_review)
    #tokens = lower_case_review.split(" ")
    not_stopped_tokens = [tok_ns for tok_ns in tokens if not tok_ns in en_stop]
    #not_stopped_tokens = [p_stemmer.stem(ns_tok) for ns_tok in not_stopped_tokens]


    """
    Commented by @abhi for disabling bigram
    """

    big_temp = [not_stopped_tokens[ii] +' '+not_stopped_tokens[ii+1] for ii in range(len(not_stopped_tokens)-1)]
    texts = texts + big_temp

    #texts = texts + not_stopped_tokens







tokenized_words_set = Set(texts)

tokenized_words_list = list(tokenized_words_set)

# Create a Bigram model
# To remove uncommon bigrams

size = (len(tokenized_words_list))
token_cnt = np.zeros(size)


review_set_size = len(review_set);

for i in range(review_set_size):
    curr_review = review_set[i].lower()

    for j in range(size):
        if  tokenized_words_list[j] in curr_review:
            token_cnt[j]=token_cnt[j]+1




bigram_list = []
for idx in range(size):
    if token_cnt[idx]>=3:
        bigram_list.append(tokenized_words_list[idx])




#bigram_list = tokenized_words_list




capital_letters_count = np.zeros((num_of_reviews),np.int)
special_letters_count = np.zeros((num_of_reviews),np.int)


#num_of_tokens = len(tokenized_words_set)
num_of_tokens = len(bigram_list)

#tokens = list(tokenized_words_set)

tokens = bigram_list

dict_tokens = {tokens[i].lower():i for i in range(num_of_tokens)}

review_to_word_map = np.ones((num_of_reviews,num_of_tokens),np.int)

doc_freq = np.zeros((num_of_tokens,num_of_reviews))

for i in range(len(review_set)):
    sentence      = review_set[i]
    #if "!" in sentence or "?" in sentence or "'"  or "$"in sentence:
    # calculates the number of special_letters and capital letters in reviews

    for each_char in sentence:
        if  not each_char.isalpha() or each_char.isdigit():
            special_letters_count[i]=special_letters_count[i]+1
        if not each_char.lower() == each_char:
            capital_letters_count[i]=capital_letters_count[i]+1

    list_of_str = ''.join([x.lower() for x in sentence if x not in string.punctuation])
    list_of_str = list_of_str.split()


    for j in range(len(list_of_str)-1):
    #for j in range(len(list_of_str)):
        word1 =  (list_of_str[j]).lower()
        word2 =  (list_of_str[j+1]).lower()
        #"""
        bigram_curr = word1+ " "+ word2
        #"""
        #bigram_curr = word1;
        #multiply_factor = (word1!=word1.lower()) or (word2!=word2.lower())
        if bigram_curr in dict_tokens:
            word_idx = dict_tokens[bigram_curr]
            #if not multiply_factor:
            review_to_word_map[i][word_idx] = review_to_word_map[i][word_idx]+1
            #else:
            #review_to_word_map[i][word_idx] = review_to_word_map[i][word_idx]+2
            doc_freq[word_idx][i] = 1


doc_freq = np.sum(doc_freq,axis=1)

"""
for i in range(num_of_reviews):
    for j in range(num_of_tokens):
        idf = num_of_reviews/(doc_freq[j]+1)
        review_to_word_map[i][j] = review_to_word_map[i][j]*math.log(idf)
"""



"""
Using our review_to_word_map to calculate meaningful clusters using LDA
"""

number_of_topics = 40
word_prob_per_topic = np.zeros((number_of_topics,num_of_tokens))
idx_top_probs_per_topic = np.zeros((number_of_topics,num_of_tokens))

model = lda.LDA(n_topics=number_of_topics, n_iter=150, random_state=1)
model.fit(review_to_word_map)
topic_word = model.topic_word_  # model.components_ also works

word_prob_per_topic = np.zeros((number_of_topics,num_of_tokens))
idx_top_probs_per_topic = np.zeros((number_of_topics,num_of_tokens))
log_word_prob_per_topic = np.zeros((number_of_topics,num_of_tokens))




# printing top words
n_top_words = 30

l1 = dict_tokens.values()
l2 = dict_tokens.keys()


for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(tokens)[np.argsort(topic_dist)][:-n_top_words:-1]
    word_prob_per_topic[i] = topic_dist
    idx_top_probs_per_topic[i] = np.argsort(topic_dist)[:-(num_of_tokens+1):-1]
    print('Topic {}: {}'.format(i, ' ; '.join(topic_words)))
    #num_of_reviews

#%%
"""
Classifying Audiophiles and Fashion Driven
"""

pragmatic = [3,5,14,16,19,20,23,28,31,34,37]
purists = [4,22,30,32,39]
yuppies = [1,10,18,25,26]
disenfranchised = [2,8,29,36]

doc_id = 0
prag = []

pure = []
yupy = []
disf = []


fpr = open('pragmatic.txt', 'wb')
fpu = open('purists.txt', 'wb')
fdf = open('disenfranchise.txt', 'wb')
fyu = open('yuppies.txt', 'wb')

total = pragmatic + purists + yuppies + disenfranchised

for i in range(num_of_reviews):
    prob = []

    for j in total:
        prob.append(np.dot(review_to_word_map[i],word_prob_per_topic[j]))

    index = prob.index(max(prob))

    if total[index] in pragmatic:
        prag.append(review_set[i])
        fpr.write(review_set[i] + '\n')
    elif total[index] in purists:
        pure.append(review_set[i])
        fpu.write(review_set[i] + '\n')
    elif total[index] in yuppies:
        yupy.append(review_set[i])
        fyu.write(review_set[i] + '\n')
    else:
        disf.append(review_set[i])
        fdf.write(review_set[i] + '\n')

fpr.close()
fpu.close()
fdf.close()
fyu.close()

print len(prag)
print len(pure)
print len(yupy)
print len(disf)

#%%

from wordcloud import WordCloud,STOPWORDS
#d = "/home/abhitrip/Courses/SOCG290/socg_data"

# Read the whole text.
text = open('pragmatic.txt').read()

STOPWORDS.add("headphone")
STOPWORDS.add("headphones")

STOPWORDS.add("button")
STOPWORDS.add("SOUND")
STOPWORDS.add("sound")
STOPWORDS.add("volume")
STOPWORDS.add("ear")


# Generate a word cloud image
wordcloud = WordCloud(background_color='black',max_words=400,stopwords=STOPWORDS,width=1280,height=720)
wordcloud.generate(text)
wordcloud.to_file("Audiophiles.png")
# Display the generated image:
# the matplotlib way:
#import matplotlib.pyplot as plt
# take relative word frequencies into account, lower max_font_size
#plt.figure()
#plt.imshow(wordcloud,cmap=plt.cm.gray)
#plt.axis("off")
#plt.show()

# The pil way (if you don't have matplotlib)
#image = wordcloud.to_image()
#image.show()

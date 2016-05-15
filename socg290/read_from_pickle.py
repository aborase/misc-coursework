try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import pickle
try:
    from sets import Set
except ImportError:
    Set = set
import numpy as np
import lda
from bs4 import BeautifulSoup
import math
from nltk.tokenize import RegexpTokenizer
# To remove stop words
from stop_words import get_stop_words

from nltk.stem.porter import PorterStemmer

##BASE_URL='http://www.amazon.com/Powerbeats-Wireless-In-Ear-Headphone-Black/product-reviews/B00IYA2ZJW/ref=cm_cr_pr_btm_link_2?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber='
#BASE_URL=['http://www.amazon.com/Beats-Solo2-Wired-On-Ear-Headphones/product-reviews/B00IYA2SMQ/ref=cm_cr_pr_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=', 'http://www.amazon.com/Skullcandy-Hesh-2-Discontinued-Manufacturer/product-reviews/B003IBB6M4/ref=cm_cr_dp_see_all_summary?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=', 'http://www.amazon.com/Sennheiser-RS-180-Discontinued-Manufacturer/product-reviews/B002TLT10S/ref=cm_cr_pr_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=']

#BASE_URL=['http://www.amazon.com/Sennheiser-RS120-Wireless-Headphones-Charging/product-reviews/B0001FTVEK/ref=cm_cr_dp_see_all_summary?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=', 'http://www.amazon.com/Skullcandy-Hesh-2-Discontinued-Manufacturer/product-reviews/B003IBB6M4/ref=cm_cr_dp_see_all_summary?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=', 'http://www.amazon.com/Beats-Studio-Wireless-Over-Ear-Headphone/product-reviews/B00FK0ELRI/ref=cm_cr_dp_see_all_summary?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=']
BASE_URL=['http://www.amazon.com/Sennheiser-HD-650-Professional-Headphone/product-reviews/B00018MSNI/ref=cm_cr_pr_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=', 'http://www.amazon.com/Sennheiser-Momentum-Headphone-Brown/product-reviews/B009QV15DU/ref=cm_cr_pr_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=', 'http://www.amazon.com/Bose-QuietComfort-Cancelling-Discontinued-Manufacturer/product-reviews/B0054JJ0QW/ref=cm_cr_pr_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=', 'http://www.amazon.com/V-MODA-Crossfade-Over-Ear-Noise-Isolating-Headphone/product-reviews/B00A39PPCG/ref=cm_cr_pr_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=', 'http://www.amazon.com/Beats-Studio-Wireless-Headphone-White/product-reviews/B00GBVKM5U/ref=cm_cr_pr_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=', 'http://www.amazon.com/Bose-QuietComfort-Acoustic-Cancelling-Headphones/product-reviews/B00M1NEUKK/ref=cm_cr_pr_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=']
all_reviews=[]
for i in BASE_URL:
    page_no=1
    total_reviews=-1
    max_page=100
    while total_reviews!=0 and page_no<=max_page:
        print ('Page No: %d' %(page_no))
        try:
            fname=urllib2.urlopen(i+str(page_no))
            soup=BeautifulSoup(fname,"html.parser")
            tags_rvw_sec=soup.find_all("div",{"class":"a-section review"})
            total_reviews=len(tags_rvw_sec)
            for sections in tags_rvw_sec:
                tags_review=sections.find("span",{"class":"a-size-base review-text"})
                tags_rating=sections.find("span",{"class":"a-icon-alt"})
                tags_user=sections.find("span",{"class":"a-size-base a-color-secondary review-byline"})
                tags_date=sections.find("span",{"class":"a-size-base a-color-secondary review-date"})
                tags_valid_purchase = sections.find("span",{"class":"a-size-mini a-color-state a-text-bold"})



                review=dict()
                review['rating']=float(tags_rating.get_text()[:3])
                review['user']=tags_user.find('a').get_text()
                review['review']=tags_review.get_text()
                review['date']=tags_date.get_text()[3:]
                """
                if tags_valid_purchase != None:
                    review['valid_purchase'] = tags_valid_purchase.get_text()
                else:
                    review['valid_purchase'] = "Not Valid Purchase"

                """
                try:
                    review['valid_purchase'] = tags_valid_purchase.get_text()
                except:
                    print ("Not a valid Purchase")
                    review['valid_purchase'] = 'Not Valid Purchase'



                for tag in sections.find_all('a'):
                    if('review-title' in tag['class']):
                        review['title']=tag.get_text()
                        break
                for tag in sections.find_all('a'):
                    if('review-title' in tag['class']):
                        review['title']=tag.get_text()
                        break

                all_reviews.append(review)
            page_no+=1
        except:
            print ('Exception...Trying again')

pickle.dump(all_reviews,open('amazon_data','wb'))
#%%

texts = []
# To get the stop words like you're,can.myself,itself,i etc
en_stop = get_stop_words('en')


# Remove stemmings from stopped tokems
#p_stemmer = PorterStemmer()



#kitty_ninja = pickle.load(open('/home/abhitrip/Kitty_Ninja.data','rb'))
#beats_pro =  pickle.load(open('/home/abhitrip/Courses/SOCG290/socg_data/amazon_data_beats_pro'))
#monster =  pickle.load(open('/home/abhitrip/Courses/SOCG290/socg_data/amazon_data_monster'))
#soundtrue =  pickle.load(open('/home/abhitrip/Courses/SOCG290/socg_data/amazon_data_beats_soundtrue'))
#scullcandy =  pickle.load(open('/home/abhitrip/Courses/SOCG290/socg_data/amazon_data_scullcandy_hesh2'))
#studio =  pickle.load(open('/home/abhitrip/Courses/SOCG290/socg_data/amazon_data_beats_studio1'))
#senn_rs120 =  pickle.load(open('/home/abhitrip/Courses/SOCG290/socg_data/amazon_data_senn_rs120'))
#bose_comfort =  pickle.load(open('/home/abhitrip/Courses/SOCG290/socg_data/amazon_data_bose_quietcomfort'))
#senn_rs180 =  pickle.load(open('/home/abhitrip/Courses/SOCG290/socg_data/amazon_data_senn_rs180'))
#bose_soundtrue =  pickle.load(open('/home/abhitrip/Courses/SOCG290/socg_data/amazon_data_bose_soundtrue'))
#ata_sync_wrath =  pickle.load(open('/home/abhitrip/Courses/SOCG290/socg_data/amazon_data_sync_wrath'))


#all_reviews = kitty_ninja + beats_pro + monster + soundtrue + scullcandy + studio #+ senn_rs120 + bose_comfort + senn_rs180 + bose_soundtrue + data_sync_wrath

#all_reviews = kitty_ninja +bose_soundtrue

review_set = []

tokens = []

tokenizer = RegexpTokenizer(r'\w+')

for each in all_reviews:
    review_str = each['review']
    #temp_tokens = tokenizer.tokenize(review_str)
    temp_tokens = review_str.split(" ")
    if len(temp_tokens)>30:
        review_set.append(review_str)


num_of_reviews = len(review_set)
# Tokenizing each review and removing stop words
for each in review_set:

    lower_case_review = each.lower()
    #tokens = tokenizer.tokenize(lower_case_review)
    tokens = lower_case_review.split(" ")
    stopped_tokens = [i for i in tokens if not i in en_stop]

    texts = texts + (stopped_tokens)

tokenized_words_set = Set(texts)



capital_letters_count = np.zeros((num_of_reviews),np.int)
special_letters_count = np.zeros((num_of_reviews),np.int)


num_of_tokens = len(tokenized_words_set)

tokens = list(tokenized_words_set)

dict_tokens = {tokens[i].lower():i for i in range(num_of_tokens)}

review_to_word_map = np.zeros((num_of_reviews,num_of_tokens),np.int)

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

    list_of_str = tokenizer.tokenize(sentence)
    for each in list_of_str:
        if each.lower() in dict_tokens:
            #print each
            word_idx = dict_tokens[each.lower()]
            # calculating the number of times each word of the entire vocabulary occurs in a review
            review_to_word_map[i][word_idx] = review_to_word_map[i][word_idx]+1
            doc_freq[word_idx][i] = 1


doc_freq = np.sum(doc_freq,axis=1)

for i in range(num_of_reviews):
    for j in range(num_of_tokens):
        idf = num_of_reviews/(doc_freq[j]+1)
        review_to_word_map[i][j] = review_to_word_map[i][j]*math.log(idf)



#%%
"""
Using our review_to_word_map to calculate meaningful clusters using LDA
"""

number_of_topics = 10
word_prob_per_topic = np.zeros((number_of_topics,num_of_tokens))
idx_top_probs_per_topic = np.zeros((number_of_topics,num_of_tokens))

model = lda.LDA(n_topics=number_of_topics, n_iter=500, random_state=1)
model.fit(review_to_word_map)
topic_word = model.topic_word_  # model.components_ also works

word_prob_per_topic = np.zeros((number_of_topics,num_of_tokens))
idx_top_probs_per_topic = np.zeros((number_of_topics,num_of_tokens))



# printing top words
n_top_words = 25
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(tokens)[np.argsort(topic_dist)][:-n_top_words:-1]
    word_prob_per_topic[i] = topic_dist
    idx_top_probs_per_topic[i] = np.argsort(topic_dist)[:-(num_of_tokens+1):-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    #num_of_reviews


#%%


"""
Classifying Audiophiles and Fashion Driven
"""

doc_id = 0
label_fashion = []
label_audiophile = []
label = []
total_prob = np.zeros((number_of_topics));

for i in range(num_of_reviews):
    for j in range(number_of_topics):
        prob = np.dot(review_to_word_map[i],word_prob_per_topic[j]);
        total_prob[j] = prob

    index = np.argmax(total_prob)
    label.append(index)

print (np.sum([1 for i in label if i in [3,6,8,9]]))
print (np.sum([1 for i in label if i in [0,1,2]]))
pickle.dump(review_set,open('review_set_high','wb'))
pickle.dump(label,open('label_high','wb'))

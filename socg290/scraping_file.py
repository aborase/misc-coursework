"""
Created on Tue Jan 05 13:09:38 2016

@file tokenized_LDA_clusters.py
@author: Group I
@brief Program to scrape data from Amazon.
"""


"""
Code Adapted from Apurva Pathak's scraping file
Scrapes 500 reviews
"""


import urllib2
import pickle
import sets
import numpy as np
import lda
from bs4 import BeautifulSoup


BASE_URL='http://www.amazon.com/Powerbeats-Wireless-In-Ear-Headphone-Black/product-reviews/B00IYA2ZJW/ref=cm_cr_pr_btm_link_2?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber='

all_reviews=[]
page_no=1
total_reviews=-1
max_page=500

num_of_reviews = 0

#%%
while total_reviews!=0 and page_no<=max_page:
    print 'Page No: %d' %(page_no)
    try:
        fname=urllib2.urlopen(BASE_URL+str(page_no))
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
                print "Not a valid Purchase"
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
            num_of_reviews = num_of_reviews +1
            if(num_of_reviews>1000):
                break
        page_no+=1
    except:
        print 'Exception...Trying again'

pickle.dump(all_reviews,open('amazon_1000_headphone_reviews','wb'))

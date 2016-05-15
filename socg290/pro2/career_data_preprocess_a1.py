"""
This file is to preprocess the data gathered from web of science
We will have to make a sequence of all the universities associated with a researcher
"""
import pickle
from optimalMatching import  OptimalMatching


file_ptr = open('/home/amit/acads/socg290/pro2/data_chunk1','rb')
records  = pickle.load(file_ptr)
file_ptr.close()

file_ptr = open('/home/amit/acads/socg290/pro2/data_chunk2','rb')
records  = records + pickle.load(file_ptr)
file_ptr.close()


file_ptr = open('/home/amit/acads/socg290/pro2/data_chunk3','rb')
records  = records + pickle.load(file_ptr)
file_ptr.close()
#%%

dict_author_univ = dict()
authors = []
for each_record in records:
    author = each_record['author']
    authors.append(author)

set_of_authors = set(authors)
# To Remove Duplicates from all the set
authors = list(set_of_authors)
#%%
corresponding_univs = [[] for z in authors] # A list of list to store all univeristies a author has worked at
for each_record in records:
    author = each_record['author']
    ## Now a loop for each  

    author_idx = authors.index(author)
    varsity = each_record['organization']
    if varsity=='':
        varsity = 'unknown'
    corresponding_univs[author_idx].append(varsity.strip())


idx = []
multiple_univs = []

#%% Filtering out unuseful parameters

useful_data_list = []


for j in range(len(corresponding_univs)):
    if len(corresponding_univs[j])>1:
        idx.append(j)
        useful_data = dict()
        useful_data['organization'] = corresponding_univs[j] 
        useful_data['author'] = records[j]['author']
        useful_data_list.append(useful_data)        
        for each in corresponding_univs[j]:
            multiple_univs.append(each)

#%% Filtering out universities where one is unknown

filtered_rec=[]

for each_record in useful_data_list:
    num_of_univs = each_record['organization']
    cnt_null = num_of_univs.count('')
    cnt_unknown = num_of_univs.count('unknown')
    if len(each_record['organization'])>=3+cnt_null+cnt_unknown:
        filtered_rec.append(each_record)
        
            
#%% Assign University Id's To all
all_unique_addresses = set()
for all in filtered_rec:
    list_of_orgs=all['organization']
    for orgs in list_of_orgs:
        all_unique_addresses.add(orgs)
    
all_unique_addresses = list(all_unique_addresses)

univ_ids = [[] for all in filtered_rec]
for i,item in enumerate(filtered_rec):
    list_of_orgs = item['organization']
    univ_ids[i] = [all_unique_addresses.index(x) for x in list_of_orgs]
    
    
#%% Now Let's do sequence analysis
f = open('univ_text','w')
for each in all_unique_addresses:
    f.write(each+'\n')
f.close()    
#%% Take Rankings from Txt file
import numpy as np
ranking = np.genfromtxt('/home/amit/acads/socg290/pro2/ranking_tier.txt',delimiter='\n')
rank_list = list(ranking)

regions = np.genfromtxt('/home/amit/acads/socg290/pro2/regions.txt',delimiter='\n')
region_list = list(regions)

#%% Now Assign sequence Id's to all

seq_tier = [[] for all in filtered_rec]
for i,all in enumerate(univ_ids):
    seq_tier[i] = [rank_list[x] for x in all]
    
#%% Now Compute A MxM Matrix calculating sequence distance between sequences
len_seqs  = len(seq_tier)
rank_dist = np.zeros((len_seqs,len_seqs))
for i in range(len_seqs):
    for j in range(len_seqs):
        rank_dist[i][j] = OptimalMatching(seq_tier[i],seq_tier[j])
    
    
#%%
import numpy as np
import random as rnd

distance = rank_dist
k = 3

num_samples =  np.shape(distance)[0]
samples = np.array(rnd.sample(range(num_samples),k))

old_medoid = np.zeros(3)
new_medoid = np.zeros(3)    
curr_medoid = np.array(samples)

new_labels = np.zeros(num_samples)

max_itrs = 50
itr = 0;
"""while not (np.array_equal(old_medoid,curr_medoid)):"""
while itr<max_itrs:
    cluster = [[] for x in range(k)]
# Compute the Cluster to be Assigned to  the point
    for i in range(num_samples):
        dist_from_medoid = distance[i][samples]
        min_dist_idx = np.argmin(dist_from_medoid)
        label = samples[min_dist_idx]
        new_labels[i] = label
        cluster[min_dist_idx].append(i)

# Calculate Groups of each of the cluster
    for w in range(len(samples)):
        curr_cluster = cluster[w]
        d = np.zeros((len(curr_cluster)))
        for i in range(len(curr_cluster)):
            d[i] = np.sum(distance[curr_cluster[i],curr_cluster])
        medoid_idx = np.argmin(d)
        new_medoid[w] = curr_cluster[medoid_idx]

    old_medoid[:] = curr_medoid[:]   
    curr_medoid[:] = new_medoid[:]     
    itr = itr+1

            
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


dict_author_univ = dict()
authors = []
for each_record in records:
    author = each_record['author']
    authors.append(author)

set_of_authors = set(authors)
# To Remove Duplicates from all the set
authors = list(set_of_authors)

corresponding_journals = [[] for z in authors]

corresponding_univs = [[] for z in authors] # A list of list to store all univeristies a author has worked at
for each_record in records:
    author = each_record['author']
    ## Now a loop for each  

    author_idx = authors.index(author)
    varsity = each_record['organization']
    if varsity=='':
        varsity = 'unknown'
    jtag = each_record['journal']
    corresponding_univs[author_idx].append(varsity.strip())
    corresponding_journals[author_idx].append(jtag.strip())

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
        useful_data['journal'] = corresponding_journals[j]
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

all_unique_addresses = []
f = open('/home/amit/acads/socg290/pro2/univ_text_latest','r')
for each in f:
    all_unique_addresses.append(each.strip())
f.close()    
#%%

univ_ids = [[] for all in filtered_rec]
for i,item in enumerate(filtered_rec):
    list_of_orgs = item['organization']
    univ_ids[i] = [all_unique_addresses.index(x.strip()) for x in list_of_orgs]
    
    
#%% Now Let's do sequence analysis
#all_unique_addresses = []
#f = open('univ_text','r')
#for each in f:
#    all_unique_addresses.append(each.strip())
#f.close()    

#%% Take Rankings from Txt file
import numpy as np
ranking = np.genfromtxt('/home/amit/acads/socg290/pro2/ranking_tier.txt',delimiter='\n')
rank_list = list(ranking)

regions = np.genfromtxt('/home/amit/acads/socg290/pro2/regions.txt',delimiter='\n')
region_list = list(regions)

#%% Now Assign sequence Id's to all

seq_tier = [[] for all in filtered_rec]
for i,all in enumerate(univ_ids):
    seq_tier[i] = [region_list[x] for x in all]
    
seq_tier1 = [[] for all in filtered_rec]
for i,all in enumerate(univ_ids):
    seq_tier1[i] = [rank_list[x] for x in all]
    
#%% Now Compute A MxM Matrix calculating sequence distance between sequences
len_seqs  = len(seq_tier)
region_dist = np.zeros((len_seqs,len_seqs))
for i in range(len_seqs):
    for j in range(len_seqs):
        region_dist[i][j] = OptimalMatching(seq_tier[i],seq_tier[j])

len_seqs1  = len(seq_tier1)
rank_dist = np.zeros((len_seqs1,len_seqs1))
for i in range(len_seqs1):
    for j in range(len_seqs1):
        rank_dist[i][j] = OptimalMatching(seq_tier1[i],seq_tier1[j])
    
    
#%%
import numpy as np
import random as rnd

distance = region_dist
k = 4

num_samples =  np.shape(distance)[0]
samples = np.array(rnd.sample(range(num_samples),k))

old_medoid = np.zeros(k)
new_medoid = np.zeros(k)    
curr_medoid = np.array(samples)

new_labels = np.zeros(num_samples)

max_itrs = 100
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

#%%
distance1 = rank_dist
k = 3

num_samples1 =  np.shape(distance1)[0]
samples1 = np.array(rnd.sample(range(num_samples1),k))

old_medoid1 = np.zeros(k)
new_medoid1 = np.zeros(k)    
curr_medoid1 = np.array(samples1)
cluster1 = []
new_labels1 = np.zeros(num_samples1)
"""while not (np.array_equal(old_medoid,curr_medoid)):"""
while itr<max_itrs:
    cluster1 = [[] for x in range(k)]
# Compute the Cluster to be Assigned to  the point
    for i in range(num_samples1):
        dist_from_medoid = distance1[i][samples1]
        min_dist_idx = np.argmin(dist_from_medoid)
        label = samples1[min_dist_idx]
        new_labels1[i] = label
        cluster1[min_dist_idx].append(i)
        
# Calculate Groups of each of the cluster1
    for w in range(len(samples1)):
        curr_cluster = cluster1[w]
        d = np.zeros((len(curr_cluster)))
        for i in range(len(curr_cluster)):
            d[i] = np.sum(distance1[curr_cluster[i],curr_cluster])
        medoid_idx = np.argmin(d)
        new_medoid1[w] = curr_cluster[medoid_idx]

    old_medoid1[:] = curr_medoid1[:]   
    curr_medoid1[:] = new_medoid1[:]     
    itr = itr+1
#%%
import xlwt


book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

x = 0
y = 0
sheet1.write(x, y, 'region cluster')
y+=1
sheet1.write(x, y, 'cluster members')
x+=1

for i in range(np.shape(curr_medoid)[0]):
    y = 0
    sheet1.write(x, y, i)
    y+=1
    sheet1.write(x, y, str(seq_tier[curr_medoid[i]]))
    x+=1
    
x+=1
y=0

sheet1.write(x, y, 'tier cluster')
y+=1
sheet1.write(x, y, 'cluster members')
x+=1

for i in range(np.shape(curr_medoid1)[0]):
    y = 0
    sheet1.write(x, y, i)
    y+=1
    sheet1.write(x, y, str(seq_tier1[curr_medoid1[i]]))
    x+=1
    
x+=1
y=0


sheet1.write(x, y, 'author')
y+=1
sheet1.write(x, y, 'journals')
y+=1
sheet1.write(x, y, 'universities')
y+=1
sheet1.write(x, y, 'region ranking')
y+=1
sheet1.write(x, y, 'region cluster')
y+=1
sheet1.write(x, y, 'tier ranking')
y+=1
sheet1.write(x, y, 'tier cluster')
x+=1

for i in filtered_rec:
    y = 0
    x+=1
    
    sheet1.write(x, y, i['author'])
    y+=1
    xx = x
    
    for j in i['journal']:
        sheet1.write(x, y, str(j))
        x+=1
    y+=1
    
    x = xx
    for j in i['organization']:
        sheet1.write(x, y, str(j))
        x+=1
    y+=1
    
    x = xx
    for j in seq_tier[filtered_rec.index(i)]:
        sheet1.write(x, y, str(j))
        x+=1
    y+=1
    
    for j in cluster:
        if j.count(filtered_rec.index(i)) == 1:
            sheet1.write(xx, y, str(cluster.index(j)))
            break
    y+=1

    x = xx
    for j in seq_tier1[filtered_rec.index(i)]:
        sheet1.write(x, y, str(j))
        x+=1
    y+=1 
    
    for j in cluster1:
        if j.count(filtered_rec.index(i)) == 1:
            sheet1.write(xx, y, str(cluster1.index(j)))
            break
        
    y+=1


book.save("/home/amit/acads/socg290/pro2/result.xls")


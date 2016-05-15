# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 18:37:24 2016

@author: amit
"""

import pickle
#from sets import set
amit = pickle.load(open('/home/amit/acads/socg290/pro3/wos_1_2071_soc_data', 'rb'))

count = 0
f = open('/home/amit/acads/socg290/pro3/comb_data.txt', 'r')
g = open('/home/amit/acads/socg290/pro3/uniadded.txt', 'w')

var = f.readline()
uni = set([])
while var:
    g.write(var)
    
    if var.count('WOS'):
        g.write('UN ')
        if 'organization' in amit[count]:
            for i in amit[count]['organization']:
                g.write(i)
                g.write(', ')
                uni.add(i)
        else:
            g.write('unknown')
        g.write('\n')
        count += 1    
    
    var = f.readline()
    
f.close()
g.close()

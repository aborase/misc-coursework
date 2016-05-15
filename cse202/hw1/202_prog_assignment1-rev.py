# coding: utf-8

import re

# Pythons default stack_size limits recursive calls to < 1000. Below code modifies the same to 1200.
#import sys
#sys.setrecursionlimit(1200)

# Read data from input file
#print "Read input.txt"
line = open('./input.txt', 'r').readlines()

# Extract start_node and node_count
node_count=int(line[0])
x=str(line[node_count+1])
start_node = int(re.sub('v', '', x))-1

# Build adj_list for each node
adj_list=[]
for i in range(1, node_count+1):
    adj=line[i].split("->")[1:]
    adj_list.append(adj)
#print "Adjacency list"

# Build a topological ordering using a DFS approach
#def dfs_topo(v):
#    visited[v] = True
#    for w in range (len(adj_list[v])):
#        y=str(adj_list[v][w])
#        child=int(re.sub('v','',y))-1
#        if(not visited[child]):
#            dfs_topo(child)
#    topo_order.insert(0,v)
           
#topo_order=[]
#visited = []
#for i in range(node_count):
#    visited.append(False)
#dfs_topo(start_node)

edge_count = [0 for i in range(node_count)]
for u in range(node_count):
    num_edges = len(adj_list[u])
    for v in range(num_edges):
        y=str(adj_list[u][v])
        edge_node = int(re.sub('v', '', y))-1
        edge_count[edge_node]+=1

def topo_order_add(u):
    topo_order.append(u)
    edge_count[u] = "NIL"
    for v in range(len(adj_list[u])):
        z=str(adj_list[u][v])
        w=int(re.sub('v', '', z))-1
        edge_count[w]-=1

topo_order=[]
while (len(topo_order) < node_count):
    for i in range(node_count):
        if edge_count[i] == 0:
            topo_order_add(i)

#print topo_order 
#print edge_count

# Traverse the nodes along topological ordering and determine if they
# are at even_length or odd_length or even_odd_length from u

node_marking=[ -1 for i in range(node_count) ]
# -1 => not discovered yet
# 0 => is at even path lengh
# 1 => is at odd path length
# 2 => is at even and od length

#ignore all the nodes placed before u in topo order using below flag
u_found=False

for i in range(node_count):
    curr=topo_order.pop(0)
    if u_found==True and curr!=start_node:
        u_found=True
	# print u_found
	if node_marking[curr]==-1:
	    continue
        for j in range (len(adj_list[curr])):
            y=str(adj_list[curr][j])
            child=int(re.sub('v','',y))-1
            if node_marking[curr]==0:
                if node_marking[child]==-1:
                      node_marking[child]=1
                elif node_marking[child]==0:
                      node_marking[child]=2
	    if node_marking[curr]==1:
                if node_marking[child]==-1:
                      node_marking[child]=0
                elif node_marking[child]==1:
                      node_marking[child]=2
            if node_marking[curr]==2:
                node_marking[child]=2
    elif u_found==False and curr==start_node :
            u_found=True
            node_marking[curr]=0
            for j in range(len(adj_list[curr])):
                y=str(adj_list[curr][j])
                child=int(re.sub('v','',y))-1
                if node_marking[child]==-1:
                    node_marking[child]=1
                elif node_marking[child]==0:
                    node_marking[child]=2
    elif u_found==False and curr!=start_node :
        continue

# build the results in required outout format
count=0
even_nodes=""
#glue = "->v"
for i in range(node_count):
    if node_marking[i]==2 or node_marking[i]==0:
        count = count +1
        num_node=str("v%i" % (i+1))
        if count !=1:
            even_nodes = even_nodes +  ",%s" % num_node 
        else:
            even_nodes = "%s" % num_node

result = str(count) + "\n" + even_nodes
#print result

# write result to output file
output = open('./output.txt', 'w')
output.write(result)
output.close()


# coding: utf-8

import re
#import numpy

# Read data from input file
#print "Read input.txt"
line = open('./input.txt','r').readlines()

# Extract total node_count
nodes = int(line[0])
#print nodes

# Read column and row degree's and sort them
row = []
column = []
row1 = [int(x) for x in line[1].split(",")]
column1 = [int(x) for x in line[2].split(",")]
#print row1
#print column1
row = sorted(row1, reverse=True)
column = sorted(column1, reverse=True)
#print row
#print column

# Build Minimal row matrix
col_cnt = [0 for x in range(nodes)]
matrix = [[0 for x in range(nodes)] for x in range(nodes)]
for i in range(0, nodes):
    for j in range(0, row[i]):
        matrix[i][j] = 1
        col_cnt[j] += 1
#print (numpy.array(matrix))

# Column transformations starting from n-1^th column and n-1^th row
feasible = True
# Keep satisfying one c^i at a time. Start from least C^i
for c in range(nodes-1, -1, -1):
    #print ("column iteration %d" % c)
    #print ("Before")
    #print numpy.array(matrix)
    #c_sum = 0
    diff = 0
    # Caluculate the required extra 1's to satisfy curent c^i
    #for r in range(nodes-1, -1, -1):
    #    #c_sum += matrix[r][c]
    diff = column[c] - col_cnt[c]
    if diff < 0:
        # We've extra more 1's in c^i than required. Hence matrix not feasible
        #print ("More 1's")
        feasible = False
        #print ("%d %d %d\n" % (c_sum, column[c], diff))
        break
    elif diff == 0:
        # We've exact 1's in c^i, move to next column.
        #print ("Exact 1's")
        #print ("%d %d %d\n" % (c_sum, column[c], diff)) 
        continue
    elif diff > 0:
        # We've less 1's in c^i than required, pull from c^i-1
        #print("Less 1's")
        #print ("%d %d %d\n" % (c_sum, column[c], diff))
        c_prev = c - 1
        r_prev = col_cnt[c_prev] - 1
        while (diff > 0):
            # if there are no 1's in c_prev that can be traded, then move c_prev to left
            if r_prev < 0:
                c_prev -= 1
                if c_prev < 0:
                    # matrix is not possible
                    feasible = False
                    break
                r_prev = col_cnt[c_prev] - 1
                continue
            # trade r_prev for the 0 in the c, update col_cnt for both c and c_prev
            # if we've 1 in c, then simply move to next 1 in c_prev by r_prev--
            if matrix[r_prev][c] == 0:
                assert matrix[r_prev][c_prev] == 1
                matrix[r_prev][c] = 1
                matrix[r_prev][c_prev] = 0
                r_prev -= 1
                col_cnt[c_prev] -= 1
                diff -= 1
            else:
                r_prev -= 1
        if feasible == False:
            break
    # If we're still short of 1's for c^i then matrix is not feasible
    #print ("after")
    #print numpy.array(matrix)       
    #print ("diff % d \n" % diff)
    if diff > 0:
        feasible = False
        break
#if feasible:
    #print ("Matrix possible")
#else:
    #print ("Matrix impossible")
    #print numpy.array(matrix)

# Re-arrange rows and columns according to original r^i and c^i sequence
# only if matrix is possible
if feasible:
    pos = 0
    temp=[0 for x in range(nodes)]
    temp1 = 0
    # re-arrage rows first
    for r1 in range(0, nodes):
        pos = 0
        for r in range(r1, nodes):
            if (row1[r1] == row[r]):
                pos = r
                break
        # move row r to r1
        temp1 = row[r]
        row[r] = row[r1]
        row[r1] = temp1
        for i in range (0, nodes):
            temp[i] = matrix[r1][i]
            matrix[r1][i] = matrix[pos][i]
            matrix[pos][i] = temp[i]
        #print ("r=%d shifted to r1=%d" %(pos, r1))
        
    # re-arrange columns next
    for c1 in range(0, nodes):
        pos = 0
        for c in range(c1, nodes):
            if (column1[c1] == column[c]):
                pos = c
                break
        # move column c to c1
        temp1 = column[c]
        column[c] = column[c1]
        column[c1] = temp1
        for j in range (0, nodes):
            temp[j] = matrix[j][c1]
            matrix[j][c1] = matrix[j][pos]
            matrix[j][pos] = temp[j]
        #print ("c=%d shifted to c1=%d" %(pos, c1))
    #print row
    #print column
    #print numpy.array(matrix)

# Dump the output to output.txt
output = open('./output.txt', 'w')
if feasible:
    output.write(str(1) + "\n")
    for r in range(0, nodes):
        for c in range(0, nodes):
            if c < nodes - 1:
                output.write(str(matrix[r][c]) + ",")
            else:
                output.write(str(matrix[r][c]) + "\n")
else:
    output.write(str(0) + "\n")
#print result
#output.write(result)
output.close()

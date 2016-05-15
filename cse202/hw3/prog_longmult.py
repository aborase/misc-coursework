import re
import time
# Read data from input file
#print ("Read input.txt")

line = open('./input.txt','r').readlines()

# Extract bit size
nbits = int(line[0])
#print (nbits)

#A = bin(int(line[1], 2))
#B = bin(int(line[2], 2))
A = line[1][0:nbits]
B = line[2][0:nbits]

#print (A)
#print (B)

start1 = time.time()
#def naive_mul_2_binary(A, B, nbits):
C = A
D = '0'
for i in range(nbits-1, -1, -1):
    if (B[i] == '1'):
        #print(D)
        #D = add_2_binary(D, C)
        len1 = max(len(C), len(D))
        C = C.zfill(len1)
        #print(len1)
        #print (A)
        D = D.zfill(len1)
        #print (B)
        temp = ''
        #C = ['' for i in range(0, len1)]
        carry = 0
        sum1 = 0
        for i in range(len1-1, -1, -1):
            sum1 = carry
            carry = 0
            if (D[i] == '1'):
                sum1 += 1
            if (C[i] == '1'):
                sum1 += 1

            if ((sum1 % 2) == 1):
                temp = '1' + temp
            else: 
                temp = '0' + temp
            #print (sum1)
            if ((sum1 / 2) >= 1):
                carry = 1
            #print (carry)
            #print (C) 
        if (carry == 1): 
            temp = '1' + temp 
        #print (C)
        D = temp 
    C += '0'
    
#print(D)
#return D


#print (naive_mul_2_binary(A, B, nbits))
end1 = time.time()
#print (end1-start1)
# strip leading 0's from result
#first_1 = 0
#for i in range(2*nbits):
#   if (D[i] == '0'):
#        continue
#    else:
#       first_1 = i
#        break
#out = D[first_1:] + "\n"
#print(out)

# write result to output file
output = open('./output.txt', 'w')
output.write((D + "\n"))
output.close()

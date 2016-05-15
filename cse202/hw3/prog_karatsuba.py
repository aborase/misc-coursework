import re
import time

# Read data from input file
#print ("Read input.txt")
line = open('./input.txt','r').readlines()

# Extract bit size
nbits = int(line[0])
#print (nbits)

A = line[1][0:nbits]
B = line[2][0:nbits]

def add_2_binary(A, B):
    len1 = max(len(A), len(B))
    A = A.zfill(len1)
    #print(len1)
    #print (A)
    B = B.zfill(len1)
    #print (B)
    C = ''
    #C = ['' for i in range(0, len1)]
    carry = 0
    sum1 = 0
    for i in range(len1-1, -1, -1):
        sum1 = carry
        carry = 0
        if (A[i] == '1'):
            sum1 += 1
        if (B[i] == '1'):
            sum1 += 1
        
        if ((sum1 % 2) == 1):
            C = '1' + C
        else:
            C = '0' + C
        #print (sum1)
        if ((sum1 / 2) >= 1):
            carry = 1
        #print (carry)
        #print (C)
    if (carry == 1):
        C = '1' + C
    #print (C)
    return C.zfill(len1)

def sub_2_binary(A, B):
    len1 = max(len(A), len(B))
    #print(len1)
    A = A.zfill(len1)
    #print (A)
    B = B.zfill(len1)
    #print (B)
    C = ''
    #C = ['' for i in range(0, len1)]
    borrow = 0
    borrow_next = 0
    sub1 = 0
    for i in range(len1-1, -1, -1):
        if (B[i] == '1'):
            if (A[i] == '1'):
                if (borrow == 1):
                    sub1 = 1
                    borrow_next = 1
                else:
                    sub1 = 0
                    #borrow_next = 0
            else:
                if (borrow == 1):
                    sub1 = 0
                    borrow_next = 1
                else:
                    sub1 = 1
                    borrow_next = 1
        else:
            if (A[i] == '1'):
                if (borrow == 1):
                    sub1 = 0
                    #borrow_next = 0
                else:
                    sub1 = 1
                    #borrow_next = 0
            else:
                if (borrow == 1):
                    sub1 = 1
                    borrow_next = 1
                else:
                    sub1 = 0
                    #borrow_next = 0
        if (sub1 == 1):
            C = '1' + C
        else:
            C = '0' + C
        borrow = borrow_next
        borrow_next = 0
        #print (C)
        #print (sub1)
        #print (borrow)
    if (borrow == 1):
        print ("\n ERROR: borrow should not be 1 \n")
    #print (C)
    return C.zfill(len1)

def mul_2_binary(A, B):
    #print (len(A))
    #print (len(B))
    len2 = max(len(A), len(B))
    #print (len2)
    if (len2 == 1):
        if ((A == '1') & (B == '1')):
            #print ("A:%s, B:%s, Result:'1'" % (A, B))
            return '1'
        else:
            #print ("A:%s, B:%s, Result:'0'" % (A, B))
            return '0'

    len1 = int(len2 / 2)
    #l2 = len2 - l1

    A = A.zfill(len2)
    B = B.zfill(len2)
    
    # (A1+A2)*(B1+B2) = TERM1
    A_sum = add_2_binary(A[0:len1], A[len1:])
    #print ("A1: %s, A2: %s, A_sum: %s \n" % (A[0:len1], A[len1:], A_sum))
    
    B_sum = add_2_binary(B[0:len1], B[len1:])
    #print ("B1: %s, B2: %s, B_sum: %s \n" % (B[0:len1], B[len1:], B_sum))
    
    TERM1 = mul_2_binary(A_sum, B_sum)
    #print ("A_sum: %s, B_sum: %s Term1: %s \n" % (A_sum, B_sum, TERM1))
    
    # (A1*B1 + A2*B2) = TERM2
    A1_B1 = mul_2_binary(A[0:len1], B[0:len1])
    #print ("A1: %s, B1: %s A1_B1: %s \n" % (A[0:len1], B[0:len1], A1_B1))
    
    A2_B2 = mul_2_binary(A[len1:], B[len1:])
    #print ("A2: %s, B2: %s A2_B2: %s \n" % (A[len1:], B[len1:], A2_B2))
    
    TERM2 = add_2_binary(A1_B1, A2_B2)
    #print ("A1_B1: %s, A2_B2: %s Term2: %s \n" % (A1_B1, A2_B2, TERM2))
    
    # (A1*B2 + A2*B1) = TERM3 = TERM1 - TERM2
    TERM3 = sub_2_binary(TERM1, TERM2)
    #print ("TERM1: %s, TERM2: %s C: %s \n" % (TERM1, TERM2, TERM3))
    
    # Result = A1_B1*2^len2 + TERM3*2^len1 + A2_B2
    for i in range(2*(len2-len1)):
        A1_B1 += '0'
    #print("A1_B1*2^n: %s" % A1_B1)
    
    for i in range(len2 - len1):
        TERM3 += '0'
    #print("TERM3*2^n-1: %s" % TERM3)
    
    TERM4 = add_2_binary(A1_B1, TERM3)
    #print("TERM4: %s" % TERM4)
    
    result = add_2_binary(TERM4, A2_B2)
    #print ("A:%s, B:%s, Result:%s" % (A, B, result))
    return result

start = time.time()
result = mul_2_binary(A, B)
end = time.time()
#print ("Multiplication: %s \n" % result)
# strip leading 0's from result
first_1 = 0
for i in range(2*nbits):
    if (result[i] == '0'):
        continue
    else:
        first_1 = i
        break
out = result[first_1:] + "\n"
#print(out)
#print (end-start)

# write result to output file
output = open('./output.txt', 'w')
output.write(out)
output.close()

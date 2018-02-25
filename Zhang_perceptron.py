#!/usr/bin/python
import os
import re
import getopt
import sys

# Parser training data 
with open('/u/cs246/data/adult/a7a.train', 'r') as f:
    lines = f.readlines()
    line_num = len(lines)
    #print lines
    #print line_num
    
training_data = [[[0 for i in range(123)], 1] for i in range(line_num)]

for i in range(line_num):
    if lines[i][0] == '+':
        training_data[i][1] = 1
    else:
        training_data[i][1] = -1
    digit =  re.findall(r'(\w*[0-9]+)\w*',lines[i])     # Get the digital numbers in every line 
    # print digit
    index =  digit[1::2]        # The even bits of digit are the indexes of features whose value is 1  
    # print index
    for j in index: 
        training_data[i][0][int(j)-1] = 1

# Parser test data
with open('/u/cs246/data/adult/a7a.test', 'r') as f:
    lines = f.readlines()
    line_num = len(lines)
    # print lines
    # print line_num
    
test_data = [[[0 for i in range(123)], 1] for i in range(line_num)]

for i in range(line_num):
    if lines[i][0] == '+':
        test_data[i][1] = 1
    else:
        test_data[i][1] = -1
    digit =  re.findall(r'(\w*[0-9]+)\w*',lines[i])     # Get the digital numbers in every line 
    # print digit
    index =  digit[1::2]        # The even bits of digit are the indexes of features whose value is 1  
    # print index
    for j in index: 
        test_data[i][0][int(j)-1] = 1

# Initialization 
w = [0.0 for i in range(123)]
b = 0
iterations = 1
 
# Update w&b
def update(item):
    global w, b
    for i in range(123):
        w[i] = w[i] + 1 * item[1] * item[0][i]
    b = b + 1 * item[1]
    # print w, b # you can uncomment this line to check the process of stochastic gradient descent
 
# Calculate the distance between item and dicision surface
def dis(item):
    global w, b
    res = 0
    for i in range(len(item[0])):
        res += item[0][i] * w[i]
    res += b
    res *= item[1]
    return res
 
# One learning loop, break if perfectly classify training_data
def check():
    flag = False
    for item in training_data:
        if dis(item) <= 0:
            flag = True
            update(item)
    if not flag:
        #print "Feature weights (bias last): " + str(w) + str(b))
        os._exit(0)
    flag = False
    
# Command Line Argument
def main(argv):
    global iterations
    try:
        opts, args = getopt.getopt(argv, "",["noDev","iterations="])
    except getopt.GetoptError:
        print 'Error: '
        sys.exit(2)
    for opt, arg in opts:
        if opt == "--iterations":
            iterations = arg
    #print iterations
 
if __name__=="__main__":
    main(sys.argv[1:])
    #print iterations
    for i in range(int(iterations)):
        check()
    
# Calcualte the Test Accuracy
correct = 0.000000000000
for item in test_data:
    if dis(item) > 0:
        correct = correct + 1
accuracy = correct / len(test_data)

#Output 
print "Test accuracy: " + str(accuracy)
print "Feature weights (bias last): " + str(w) + str(b)
    
    

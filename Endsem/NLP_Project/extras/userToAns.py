import json
from pprint import pprint

import csv
zeroAns = []
morethan2Ans = []
with open('user_to_ans_count.json') as data_file:
	data = json.load(data_file)
	for items in data:
		zeroAns.append(data[items]['no_ans'])
		morethan2Ans.append(data[items]['more_than_2_ans'])
#print zeroAns

import matplotlib.pyplot as plt
import numpy as np
arr = plt.hist(zeroAns, bins=20, width=1)#range(min(scores), max(scores) + 1000, 1000))

plt.xlabel('Questions with Zero Answers')
plt.ylabel('Number of Users')
# plt.show()
for i in range(10):
    plt.text(arr[1][i],arr[0][i],str(arr[0][i]))
plt.show()

arr = plt.hist(morethan2Ans, bins=20, width=10)#range(min(scores), max(scores) + 1000, 1000))

plt.xlabel('Questions with More than 2 Answers')
plt.ylabel('Number of Users')
# plt.show()
for i in range(10):
    plt.text(arr[1][i],arr[0][i],str(arr[0][i]))
plt.show()

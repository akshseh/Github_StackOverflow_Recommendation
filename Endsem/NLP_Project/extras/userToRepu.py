import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

import csv
repu = []
with open('user_to_reputation.json') as data_file:
	data = json.load(data_file)
	print data
	for items in data:
		repu.append(data[items])

repu1 = [int(i) for i in repu]
#print repu1
print min(repu1)
print max(repu1)

finScores = []
for score in repu1:
	if score < 10000:
		finScores.append(score)

rep = np.array(finScores)
arr = plt.hist(finScores, bins=20, facecolor='blue', width=200)

# rep_bins = np.bincount(rep)
# print rep_bins
# x = []
# y = []
# for i,j in enumerate(rep_bins):
# 	x.append(i)
# 	y.append(j)
# arr = plt.scatter(x,y)
for i in range(20):
    plt.text(arr[1][i],arr[0][i],str(arr[0][i]))
plt.ylabel('Number of Users')
plt.xlabel('StackOverflow Reputations')
plt.show()

import json
from pprint import pprint
import numpy as np
import csv

scores = []
with open('user_to_score.json') as data_file:    
    data = json.load(data_file)
    print data.keys()
#     for items in data:
#     	#scores.append(data['items'])
# 		scores.append(data[items])
# maxScore = max(scores)
# print min(scores)
# print maxScore

# scores = [x-min(scores) for x in scores]

# print min(scores)
# print max(scores)

# import matplotlib.pyplot as plt
# import numpy as np
# print scores
# # finScores = []
# # for score in scores:
# # 	if score < 10000:
# # 		finScores.append(score)
# # sc = np.array(finScores)
# # sc1 = np.bincount(sc)
# # x = []
# # y = []
# # for i,item in enumerate(sc1):
# # 	x.append(i)
# # 	y.append(item)

# # plt.scatter(x,y)

# # plt.show()

# arr = plt.hist(scores, bins=10, width=5000)#range(min(scores), max(scores) + 1000, 1000))
# for i in range(10):
#     plt.text(arr[1][i],arr[0][i],str(arr[0][i]))
# plt.ylabel('Number of Users')
# plt.xlabel('Score from SO')
# plt.show()

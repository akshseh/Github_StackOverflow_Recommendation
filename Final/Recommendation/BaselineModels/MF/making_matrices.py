#Making user-feature, item-feature matrices for LightFM reccomendation system
import json
import csv
import numpy as np
import pickle
import pymongo
import json
from pymongo import MongoClient
import requests.packages.urllib3
import numpy as np
requests.packages.urllib3.disable_warnings()


#Reading Input
input_1 = '../../../Dataset/username_userID.csv'
input_2 = '../../../Dataset/repo_user.json'
input_3 = '../../../Dataset/languages_repo.json'
input_4 = '../../../Dataset/finout.csv'


#Creating list of users
with open(input_1, 'rb') as file_input:
	file_read = csv.reader(file_input)
	users_set = set()
	for row in file_read:
		repo_url = row[0]
		users_set.add(repo_url)
user_list = list(users_set) 


#Creating list of repos
with open(input_2) as file_input:
	repos_present = set()
	for row in file_input:
		# data.append(json.loads(line))
		t = (json.loads(row))
		repo_link = t['repo']
		for i in repo_link:
			repos_present.add(i)
repos_list = list(repos_present)



#Creating list of languages
with open(input_3) as file_input:
	langauges = set()
	for row in file_input:
		t = (json.loads(row))
		lang_dict = t['lang']
		for i in lang_dict:
			keys = i.keys()
			for j in keys:
				langauges.add(j)
languages_as_feaures = list(langauges)



#Generating repo_vs_users: user_item matrix
repo_vs_user = np.zeros((len(repos_list),len(user_list)))

with open(input_2) as repo_map:
	with open(input_1,'rb') as users_name:
		name_of_users = csv.reader(users_name)

		for i,name_1 in zip(repo_map,name_of_users):
			name = name_1[0]
			user_index = user_list.index(name)
			repos = (json.loads(i))
			repo_names = repos['repo']
			for j in repo_names:
				repo_index = repos_list.index(j)
				repo_vs_user[repo_index][user_index] = 1


#Generating repo_vs_language: user_feature matrix
repo_vs_language = np.zeros((len(repos_list),len(languages_as_feaures)))

with open(input_2) as repo_map:
	with open(input_3) as language_map:
		for i,j in zip(repo_map,language_map):
			repos = (json.loads(i))
			repo_names = repos['repo']

			lang_1 = (json.loads(j))
			langs = lang_1['lang'] 


			for x,y in zip(repo_names,langs):	
				repo_index_new = repos_list.index(x)
				keys_new = y.keys()
				for k in keys_new:
					language_index=languages_as_feaures.index(k)
					value = y[k]
					if(type(value) == int):
						value = int(value)
						repo_vs_language[repo_index_new][language_index] = value




'''stact_overflow_mapping_1 = np.zeros((len(user_list)))
stack_overflow_mapping = stact_overflow_mapping_1.tolist()
print " Working "


with open(input_4, 'rb') as file_input:
	file_read = csv.reader(file_input)
	for row in file_read:
		if row[1] in user_list:
			index_val = user_list.index(row[1])
			stack_overflow_mapping[index_val] = row[0]'''


# Connect to MongoDB
client = MongoClient("hpc.iiitd.edu.in", 27017, maxPoolSize=50)

# Connect to db tweets
db=client.nlpprojects

#db.repos.update({'name':'square'}, {$unset: {'starredUsers':1}}, false, true);

# Collection - users
collection=db['nlp']

cursor = collection.find({}, no_cursor_timeout=True)



features=[]
languages=[]
languages_set_new = set()
count=0
for v in cursor:
	if v['name'] in user_list:
		for i in v['features']:
			languages_set_new.add(i)
language_list_new = list(languages_set_new)


#Generating user_language matrix : item_feature matrix
user_vs_languages = np.zeros((len(user_list),len(language_list_new)))

new_cursor = collection.find({}, no_cursor_timeout=True)

for v in new_cursor:
	if v['name'] in user_list:
		user_index_now = user_list.index(v['name']) 
		for i in v['features']:
			language_index_now = language_list_new.index(i) 
			count_val = v['features'][i]
			user_vs_languages[user_index_now][language_index_now] = count_val


#Train Test split of 80-20
trainX = user_list[int(0.8*len(user_list)):]
trainY = user_list[int(0.8*len(repos_list)):]
trainY_1 = user_list[:int(0.8*len(repos_list))]



#Saving Model
f = open('Model/first.txt', 'w')
pickle.dump(user_vs_languages, f)
f.close()

f = open('Model/second.txt', 'w')
pickle.dump(repo_vs_language, f)
f.close()

f = open('Model/third.txt', 'w')
pickle.dump(repo_vs_user, f)
f.close()

with open("Model/lang.dat", "wb") as f:
	pickle.dump(languages_as_feaures, f)


with open("Model/repo_vs_language.dat", "wb") as f:
	pickle.dump(repo_vs_language, f)

import pymongo
import json
from pymongo import MongoClient
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

import numpy as np
import csv


features=[]
languages=[]
userno=0
client = MongoClient("hpc.iiitd.edu.in", 27017)

db=client.nlpprojects

usersDone = []
allUsers = db.nlp.find({},no_cursor_timeout=True)
for users in allUsers:
    usersDone.append(users['name'])

with open('finList.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    for row in readCSV:
        githubName = row[1]
        if githubName not in usersDone:
            print githubName
            #print "Searching repos for user " + str(v['user'])
            repoList = []
            languages1=[]
            #userResponse = requests.get('https://api.github.com/user/' + githubID + '?client_id=4847f3d8493451998aa5&client_secret=7ed325919a2211f4d0c7c688044750e9d64d8688')
            #print githubID
            #userName = userResponse.json()['login']
            


            try:
                page1 = 1
                while True:
                    
                    reposList = requests.get('https://api.github.com/users/' + githubName + '/repos?client_id=4847f3d8493451998aa5&client_secret=7ed325919a2211f4d0c7c688044750e9d64d8688&page=' + str(page1))
                    
                    if not reposList.json():
                        break
                    page2=1
                    for repo in reposList.json():
                        langs = requests.get('https://api.github.com/repos/' + githubName + '/'+repo['name']+'/languages'+'?client_id=4847f3d8493451998aa5&client_secret=7ed325919a2211f4d0c7c688044750e9d64d8688&page=' + str(page2))
                        if(not langs.json()):
                            break;
                        #print(langs.json())
                        for lang in langs.json():
                            languages1=languages1+[lang]
                        page2=page2+1

                    page1 = page1 + 1
                #print('len',len(np.hstack(np.array(languages1))))
                if(len(np.hstack(np.array(languages1)))<5):
                    continue
                f1={}
                langs=set(np.hstack(np.array(languages1)))
                for feature in langs:
                    f1[str(feature)]=languages1.count(feature)
                print(userno)
                userno=userno+1
                #db.user_features.insert_one({'name':githubName, 'features':f1})
                db.nlp.insert_one({'name':githubName,'features':f1})
                #languages=languages+[languages1]
                #features=features+languages
            except Exception,e:
                    #print str(e)
                    continue
print(languages)


feature_set=[]
index=0
features=set(np.hstack(np.array(features)))


'''
for f in languages:
    f1={}
    for feature in features:
        f1[str(feature)]=f.count(feature)
    feature_set=feature_set+[f1]
    db.user_features.insert_one(f1)
print(feature_set)
'''

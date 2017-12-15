import pymongo
import json
from pymongo import MongoClient
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

import numpy as np
import csv
import sys
import ConfigParser

#This file creates user-language feature generation
if len(sys.argv) < 2:
    print """
        Command : python userLanguages.py <inp-file> <settings-file>
        (IN OUR CASE)
        python userLanguages.py ../../Dataset/username_userID.csv ../settings.txt
    """
    sys.exit(1)

# Reading argv input
inp_file = sys.argv[1]
settings_file = sys.argv[2]


# Read config settings
config = ConfigParser.ConfigParser()
config.readfp(open(settings_file))

features=[]
languages=[]
userno=0

# Connect to the mongo server
client = MongoClient("hpc.iiitd.edu.in", 27017)

# Mongo DB name
db=client.nlpprojects

usersDone = []

# Find list of users done
# allUsers = db.nlp.find({},no_cursor_timeout=True)
# for users in allUsers:
#     usersDone.append(users['name'])

with open(inp_file) as csvfile:
    readCSV = csv.reader(csvfile)

    # Iterate each username in GitHub
    for row in readCSV:
        githubName = row[0]
        print githubName

        languages1=[]
        try:
            page1 = 1
            while True:
                
                # Get list of repos for a user
                reposList = requests.get('https://api.github.com/users/' + githubName + '/repos?client_id='+config.get('GitHub API keys', 'github_client_id')+'&client_secret=' + config.get('GitHub API keys', 'github_client_secret') +'&page=' + str(page1))
                #print reposlist.json()
                if not reposList.json():
                    break
                page2=1

                # Get list of languages for a particular repo
                for repo in reposList.json():
                    langs = requests.get('https://api.github.com/repos/' + githubName + '/'+repo['name']+'/languages'+'?client_id='+config.get('GitHub API keys', 'github_client_id')+'&client_secret=' + config.get('GitHub API keys', 'github_client_secret') +'&page=' + str(page1))
                    if(not langs.json()):
                        break;
                    for lang in langs.json():
                        languages1=languages1+[lang]
                    page2=page2+1

                page1 = page1 + 1

            if(len(np.hstack(np.array(languages1)))<5):
                continue
            f1={}
            langs=set(np.hstack(np.array(languages1)))
            for feature in langs:
                f1[str(feature)]=languages1.count(feature)
            print(userno)
            userno=userno+1
            print "Features: " + str(f1)
            
            db.final_nlp.insert_one({'name':githubName,'features':f1})
           
        except Exception,e:
                print str(e)
                continue
# print(languages)


# feature_set=[]
# index=0
# features=set(np.hstack(np.array(features)))


# '''
# for f in languages:
#     f1={}
#     for feature in features:
#         f1[str(feature)]=f.count(feature)
#     feature_set=feature_set+[f1]
#     db.user_features.insert_one(f1)
# print(feature_set)
# '''

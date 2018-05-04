import requests
import json
import csv

import urllib2

#Writing output json file 
def write_to_out_file(out_data):
	with open('user_languages_repo.json','a') as file_out:
		json.dump(out_data,file_out)
		file_out.write('\n')
# Extrraction of Git-Hub user info





def extract_user_info(object):
	repo_link = object['repo']

	langauge_of_repo_json = {
		 	'lang' : []
		}
	for i in repo_link:
		
		final_call = i + '/languages'
		language_data = requests.get(final_call+'?client_id=4847f3d8493451998aa5&client_secret=7ed325919a2211f4d0c7c688044750e9d64d8688&')
		language_data_json = json.loads(language_data.text or language_data.content)
		langauge_of_repo_json['lang'].append(language_data_json)
	print "______-_________________________________" 
	write_to_out_file(langauge_of_repo_json)
	'''for i in repo_data_json:
		data = i['url']
		language_of_users_repo['languages'].append(data)
	print''' 


#extract_user_info("https://api.github.com/repos/Sinha-Raunak/ELD3/languages")

data = []

with open('repo_user.json') as file_input:
	print "Started Reading"
	for row in file_input:
		# data.append(json.loads(line))
		t = (json.loads(row))
		extract_user_info(t)
		
# Wrting a csv file 
# login , Date of creation of account, followers, following, gists, stared url, , organisation url, repos_url, company, email,

##Requests
#r = requests.get('https://api.github.com/repos/django/django')
#def extract_use_info(user_link):
#	r = requests.get(user_link)
#	if(r.ok):
 #   	repoItem = json.loads(r.text or r.content)
  #  	print "Django repository created: " + repoItem['created_at']

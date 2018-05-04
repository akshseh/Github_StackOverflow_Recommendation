import requests
import json
import csv

#Writing output json file 
def write_to_out_file(out_data):
	with open('output_github.json','a') as file_out:
		json.dump(out_data,file_out)
		file_out.write('\n')
# Extrraction of Git-Hub user info
def extract_user_info(user_link):
	user_data = requests.get(user_link)
	if(user_data.ok):
		user_data_json = json.loads(user_data.text or user_data.content)
		#user_info = ""
		#user_info = user_info + user_data_json['login'] +',' #login 
		#user_info = user_info + user_data_json['created_at']+',' #Date of creation
		#user_info = user_info + str(user_data_json['followers'])+',' #Number of followers
		#user_info = user_info + str(user_data_json['following'])+',' #Number of following
		#user_info = user_info + user_data_json['followers_url']+',' #Set of URL of followers
		#user_info = user_info + user_data_json['following_url']+',' #Set of URL of following
		#print "HAHHAHAHAH:" + user_info
		user_info = {
			'login' : user_data_json['login'],
			'date_created' : user_data_json['created_at'],
			'number_followers' : user_data_json['followers'],
			'number_following' : user_data_json['following'],
			'followers_url' : user_data_json['followers_url'], # Use GitHub API to find username , ID 
			'following_url' : user_data_json['following_url'],
			'public_repo_count' :  user_data_json['public_repos'],
			'public_gist_count' : user_data_json['public_gists'],
			'repo_url' : user_data_json['repos_url'],
			'gists_url' : user_data_json['gists_url'],
			'organizations_url' : user_data_json['organizations_url'],
			'email' : user_data_json['email']


		}
		write_to_out_file(user_info)
		print "HERE"

#Reading input csv file
with open('common_users.csv', 'rb') as file_input:
	print "Started"
	file_read = csv.reader(file_input)
	for row in file_read:
		user_link_search = 'https://api.github.com/user/'+row[1]
		extract_user_info(user_link_search)




# Wrting a csv file 
# login , Date of creation of account, followers, following, gists, stared url, , organisation url, repos_url, company, email,

##Requests
#r = requests.get('https://api.github.com/repos/django/django')
#def extract_use_info(user_link):
#	r = requests.get(user_link)
#	if(r.ok):
 #   	repoItem = json.loads(r.text or r.content)
  #  	print "Django repository created: " + repoItem['created_at']

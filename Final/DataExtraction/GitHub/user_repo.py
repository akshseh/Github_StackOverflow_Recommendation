import requests
import json
import csv
import urllib2
import ConfigParser
import sys
#This file extracts the repolist of each user in a file
if len(sys.argv) < 4:
    print """
        Command : python user_repo.py <input-file : links of repository> <output-file> <settings-file>
        (IN OUR CASE)
        python user_repo.py ../../Dataset/githubID-stackID.csv repo_user.csv ../settings.txt
    """
    sys.exit(1)

#Reading argv input
input_file = sys.argv[1]
output_file = sys.argv[2]
settings_file = sys.argv[3]


# Read config settings
config = ConfigParser.ConfigParser()
config.readfp(open(settings_file))

#Funtion to write output 
def write_to_out_file(out_data):
	with open(output_file,'a') as file_out:
		json.dump(out_data,file_out)
		file_out.write('\n')

#Fucntion for Extracting of Git-Hub Repo-list for each User in Input
def extract_user_info(user_link):
	repo_data = requests.get(user_link+'?client_id='+config.get('GitHub API keys', 'github_client_id')+'&client_secret=' + config.get('GitHub API keys', 'github_client_secret') +'&')
	repo_data_json = json.loads(repo_data.text or repo_data.content)
	repo_of_users_json = {
		 	'repo' : []
		}
	for i in repo_data_json:
		repo_link = i['url']
		repo_of_users_json['repo'].append(repo_link)
	write_to_out_file(repo_of_users_json)

with open(input_file, 'rb') as file_input:
	print "Started Reading"
	file_read = csv.reader(file_input)
	for row in file_read:
		repo_url ='https://api.github.com/user/'+row[0].split(";")[0]+'/repos'
		extract_user_info(repo_url)


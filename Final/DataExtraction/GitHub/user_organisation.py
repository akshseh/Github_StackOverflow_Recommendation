import requests
import json
import csv
import urllib2
import ConfigParser
import sys
#This file extracts the organisation-list of each user in a file
if len(sys.argv) < 4:
    print """
        Command : python user_organisation.py  <input-file : links of repository> <output-file> <settings-file>
        (IN OUR CASE)
        python user_organisation.py ../../Dataset/githubID-stackID.csv ../../Dataset/org_user.json ../settings.txt
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

#Fucntion for Extracting of Git-Hub Organisation-list for each User in Input
def extract_user_info(user_link,github_id):
	org_data = requests.get(user_link+'?client_id='+config.get('GitHub API keys', 'github_client_id')+'&client_secret=' + config.get('GitHub API keys', 'github_client_secret') +'&')
	org_data_json = json.loads(org_data.text or org_data.content)
	org_of_users_json = {
			'github_id' : github_id,
		 	'organizations_url' : []
		}
	for i in org_data_json:
		org_link = i['url']
		org_of_users_json['organizations_url'].append(org_link)
	write_to_out_file(org_of_users_json)

with open(input_file, 'rb') as file_input:
	print "Started Reading"
	file_read = csv.reader(file_input)
	for row in file_read:
		org_url ='https://api.github.com/user/'+row[0].split(";")[0]+'/orgs'
		extract_user_info(org_url,row[0].split(";")[0])

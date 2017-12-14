import requests
import json
import csv
import urllib2
import ConfigParser
import sys
# This file extracts list of languages used in a Git-Hub Repository
if len(sys.argv) < 4:
    print """
        Command : python repo_languages.py <input-file : links of repository> <output-file> <settings-file>
        (IN OUR CASE)
        python repo_languages.py ../../Dataset/repo_user.json ../../Dataset/languages_repo.json ../settings.txt
    """
    sys.exit(1)

#Reading Python argv input
input_file = sys.argv[1]
output_file = sys.argv[2]
settings_file = sys.argv[3]

# Read config settings
config = ConfigParser.ConfigParser()
config.readfp(open(settings_file))

#Function to write output 
def write_to_out_file(out_data):
	with open(output_file,'a') as file_out:
		json.dump(out_data,file_out)
		file_out.write('\n')

#Extracting Git-Hub languages of each repository
def extract_user_info(object):
	repo_link = object['repo']
	langauge_of_repo_json = {
		 	'lang' : []
		}
	for i in repo_link:
		final_call = i + '/languages'
		language_data = requests.get(final_call+'?client_id='+config.get('GitHub API keys', 'github_client_id') + '&client_secret=' + config.get('GitHub API keys', 'github_client_secret')+'&')
		language_data_json = json.loads(language_data.text or language_data.content)
		langauge_of_repo_json['lang'].append(language_data_json)
	write_to_out_file(langauge_of_repo_json)

data = []

with open(input_file) as file_input:
	print "Started Reading"
	for row in file_input:
		t = (json.loads(row))
		extract_user_info(t)

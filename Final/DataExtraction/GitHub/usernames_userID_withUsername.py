import requests
import json
import csv
import ConfigParser
import sys
#Finding User name form Github User ID
if len(sys.argv) < 4:
    print """
        Command : python usernames_userID.py <input-file : links of repository> <output-file> <settings-file>
        (IN OUR CASE)
        python usernames_userID.py ../../Dataset/githubID-stackID.csv ../../Dataset/username_userID.csv ../settings.txt
    """
    sys.exit(1)
#Reading argv input
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


#Function to extract of Git-Hub user-ID
def extract_user_info(user_link, id):
	user_data = requests.get(user_link+'?client_id='+config.get('GitHub API keys', 'github_client_id')+'&client_secret=' + config.get('GitHub API keys', 'github_client_secret') +'&')
	#if(user_data.ok): Is this needed
	user_data_json = json.loads(user_data.text or user_data.content)
	username = user_data_json['login']
	
	write_to_out_file(str(id) + "," +  str(username))

#Function to read input file
with open(input_file, 'rb') as file_input:
	print "Started Reading"
	file_read = csv.reader(file_input)
	for row in file_read:
		user_link_search = 'https://api.github.com/user/'+row[0].split(";")[0]
		extract_user_info(user_link_search,row[0])


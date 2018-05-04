import requests
import json
import csv

import urllib2

#Writing output json file 
def write_to_out_file(out_data):
	with open('output_github.json','a') as file_out:
		json.dump(out_data,file_out)
		file_out.write('\n')
# Extrraction of Git-Hub user info


def get_api(url):
    try:
        request = urllib2.Request(GIT_API_URL + url)
        base64string = base64.encodestring('%s/token:%s' % (USER, API_TOKEN)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)
        result.close()
    except:
        print 'Failed to get api request from %s' % url



def extract_user_info(repo_link):
	language_data = requests.get(repo_link)
	language_data_json = json.loads(language_data.text or language_data.content)
	print language_data_json
	language_of_users_repo = {
		 	'languages' : []
		}
	'''for i in repo_data_json:
		data = i['url']
		language_of_users_repo['languages'].append(data)
	print''' 


extract_user_info("https://api.github.com/repos/Sinha-Raunak/Gti-Hub-Proposal/languages")




# Wrting a csv file 
# login , Date of creation of account, followers, following, gists, stared url, , organisation url, repos_url, company, email,

##Requests
#r = requests.get('https://api.github.com/repos/django/django')
#def extract_use_info(user_link):
#	r = requests.get(user_link)
#	if(r.ok):
 #   	repoItem = json.loads(r.text or r.content)
  #  	print "Django repository created: " + repoItem['created_at']

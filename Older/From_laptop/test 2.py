import requests
import json
import csv


#Writing Repo
def write_to_out_file(out_val):
	with open('repo_data_1.csv','ab') as f:
		writer=csv.writer(f)
		writer.writerow([out_val])

#Reading input csv file
with open('name.csv', 'rb') as file_input:
	print "Started Reading"
	file_read = csv.reader(file_input)
	for row in file_read:
		user_link_search = 'https://api.github.com/users/'+row[0]+'/repos'
		write_to_out_file(user_link_search)

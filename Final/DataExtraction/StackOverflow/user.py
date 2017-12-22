# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 17:55:42 2017

@author: karan
"""
import xml.etree.ElementTree as ET
import csv

def csv_dict_reader(file_obj): #reading the stackIDs
    """
    Read a CSV file using csv.DictReader
    """
    lst=[]
    reader = csv.reader(file_obj)
    for line in reader:
        
            
        a=line[0].split(';')
        lst.append(a[1])
       
    return lst  

def write_csv(csvfl,repo_dic): #writing the csv file
     with open(csvfl, 'w', newline='') as csvfile:
        fieldnames = ['StackID', 'Reputation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user in repo_dic:
            writer.writerow({'StackID': user, 'Reputation':repo_dic[user]})





def parse_post(row):  #parsing each row
    user=row.get('Id')
    repo=row.get('Reputation')
    
    return user,repo
    


def parse_posts(posts_path,dic):
    """
    Parameters: path to Posts.xml
    Output: written to parsed_data.txt
    """
    repodic={}
    posts_file = open(posts_path, "r", encoding="utf8")
    posts_file.readline()
    
    error_count = 0
    
    for line in posts_file:
            try:
                root = ET.fromstring(line)
                user,repo = parse_post(root)
            
                if user in dic: #for users common to github and stackoverflow
                    if user not in repodic: 
                        repodic[user]=repo 
                
                                
            except :
                error_count += 1
     
    posts_file.close()
    
    return repodic



if __name__ == "__main__":
    with open("githubID-stackID_25000.csv") as f_obj: 
        uids=csv_dict_reader(f_obj)
        
    repodic=parse_posts("Users.xml",uids)
    write_csv("top_tags.csv",repodic)
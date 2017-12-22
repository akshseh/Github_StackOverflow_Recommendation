# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 17:55:42 2017

@author: karan
"""
import xml.etree.ElementTree as ET
import csv,sys

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

def write_csv(csvfl,user,repo): #writing the csv file
     with open(csvfl, 'a', newline='') as csvfile:
        fieldnames = ['StackID', 'Reputation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'StackID': user, 'Reputation':repo})





def parse_post(row):  #parsing each row
    user=row.get('Id')
    repo=row.get('Reputation')
    
    return user,repo
    


def parse_posts(csvfl,posts_path,dic):
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
                        print(user,repo)
                        repodic[user]=repo
                        write_csv(csvfl,user,repo)
                        
                
                                
            except :
                error_count += 1
     
    posts_file.close()
    
    return repodic



if __name__ == "__main__":
    with open(sys.argv[1]) as f_obj: 
        uids=csv_dict_reader(f_obj)
        
    repodic=parse_posts(sys.argv[2],"Users.xml",uids)
    for user in uids:
        if user not in repodic:
            print("*"+str(user))
            write_csv(sys.argv[2],user,0)
    

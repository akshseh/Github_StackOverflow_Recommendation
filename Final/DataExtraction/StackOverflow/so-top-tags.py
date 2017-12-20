# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:32:19 2017

@author: karan
"""

import stackexchange,csv
 
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

def write_csv(csvfl,tag_dic):
     with open(csvfl, 'w', newline='') as csvfile:
        fieldnames = ['StackID', 'tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user in tag_dic:
            writer.writerow({'StackID': user, 'tags':tag_dic[user]})

def return_tags(lst_tag): #converting the tag object into a list of tag names
    lst=[]
    for tag in lst_tag:
        a=str(tag)
        a=a.split("'")
        lst.append(a[1])
    return lst
  


def top_tags(userdic,toptag_dic,key):
    
     so=stackexchange.Site(stackexchange.StackOverflow,key)
     count=0
     for user in userdic: 
         if user not in toptag_dic:
             if count<10000:        #each key allows only 100000 per day
                try:
                    u=so.user(user) #creating user object
                    count+=1
                    ans_tags=list(u.top_answer_tags.fetch())
                    ans_lst=return_tags(ans_tags)
                    ques_tags=list(u.top_question_tags.fetch())
                    ques_lst=return_tags(ques_tags)
                    toptag_dic[user]=ans_lst+[i for i in ques_lst if i not in ans_lst] #creating a dictionary of tags with users
                         
                except ValueError: #if user does not exist on stackoverflow
                    toptag_dic[user]=[]
                    count+=1
                    continue
                         
                         
             else:
                 count=0
                 break
     return toptag_dic                 
     
 
 
    
if __name__ == "__main__":
    with open("githubID-stackID_25000.csv") as f_obj:
        uids=csv_dict_reader(f_obj)
        
    key=['2d9juSFkFrvB7tHubprJWA((','mMHywYKQJjv)9wybCfHK)A((','kE)3IYDINqv)v)L4kC3Fqw((']
    user_top_tags={}
    for k in key:
        user_top_tags=top_tags(uids,user_top_tags,k)
    write_csv("top_tags.csv",user_top_tags)
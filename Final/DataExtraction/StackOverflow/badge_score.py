import csv
import sys
import xml.etree.ElementTree as ET
import os
#----------------------------------------------------------------------
def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    dic={}
    reader = csv.reader(file_obj)
    for line in reader:
       a=line[0].split(';')
       if a[1] not in dic:
           dic[a[1]]=[a[0]] #using stackIDs as key
    else:
        dic[a[1]].append(a[0]) #githubIDs were repeating
    return dic    

#---------------------------------------------------------------------
def parse_post(row):  #parsing each row
    user= row.get('UserId')
    badge=row.get('Name')
    
    return user,badge
    
    
#----------------------------------------------------------------------
def parse_posts(posts_path,dic):
    """
    Parameters: path to Posts.xml
    Output: written to parsed_data.txt
    """
    badgedic={}
    print("Parsing Posts.xml ...")
    posts_file = open(posts_path, "r")
    posts_file.readline()
    
    error_count = 0
    print(posts_file)
    # # CREATE NEW PARSED FILE
    dir_name = "ProcessedData"
    path = os.path.join(dir_name, "parsed_data.txt")

    if not os.path.exists("ProcessedData"):
        os.mkdir(dir_name)
    if os.path.exists(path):
        print("parsed_data.txt ALREADY EXISTS.. Skipping..")
        return
    parsed_file = open(path, "w")
    parsed_file.write("")
    parsed_file.close()

    parsed_file = open(path, "a")
    for line in posts_file:
        try:
            root = ET.fromstring(line)
            user,badge = parse_post(root)
            
            if user in dic: #for users common to github and stackoverflow
                if user not in badgedic: 
                    badgedic[user]=[badge] 
                else:
                    badgedic[user].append(badge) #creating a badge list for each user
            
            
        except:
            error_count += 1
        
     
    parsed_file.close()
    posts_file.close()
    
    return badgedic
#----------------------------------------------------------------------
def count_score(badgedic):
    scoredic={}
    bronze_badge=['Altruist','Benefactor', 'Curious','Investor','Nice Question', 'Popular Question', 'Promoter', 'Scholar', 'Student', 'Tumbleweed', 'Explainer', 'Nice Answer', 'Revival', 'Self-learner', 'Teacher','Autobiographer','Caucus', 'Commentator', 'Mortarboard', 'Precognitive', 'Quorum', 'Talkative', 'Citizen Patrol', 'Cleanup', 'Critic', 'Custodian', 'Disciplined', 'Editor', 'Excavator', 'Organizer', 'Peer Pressure', 'Proofreader', 'Suffrage', 'Supporter', 'Synonymizer', 'Tag Editor', 'Vox Populi', 'Analytical', 'Announcer', 'Informed','Bronze Badge'] 
    silver_badge=['Inquisitive', 'Favourite Question', 'Good Question','Notable Question', 'Notable Question', 'Enlightened', 'Refiner', 'Generalist', 'Guru','Good Answer', 'Necromancer', 'Tenacious', 'Constituent', 'Pundit', 'Enthusiast', 'Epic', 'Beta', 'Convention', 'Outspoken', 'Yearling', 'Deputy','Civic Duty', 'Reviewer', 'Strunk & White', 'Archaeologist', 'Sportsmanship', 'Research Assistant', 'Taxonomist', 'Booster', 'Census', 'Not a Robot', 'Documentation Beta', 'Documentation Pioneer', 'Documentation User', 'Silver Badge'] 
    gold_badge=['Socratic', 'Stellar Question', 'Great Question', 'Famous Question','Illuminator', 'Great Answer', 'Populist', 'Reversal', 'Unsung Hero','Fanatic', 'Legendary', 'Marshal', 'Constable', 'Sheriff', 'Steward', 'Copy Editor', 'Electorate', 'Publicist', 'Gold Badge' ]
    for user in badgedic:
        score=0
        for badge in badgedic[user]:
            if badge in bronze_badge: 
                score+=1 #score of 1 for each bronze badge
            elif badge in silver_badge:
                score+=2 #score of 2 for each silver badge
            elif badge in gold_badge:
                score+=3 #score of 3 for each gold badge
        scoredic[user]=score
    
    return scoredic
            
        
      

     
#----------------------------------------------------------------------
if __name__ == "__main__":
    with open("githubID-stackID_25000.csv") as f_obj:
        dic=csv_dict_reader(f_obj)
   
    xml_input_path = sys.argv[1]
    badgedic=parse_posts(xml_input_path,dic)
    
    badgedic
    
    for user in dic:
        if user not in badgedic:
            badgedic[user]=[]
    
    badge_score=count_score(badgedic)
    
    
    with open('badge_score.csv', 'w', newline='') as csvfile:
        fieldnames = ['StackID', 'badge_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user in badge_score:
            writer.writerow({'StackID': user, 'badge_score':badge_score[user]})
    
    
        


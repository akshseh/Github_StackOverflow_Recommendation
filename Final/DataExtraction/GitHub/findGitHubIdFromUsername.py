import csv, requests, time, sys
import ConfigParser

if len(sys.argv) < 4:
    print """
        Command : python findGitHubIdFromUsername.py <input-common-users-file> <output-file> <settings-file>

        (IN OUR CASE)
        python findGitHubIdFromUsername.py ../../Dataset/SOIntersectionGithub.csv out.csv ../settings.txt
    """
    sys.exit(1)

# Input and output file 
ifile = sys.argv[1]
ofile = sys.argv[2]
settingsFile = sys.argv[3]

# Write GitHubID-StackOverflowID in outFile
out_file = open(ofile,'w')

# Read config settings
config = ConfigParser.ConfigParser()
config.readfp(open(settingsFile))


with open(ifile) as csvfile:
    # Input file delimited by colon(;)
    readCSV = csv.reader(csvfile, delimiter=';')

    # Iterate each line
    for row in readCSV:
        
        githubEmailID = row[1]
        stackOverflowID = row[2]

        # Request GitHub API to get userId from email id
        idResponse = requests.get('https://api.github.com/search/users?client_id=' + config.get('GitHub API keys', 'github_client_id') + '&client_secret=' + config.get('GitHub API keys', 'github_client_secret') + '&q=' + githubEmailID + '%20in:email')
        
        try:
            # Get GitHub ID from response
            githubID = str(idResponse.json()['items'][0]['id'])

            # Write GitHub ID and StackOverflow ID to file
            out_file.write(githubID + ";" + str(stackOverflowID) + "\n")

            # Flush the intermediate output
            out_file.flush()
        except Exception as e:
            print str(e)

            # If user not found
            if str(e) == "list index out of range":
                print str(githubEmailID) + " -> User Not Found"
            else:
            # If api limit exceeded
                print "API Limit Exceeded"
                time.sleep(15)
                
out_file.close()

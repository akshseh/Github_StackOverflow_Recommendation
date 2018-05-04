import pickle
from lightfm import LightFM
from scipy.sparse import csr_matrix
import numpy as np
first=[]
second=[]
third=[]
users=[]
orgs=[]

# Read different matrices
with open('Model/first.txt') as f:
    first = pickle.load(f)

with open('Model/second.txt') as f:
    second = pickle.load(f)

with open('Model/third.txt') as f:
    third = pickle.load(f)

first=first[0:len(third)]
second=second[0:len(third)]


def normalise(array_to_normalise_inp):

    array_normalise = np.array([])
    for i in array_to_normalise_inp:
        array_normalise=np.append(array_normalise,i)
    max_value = np.amax(array_normalise)
    for i in range(len(array_to_normalise_inp)):
        for j in range(len(array_to_normalise_inp[i])):
            array_to_normalise_inp [i][j] = array_to_normalise_inp[i][j] / max_value
    return array_to_normalise_inp



model = LightFM(no_components=30,learning_rate=1.0e-40)

def sample_recommendation(model, data, user_ids,first1,second1):

    #number of users and movies in training data
    n_users, n_items = data.shape

    #generate recommendations for each user we input
    for user_id in user_ids:

        #movies they already like
        known_positives = np.nonzero(data[user_id])[0]
        print(user_id, np.arange(n_items))
        #movies our model predicts they will like
        scores = model.predict(user_id, np.arange(n_items), user_features=csr_matrix(first1), item_features=csr_matrix(second1))
        #print('scores',scores)
        #rank them in order of most liked to least
        top_items = np.argsort(-scores)

        #print out the results
        print("User %s" % user_id)
        print("     Known positives:")

        for x in known_positives[:3]:
            print("        %s" % x)#orgs[x]['name'])

        print("     Recommended:")

        for x in top_items[:3]:
            dist=0.0
            for o in known_positives:
                val=np.sqrt(sum((second[o]-second[x])*(second[o]-second[x])))
                #if(val>0):
                #    val=1
                dist=dist+val
            dist=dist/(len(known_positives)+1)
            
            print("        %s" % x,float(scores[x]),'error',dist)

        print("     random recommendation")
        random1=np.random.randint(len(orgs), size=3)
        for x in random1:
            dist=0.0
            for o in known_positives:
                val=np.sqrt(sum((second[o]-second[x])*(second[o]-second[x])))
                #if(val>0):
                #    val=1
                dist=dist+val
            dist=dist/(len(known_positives)+1)
            
            print("        %s" % orgs[x]['name'],float(scores[x]),'error',dist)
    
print('first : user_vs_languages',first.shape)
print('second : repo_vs_language',second.shape)
print('third: repo_vs_user',third.shape)

first_new = normalise(first)
print "Done"
second_new = normalise(second)
print "Done"
third_new = normalise(third)
print "Done"

print('first : user_vs_languages',first_new.shape)
print('second : repo_vs_language',second_new.shape)
print('third: repo_vs_user',third_new.shape)


model.fit(csr_matrix(third_new),user_features=csr_matrix(second_new),item_features=csr_matrix(first_new),epochs=20)


sample_recommendation(model,third_new,[4,70,76,10001],first_new,second_new)
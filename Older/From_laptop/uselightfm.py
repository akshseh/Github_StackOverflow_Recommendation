import pickle
from lightfm import LightFM
from scipy.sparse import csr_matrix
import numpy as np
first=[]
second=[]
third=[]
users=[]
orgs=[]
with open('first.txt') as f:
    first = pickle.load(f)

with open('second.txt') as f:
    second = pickle.load(f)

with open('third.txt') as f:
    third = pickle.load(f)

with open('user_list') as f:
    list_of_users = pickle.load(f)


# with open('users.txt') as f:
#     users = pickle.load(f)
# with open('orgs.txt') as f:
#     orgs = pickle.load(f)

first=first[0:len(third)]
second=second[0:len(third)]

print('first',first.shape)
print('second',second.shape)
print('third',third.shape)

model = LightFM(no_components=30, learning_rate=0.001)

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
            print ("User-recommended:")
            print list_of_users[x]
            print("        %s" % x,float(scores[x]),'error',dist)

    

print('mix',third.shape)
print('first',first.shape)
print('second',second.shape)

model.fit(csr_matrix(third),
          user_features=csr_matrix(second),
          item_features=csr_matrix(first),
          epochs=20)


sample_recommendation(model,third,[4,70,76,10001],first,second)



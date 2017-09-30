import glob
import os
import json
import sys
from collections import defaultdict
import csv

users = defaultdict(lambda: { 'followers': 0 })
FOLLOWING_DIR ='following'
TWITTER_FNAME = 'twitter_network.csv'


def process_follower_list(screen_name, edges=[], depth=0, max_depth=2, edge_exists={}):
    f = os.path.join(FOLLOWING_DIR, screen_name + '.csv')

    if not os.path.exists(f):
        print 'not exists, edges:'
        return edges
#read the csv file and get the follower ids
    with open(f, 'rb') as outf:
        reader = csv.reader(outf, delimiter=' ', quotechar='|')
        followers_ids = []
        for row in reader:
            followers_ids.append(row[0].split(';')[2])

        screen_name_2 = followers_ids

        # use the number of followers for screen_name as the weight
        weight = users[screen_name]['followers']
        
        edges.append([screen_name, screen_name_2, weight])


    with open(, 'w') as outf:
        edge_exists = {}
        for edge in edges:
            for name in  edge[1]:
                key = '%s,%s' %(edge[0], name)
                if not(key in edge_exists):
                    #create an excel file with the edges from user to user
                    outf.write('%s;' % edge[0])
                    outf.write('%s;' % name)
                    outf.write('%s;' % edge[2])
                    outf.write('\n')
                    edge_exists[key] = True
              
                    
                    
    
    return edges

edge_exists = {}
for f in glob.glob('twitter-users/*.json'):
    #after we've created our json files in previous a.py, for each json file
    data = json.load(file(f))
    screen_name = data['screen_name']
    print screen_name
    users[screen_name] = { 'followers': data['followers_count'] }
    edges = process_follower_list(screen_name, max_depth=3, edge_exists = edge_exists)
    

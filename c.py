import networkx as net
import matplotlib.pyplot as plt

from collections import defaultdict
import math

twitter_network = [ line.strip().split('\t') for line in file('twitter_network.csv') ]

o = net.Graph()
hfollowers = defaultdict(lambda: 0)

users = {}
i=0
for (row) in twitter_network:    
    user = str(row[0].split(';')[0])
        
    if user not in users:
        #add the node from 1st column of excel
        users[i] = user
        o.add_node(user)
                 
    for (row) in twitter_network:
        #for each follower that node has, add the node-edge to its follower
        u = str(row[0].split(';')[0])                
        if u == users[i]:
            followed_by = str(row[0].split(';')[1])
            o.add_edge(u,followed_by)
            
    i = i+1
    
 

SEED = 'user_name'

# centre around the SEED node and set radius of graph
#g = net.Graph(net.ego_graph(o, SEED, radius=15))
g=net.ego_graph(o, SEED, radius=15)

#draw graph and write the file
net.draw(g, with_labels = True)
plt.show()
net.write_gexf(g,'graph.gexf', version='1.2draft')

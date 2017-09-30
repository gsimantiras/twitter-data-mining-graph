import tweepy
import time
import os
import sys
import json
import argparse
import csv

FOLLOWING_DIR = 'following'
#set here how many max friends to extract from each
MAX_FRIENDS = 50


if not os.path.exists(FOLLOWING_DIR):
    os.makedir(FOLLOWING_DIR)

enc = lambda x: x.encode('ascii', errors='ignore')

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
CONSUMER_KEY = 'xxxxxxxxxxxxxxx'
CONSUMER_SECRET = 'xxxxxxxxxxxxxxx'
ACCESS_TOKEN = 'xxxxxxxxxxxxxxx'
ACCESS_TOKEN_SECRET = 'xxxxxxxxxxxxxxx'

user_name = 'xxxxxxxxxxxxxxx'

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#create your api 
api = tweepy.API(auth)

def get_follower_ids(centre, max_depth, current_depth, taboo_list):

    # print 'current depth: %d, max depth: %d' % (current_depth, max_depth)
    # print 'taboo list: ', ','.join([ str(i) for i in taboo_list ])

    if current_depth == max_depth:
        print 'out of depth'
        return taboo_list

    if centre in taboo_list:
        # we've been here before
        print 'Already been here.'
	return taboo_list
    else:
        taboo_list.append(centre)
        
    try:
        
	userfname = os.path.join('twitter-users', str(centre) + '.json')
		
        if not os.path.exists(userfname):
            print 'Retrieving user details for twitter id %s' % str(centre)
            while True:
                try:
                    user = api.get_user(centre)
		    #create a json file for each user
                    d = {'name': user.name,
                         'screen_name': user.screen_name,
                         'id': user.id,
                         'friends_count': user.friends_count,
                         'followers_count': user.followers_count,
                         'followers_ids': user.followers_ids()}
                    
                    with open(userfname, 'w') as outf:
                        outf.write(json.dumps(d, indent=1))

                    user = d
                    break
                except tweepy.TweepError, error:
                    print type(error)
                    #a try-exception is required because twitter could cut you out
                    if str(error) == 'Not authorized.':
                        print 'Can''t access user data - not authorized.'
                        return taboo_list

                    if str(error) == 'User has been suspended.':
                        print 'User suspended.'
                        return taboo_list

                    errorObj = error[0][0]

                    print errorObj

                    if errorObj['message'] == 'Rate limit exceeded':
                        return taboo_list
                        print 'Rate limited. Sleeping for 15 min.'
                        time.sleep(15*60)
                        continue

                    return taboo_list
        else:
            print 'json exists'
            #if the follower already exists, read he's json file
            with open(userfname) as fname:
                user = json.load(fname)

                
	screen_name = enc(user['screen_name'])
	followers_ids = user['followers_ids']
	
        fname = os.path.join(FOLLOWING_DIR, screen_name + '.csv')
        #in the 'following' folder we're going to create a
        #excel file, storing the followers
                
        if not os.path.exists(fname):
            i=0
            with open(fname, 'w') as outf:
                for friend in followers_ids:
                    if i>MAX_FRIENDS:
                        #get a max of 151 followers
                        #because of request limiation
                        break
                    try:
                        #write name follower id and follower name
                        #in separate columns
                        i = i+1
                        outf.write('%s;' % screen_name)
                        outf.write('%s;' % friend)
                        outf.write('%s;' % api.get_user(friend).screen_name)
                        outf.write('\n')
                    except tweepy.TweepError:
                        # hit rate limit, sleep for 15 minutes
                        print 'Rate limited. Sleeping for 15 min.'
                        time.sleep(15*60)
                        continue
                    except StopIteration:
                        break
	else:
            print 'csv exists'
            #if the file already exists read it
            with open(fname, 'rb') as outf:
                reader = csv.reader(outf, delimiter=' ', quotechar='|')
                followers_ids = []
                for row in reader:
                    followers_ids.append(row[0].split(';')[1])
                    
            print 'Found %d friends for %s' % (len(followers_ids), screen_name)

        # get friends of friends
	current_depth = current_depth +1
        	
	if current_depth < max_depth:
            for fid in followers_ids:
                print 'going deeper for %s' %fid
                taboo_list2 = get_follower_ids(fid, max_depth, current_depth, taboo_list)
                taboolist = taboo_list + taboo_list2
                if current_depth+1 < max_depth and len(followers_ids) > FRIENDS_OF_FRIENDS_LIMIT:
                    print 'Not all friends retrieved for %s.' % screen_name

    except Exception, error:
        print 'Error retrieving followers for user id: ', centre
        print error

        
    return taboo_list



if __name__ == '__main__':
    #starting with me, and in depth of 3, getting my followers
    taboo_list = []
    max_depth = 3
    current_depth = 1
    #type your user name or any username you want to start getting its followers
    matches = api.lookup_users(screen_names=[user_name])
    friendlist = get_follower_ids(matches[0].id, max_depth=max_depth, current_depth=current_depth, taboo_list=taboo_list)

   

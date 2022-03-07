#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Travis McDaneld
#
# Hello! This program will find tweets from Twitter (via Twython) based on a
# given string, the number of tweets you'd like to store,
# and the name for an SQL database you'd like to create and store
# the data in, accomplished via the sqlite3 package.
# Use "python Twitter_API_SQL_Demonstration.py data 1000 tweets.db" in the command line, for example,
# to create a database called "tweets.db" and gather 1000 tweets about the topic: "data",
# and store them in that new database file (this will include the User ID, name,
# screen name and the number of followers regarding the original poster, as well
# as the content of the tweet itself). You will then be given the first three rows of the
# database, so you can see the outcome.


# In[1]:


import sys
import sqlite3
from twython import Twython


# In[6]:


class twitterAnalyze():
    
    def __init__(self, keyWord, recordLimit, output):
        
        # Variable initialization
        self.keyWord = keyWord
        self.recordLimit = int(recordLimit)
        self.output = output
        
        # Lists made for the tweet information
        self.user_id = []
        self.name = []
        self.screen_name = []
        self.tweet_text = []
        self.followers_count = []
        
        # My API Keys for twitter access
        self.CONSUMER_KEY = "Lxa2Jk12VRcnxovEyNmUBlDK4"
        self.CONSUMER_SECRET = "XDHgjhousCyXMpueZ238OeheaDccs4D8KrZ1AjGhr45xAVNNFo"
        self.ACCESS_TOKEN = "1353555996367482882-z896vW4frwDdJuxPjMt5QDNf5I43OP"
        self.ACCESS_TOKEN_SECRET = "72fFf3nirtyvIFle87nE2HMZqy6DTOHefpucd2sTfvtap"

        self.twitter = Twython(self.CONSUMER_KEY,
                               self.CONSUMER_SECRET,
                               self.ACCESS_TOKEN,
                               self.ACCESS_TOKEN_SECRET)
        
        # Let's make the search!
        self.search_results = self.twitter.search(q=self.keyWord, count=self.recordLimit)
        
        # Connecting to the sqlite3 server
        self.con = sqlite3.connect(output)
        self.cur = self.con.cursor()

        self.initTable()
        self.insertValues()
        self.printValues()
        
    
    def initTable(self):
        
        # This appends information to our lists
        for tweet in range(len(self.search_results['statuses'])):
            self.user_id.append(self.search_results['statuses'][tweet]['user']['id'])
            self.name.append(self.search_results['statuses'][tweet]['user']['name'].encode('utf-8'))
            self.screen_name.append(self.search_results['statuses'][tweet]['user']['screen_name'].encode('utf-8'))
            self.tweet_text.append(self.search_results['statuses'][tweet]['text'].encode('utf-8'))
            self.followers_count.append(self.search_results['statuses'][tweet]['user']['followers_count'])
        
        # Connection to sqlite database 'output'
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tweets (user_id VARCHAR (50), name VARCHAR (50), screen_name VARCHAR(50), tweet_text VARCHAR (300), followers_count INT NOT NULL)''') 
        
    def insertValues(self):
        
        # Adds to the table for each element of the 5 lists
        for i in range(len(self.user_id)):
            self.cur.execute('INSERT INTO tweets (user_id, name, screen_name, tweet_text, followers_count) VALUES(?, ?, ?, ?, ?)' , [self.user_id[i], self.name[i], self.screen_name[i], self.tweet_text[i], self.followers_count[i]])
        
        # Save the changes
        self.con.commit()
        
        # Close the Connection
        self.con.close()
    
    def printValues(self):
        
        # Reopen the connection for printing
        con = sqlite3.connect(self.output)
        cur = con.cursor()
        instances = 0
        
        # Printing the first three rows of the database
        print("You have stored " + str(sys.argv[2] + " tweets into " + str(sys.argv[3])) + ".")
        print("Here are the first three instances of what was stored in your database " + str(self.output) + ":")
        print("It is in this order: User ID, Name, Screen Name, Content of Tweet, Followers of User." + "\n")
        for row in cur.execute('SELECT * FROM tweets'):
            if instances >= 3:
                break
            print(row)
            instances += 1
            
        # Close the connection
        con.close()


# In[5]:


# Just in case the call is done incorrectly:
if len(sys.argv) != 4:
            print('''Please provide (in order) a word to search for, 
                  the number of tweets to collect, 
                  and the name of the database 
                  you'd like to create (must end in \'.db\')''')
else:
    twitterAnalyze(sys.argv[1], sys.argv[2], sys.argv[3])

# Used for testing:
# myt = twitterAnalyze("data science", 10, "twitterdata.db")


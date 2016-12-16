# Loading required python modules

import tweepy
from tweepy import OAuthHandler
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 
consumer_key = '' #enter your consumer_key
consumer_secret = '' #enter your consumer_secret
access_token = '' #enter your access_token
access_secret = '' #enter yout access_secret
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)


#creating an empty dataframe:
columnNames = ["date","text"]

df = pd.DataFrame(columns=columnNames)

# Downloading tweets:
for tweet in tweepy.Cursor(api.search,
                           q='Soccer', #select the topic you're interested in
                           wait_on_rate_limit = True,
                           wait_on_rate_limit_notify = True,
                           since = '"2016-12-10"',
                           until = '"2016-12-15"',
                           
                           lang = 'en').items():
    print tweet.text, tweet.created_at
    data = pd.DataFrame({"date":tweet.created_at, "text":tweet.text}, index=[0])
    df = df.append(data,ignore_index=True)
    


# Computing sentiment of tweets
df["negative"] = np.zeros(len(df))
df["positive"] = np.zeros(len(df))

for row in range(len(df)):
    feeling = vaderSentiment((df["text"][row]).encode("utf-8"))
    df.set_value(row,'negative', feeling["neg"])
    df.set_value(row,'positive', feeling["pos"])
    print row
  


#plotting evoution of tweets' "sentiment" (it's quite ugly.... sorry....)
dfPlot = df.groupby(df['date'].map(lambda x: x.day)).mean()


plt.plot(dfPlot['negative'])
plt.show()

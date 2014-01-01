from twitter import *
import os
import pickle

CONSUMER_KEY = 	"cwSZjDHLZ9PgJrdeQjtLfQ"
CONSUMER_SECRET = "W7TrsdB7fYgOY3wT6wIZjBblxrC87cUA1pP4QagS1Qc"

MY_TWITTER_CREDS = os.path.expanduser('my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
	oauth_dance("msgB", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
global twitter
twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

#Post a tweet
twitter.statuses.update(status="Testing")

fo = open("test.txt", "wb")


#last 5 tweets
x = t.statuses.user_timeline(count = 5)
tweets = []

for y in range(0,5):
	tweets.append(x[y]['text'])
	s = x[y]['text']
	fo.write(s.encode("UTF-8"))
	
fo.close()

#Getting last 20 mentions
mention_data = t.statuses.mentions_timeline()

last20_mention = []
last20_mentioner = []

for count in range(0, 20):
	last20_mention.append(mention_data[count]['text'])
	last20_mentioner.append(mention_data[count]['user']['name'])
	temp = last20_mentioner[count] + ":" + last20_mention[count] + "\n"
	fo.write(temp.encode("UTF-8"))





import tweepy
import requests
import urllib
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
user = api.me()

def get_info(status):
    return {
        "text": status.text,
        "username": status.author.screen_name,
        "id": status.id   
    }

def respondToTweet(status):
    print("Getting info")
    tweet = "@{0} \n".format(status["username"])
    urlquery = urllib.parse.urlencode({
        "search": status["text"]
    })
    r = requests.get("http://localhost:3000/cops?search={0}".format(urlquery))
    print(r.json()["form"])
    #api.update_status(tweet, status["id"])

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.user.id)
        info = get_info(status)
        respondToTweet(info)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(follow=[user.id_str])


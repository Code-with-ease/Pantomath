# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
from flask import Flask, render_template,request,jsonify
import pickle
import sys
import numpy as np
sys.path.append(".")
from src.personality_detection import PersonalityPredictor
# from multinomial import MultiNomialNaiveBayesClassifier
from src.tweetApi import TwitterFetcher
from src.tweetcleaner import *
from src.multinomial import MultiNomialNaiveBayesClassifier
twitter_fetcher=TwitterFetcher()
personality_predictor=PersonalityPredictor()
app = Flask(__name__)
model = pickle.load(open("Models/multinomial_naive_bayes.sav", 'rb'))

def personality(tweets_arr_fetched):
    # tweets_arr_fetched=twitter_fetcher.get_tweets_arr(username)
    posts = ""
    for tweet in tweets_arr_fetched:
      posts+=tweet+" ||| "
    return (personality_predictor.get_personality(posts))



# @app.route('/personality')
# def personality():
#     username = request.args.get('username')
#     tweets_arr_fetched=twitter_fetcher.get_tweets_arr(username)
#     posts = ""
#     for tweet in tweets_arr_fetched:
#       posts+=tweet+" ||| "
#     return (personality_predictor.get_personality(posts))

@app.route('/checkuser')
def checkuser():
    username = request.args.get('username')
    getReplies = request.args.get('replies')
    getTweets = request.args.get('tweets')
    if(getTweets=="True" and getReplies=="False"):
        tweets_arr_fetched=twitter_fetcher.get_tweets_arr(username)
        cleaned_tweets = getStemmedDocument(tweets_arr_fetched)
        # print("cleaned tweets:-\n",tw)
        predictions=model.predictMany(cleaned_tweets)
        print(predictions)
        tweet_list=[]
        for i in range(0,len(tweets_arr_fetched)):
            tweets = {}
            tweets["type"]="tweet"
            tweets["text"]=tweets_arr_fetched[i]
            tweets["isHateSpeech"]=str(predictions[i])
            tweet_list.append(tweets)
        res={
            "tweets":tweet_list,
            "hatespeechCount":str(np.sum(np.array(predictions)==1)),
            "personality":personality(tweets_arr_fetched)
        }
        print(res)
    elif(getReplies=="True" and getTweets=="False"):
        # tweets_arr_fetc?h=[]
        reply_arr_fetch=[]
        tweets_data = twitter_fetcher.get_timeline(username)
        for tweet in tweets_data:
            # tweets_arr_fetch.append(tweet["text"])
            for reply in tweet["replies"]:
                reply_arr_fetch.append(reply["text"])
        cleaned_tweets = getStemmedDocument(reply_arr_fetch)
        # print("cleaned tweets:-\n",tw)
        predictions=model.predictMany(cleaned_tweets)
        print(predictions)
        tweet_list=[]
        for i in range(0,len(reply_arr_fetch)):
            tweets = {}
            tweets["text"]=tweets_arr_fetched[i]
            tweets["isHateSpeech"]=str(predictions[i])
            tweet_list.append(tweets) 
        res={
            "replies":tweet_list,
            "hatespeechCount":str(np.sum(np.array(predictions)==1)),
            "personality":personality(reply_arr_fetch)
        }
    else:
        tweets_arr_fetch=[]
        tweets_data = twitter_fetcher.get_timeline(username)
        c=0
        for tweet in tweets_data:
            c+=1
            r=0
            tweets_arr_fetch.append(tweet["text"])
            for reply in tweet["replies"]:
                r+=1
                tweets_arr_fetch.append(reply["text"])
            print(c,r)
        cleaned_tweets = getStemmedDocument(tweets_arr_fetch)
        # print("cleaned tweets:-\n",tw)
        predictions=model.predictMany(cleaned_tweets)
        print(predictions)
        tweet_list=[]
        for i in range(0,len(tweets_arr_fetch)):
            tweets = {}
            tweets["text"]=tweets_arr_fetch[i]
            tweets["isHateSpeech"]=str(predictions[i])
            tweet_list.append(tweets) 
        res={
            "tweets":tweet_list,
            "hatespeechCount":str(np.sum(np.array(predictions)==1)),
            "personality":personality(tweets_arr_fetch)
        }
    # print("uncleaned tweets:-\n",tweets_arr_fetched)
    # for tweet in tweets_arr_fetched:
    #   posts+=tweet
    
    return res
    # return "hello"

# @app.route('/tweets')
# def tweets():
#     username=request.args.get('username')
#     print(twitter_fetcher.get_timeline(username))
#     print(model.predict("Shut up!"))
#     return "Hello"
#
# @app.route('/tweets')
# def replies():
#     username=request.args.get('username')
#     tweetId = request.args.get('tweetId')
#     tweetApi.get_replies(username,tweetId)
#     return "Hello"

if __name__ == '__main__':   
    app.run(host='127.0.0.1', port=8000, debug=True, use_reloader=False)
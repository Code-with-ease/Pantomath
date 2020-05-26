from flask import Flask, render_template,request,jsonify
from flask_cors import CORS
import sys
import numpy as np
import tweepy
sys.path.append(".")
from src.personality_detection import PersonalityPredictor
from src.logisticregression import LogisticRegressionClassifier,CountVectorizerNGram
# from src.countvectorizerngram import TfidfVectorizerNGram,Countvectorizerngram
from src.tweetApi import TwitterFetcher
from src.tweetcleaner import *
import pickle

twitter_fetcher=TwitterFetcher()
personality_predictor=PersonalityPredictor()
hate_speech_predictor=LogisticRegressionClassifier()
app = Flask(__name__)
CORS(app)
hate_speech_predictor = pickle.load(open("Models/LogisticRegression.pickle", 'rb'))
tf_idf = pickle.load(open("Models/CountVectorizerLR.pickle", 'rb'))
def personality(tweets_arr_fetched):
    # tweets_arr_fetched=twitter_fetcher.get_tweets_arr(username)
    posts = ""
    for tweet in tweets_arr_fetched:
      posts+=tweet+" ||| "
    return (personality_predictor.get_personality(posts))



@app.route('/')
def mainpage():
    return("Welcome to the server !!")

@app.route('/checkuser')
def checkuser():
    username = request.args.get('username')
    getRetweets = request.args.get('retweets')
    getTweets = request.args.get('tweets')
    print(username,getRetweets,getTweets)
    try:

        tweets_arr_fetched=twitter_fetcher.get_timeline(username,getretweets=getRetweets=="true",gettweets=getTweets=="true")
        if(len(tweets_arr_fetched)!=0):
                X_test_vec_tweets = tf_idf.transform(tweets_arr_fetched)
                
                predictions= hate_speech_predictor.predict(X_test_vec_tweets)
                person = personality(tweets_arr_fetched)
        else:
                predictions=[]
                person = "Insufficient tweets"
        tweet_list=[]
        for i in range(0,len(tweets_arr_fetched)):
            tweets = {}
            tweets["text"]=tweets_arr_fetched[i]
            tweets["isHateSpeech"]=str(predictions[i])
            tweet_list.append(tweets)
        res={
                "tweets":tweet_list,
                "hatespeechCount":str(np.sum(np.array(predictions)==1)),
                "personality":person
        }

    except tweepy.error.TweepError:
        return {
            "tweets":[],
            "hatespeechCount":0,
            "personality": "Account doesnot exist"
        }
    return (jsonify(res))




if __name__ == '__main__':   
    app.run(host='127.0.0.1', port=8000, debug=True, use_reloader=False)


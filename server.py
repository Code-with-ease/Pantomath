from flask import Flask, render_template,request,jsonify
from flask_cors import CORS
import sys
import numpy as np
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
    getReplies = request.args.get('replies')
    getTweets = request.args.get('tweets')
    print(username,getReplies,getTweets)
    if(getTweets=="true" and getReplies=="false"):
        tweets_arr_fetched=twitter_fetcher.get_tweets_arr(username)
        
        X_test_vec_tweets = tf_idf.transform(tweets_arr_fetched)
        
        predictions= hate_speech_predictor.predict(X_test_vec_tweets)
        print(predictions)
        tweet_list=[]
        for i in range(0,len(tweets_arr_fetched)):
            tweets = {}
            tweets["text"]=tweets_arr_fetched[i]
            tweets["isHateSpeech"]=str(predictions[i])
            tweet_list.append(tweets)
        res={
            "tweets":tweet_list,
            "hatespeechCount":str(np.sum(np.array(predictions)==1)),
            "personality":personality(tweets_arr_fetched)
        }
        print(res)
    elif(getReplies=="true" and getTweets=="false"):
        
        reply_arr_fetch=[]
        tweets_data = twitter_fetcher.get_timeline(username)
        
        for tweet in tweets_data:
            for reply in tweet["replies"]:
                reply_arr_fetch.append(reply["text"])
        
        X_test_vec_reply = tf_idf.transform(reply_arr_fetch)
        predictions=hate_speech_predictor.predict(X_test_vec_reply)
        print(predictions)
        reply_list=[]
        for i in range(0,len(reply_arr_fetch)):
            tweets = {}
            tweets["text"]=reply_arr_fetch[i]
            tweets["isHateSpeech"]=str(predictions[i])
            tweet_list.append(tweets)
        res={
            "replies":reply_list,
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
        
        X_test_vec_tweets = tf_idf.transform(tweets_arr_fetch)
        
        predictions= hate_speech_predictor.predict(X_test_vec_tweets)
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

    return (jsonify(res))


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


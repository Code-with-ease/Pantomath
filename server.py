# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
from flask import Flask, render_template,request
import pickle
import sys
sys.path.append(".")
from src.personality_detection import PersonalityPredictor
# from multinomial import MultiNomialNaiveBayesClassifier
from src.tweetApi import TwitterFetcher

twitter_fetcher=TwitterFetcher()
personality_predictor=PersonalityPredictor()
app = Flask(__name__)
filename = 'multinomial_naive_bayes.sav'

# model = pickle.load(open(filename, 'rb'))


@app.route('/personality')
def personality():
    username = request.args.get('username')
    tweets_arr_fetched=twitter_fetcher.get_tweets_arr(username)
    posts = ""
    for tweet in tweets_arr_fetched:
      posts+=tweet+" ||| "
    return (personality_predictor.get_personality(posts))


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
    app.run(host='127.0.0.1', port=8000, debug=True)

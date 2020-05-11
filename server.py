import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template,request
import pickle
from multinomial import MultiNomialNaiveBayesClassifier
import tweetApi

app = Flask(__name__)
filename = 'multinomial_naive_bayes.sav'
model = pickle.load(open(filename, 'rb'))
@app.route('/tweets')
def tweets():
    username=request.args.get('username')
    print(tweetApi.get_timeline(username))
    print(model.predict("Shut up!"))
    return "Hello"

@app.route('/tweets')
def replies():
    username=request.args.get('username')
    tweetId = request.args.get('tweetId')
    tweetApi.get_replies(username,tweetId)
    return "Hello"

if __name__ == '__main__':   
    app.run(host='127.0.0.1', port=8000, debug=True)


import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import nltk
from nltk.stem import WordNetLemmatizer
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score,accuracy_score
import pickle
from nltk.corpus import stopwords 
from nltk import word_tokenize

nltk.download('stopwords')
nltk.download('wordnet')

lemmatiser = WordNetLemmatizer()
cachedStopWords = stopwords.words("english")

class LogisticRegressionClassifier:
  # model_cv = CountVectorizerNGram()
  # def __init(self,ngram_start=1,ngram_end=1):
  #   # model_cv = CountVectorizerNGram(ngram_start,ngram_end)
  modelLR = LogisticRegression(C=0.1,penalty="l2")
  def __init__(self):
    self.modelLR = LogisticRegression(C=0.1,penalty="l2")
  def train(self,X_train_vec,Y_train):
    # X = pd.DataFrame(data={'posts': X_train})
    # print(X)
    # X= X.loc[:, ~X.columns.str.contains('^Unnamed')]
    # slef.modelLR = LogisticRegression(C=100)
    self.modelLR.fit(X_train_vec,Y_train)
    return self.modelLR
  def predict(self,X_test_vec):
    ypred = self.modelLR.predict(X_test_vec)
    return ypred
  def score(self,Y_pred,Y):
    result = accuracy_score(Y_pred,Y)
    return result*100 
class CountVectorizerNGram:
  def __init__(self,start,end):
    if(start>end):
      end=start
    self.model_cv = CountVectorizer(ngram_range=(start,end))
  def clean(self,text):
    list_posts = []
    for row in text.iterrows():
        # Remove and clean comments
        posts = row[1].posts
        temp = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', posts)
        temp = re.sub("[^a-zA-Z]", " ", temp)
        temp = re.sub(' +', ' ', temp).lower()
        temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ') if w not in cachedStopWords])
        
        list_posts.append(temp)
            
    list_posts = np.array(list_posts)
    return list_posts
  def fit_transform(self,X):
    print("X_train\n",X.values)
    X = pd.DataFrame(data={'posts':X.values})
    clean_text = self.clean(X)
    X_train_vec = self.model_cv.fit_transform(clean_text)
    return X_train_vec
  def transform(self,X_test):
    X_test_vec = self.model_cv.transform(X_test)
    return X_test_vec
class TfidfVectorizerNGram:
  def __init__(self,start,end):
    if(start>end):
      end=start
    self.model_cv = TfidfVectorizer(ngram_range=(start,end))
  def clean(self,text):
    list_posts = []
    for row in text.iterrows():
        # Remove and clean comments
        posts = row[1].posts
        temp = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', posts)
        temp = re.sub("[^a-zA-Z]", " ", temp)
        temp = re.sub(' +', ' ', temp).lower()
        temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ') if w not in cachedStopWords])
        
        list_posts.append(temp)
            
    list_posts = np.array(list_posts)
    return list_posts
  def fit_transform(self,X):
    print("X_train\n",X.values)
    X = pd.DataFrame(data={'posts':X.values})
    clean_text = self.clean(X)
    X_train_vec = self.model_cv.fit_transform(clean_text)
    return X_train_vec
  def transform(self,X_test):
    X_test_vec = self.model_cv.transform(X_test)
    return X_test_vec
if __name__ == '__main__':
    global data,X,Y
    data=pd.read_csv("../Datasets/hate_speech.csv")
    X=data["text"]
    Y = data["label"]
    # from countvectorizerngram import TfidfVectorizerNGram
    cv = CountVectorizerNGram(1,4).model_cv

    X_train_vec=cv.fit_transform(X)
    lr = LogisticRegressionClassifier()
    lr.train(X_train_vec,Y)
    c=1
    while(c!=0):
        print("enter 0 to exit. enter 1 for manual input. enter 2 to fetch by twitter handle")
        c = int(input())
        if(c==2):
            from tweetApi import TwitterFetcher
            twf = TwitterFetcher()
            print("enter twitter handle:-")
            username = input()
            print("fetching tweets")
            tweets = twf.get_timeline(username,True,True)
            print(str(len(tweets))+"tweets fetched")
            X_test_vec_tweets = cv.transform(tweets)
            pred = lr.predict(X_test_vec_tweets)
            print("hate speech detected",sum(np.array(pred)==1))
            k=0
            q=1
            if(sum(np.array(pred)==1)>=1):
                print("text detected with hate speech are:-")
                for p in pred:
                    if(p):
                        print(str(q)+".",tweets[k])
                        q+=1
                    k+=1
        if(c==1):
            print("enter the text to be predicted")
            txt = input()
            text = []
            text.append(txt)
            print(text)
            X_test_vec_tweets = cv.transform(text)
            pred = lr.predict(X_test_vec_tweets)
            if(pred[0]==1):
                print("Hate speech detected")
            else:
                print("not a hate speech text")
    
    pickle.dump(lr,open("../Models/LogisticRegression.pickle","wb"))
    pickle.dump(cv,open("../Models/CountVectorizerLR.pickle","wb"))

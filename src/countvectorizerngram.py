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

class TfidfVectorizerNGram:
  def __init__(self,start,end):
    if(start>end):
      end=start
    self.model_tf = TfidfVectorizer(ngram_range=(start,end))
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
    X_train_vec = self.model_tf.fit_transform(clean_text)
    return X_train_vec
  def transform(self,X_test):
    X_test_vec = self.model_tf.transform(X_test)
    return X_test_vec
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

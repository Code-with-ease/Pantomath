#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import datetime


# In[2]:


class MultiNomialNaiveBayesClassifier:
    train_text=[]
    test_text=[]
    train_result=[]
    test_result=[]
    distinct_list = []
    class_list = []
    Prior = {}
    likelyhood={}
    wordCount={}
    WordsInClass_list={}

    def __init__(self):
        self.train_text=[]
        self.train_result=[]
        self.distinct_list=[]
        self.class_list=[]
        self.wordCount={}
        self.WordsInClass_list={}      
    def WordCountInData(self):
        for word in self.distinct_list:
            for text in self.train_text:
                word_list=text.split()
                self.wordCount[word]+=word_list.count(word)
        return
    def ngramSet(self,nstart=1,nend=1):
      if(nend==1):
        nend=nstart
      distinct_list = []
      c=0
      for text in self.train_text:
        print(c)
        c+=1
        word_list = text.split()
        for k in range(nstart,nend+1):
          for i in range(0,len(word_list)-k+1):
            # print(word_list[i:i+k])
            distinct_list.append(' '.join(word_list[i:i+k]))
      return set(distinct_list)
    
    def classes(self):
        return set(self.train_result)

    def PriorOfClass(self,className):
        return float(self.train_result.count(className))/len(self.train_result)
    
    def WordsCountInClass(self,className):
        wordsInClass=0
        for i in range(len(self.train_text)):
            if(self.train_result[i]==className):
                wordInText=self.train_text[i].split()
                textWordsCount=len(wordInText)
                wordsInClass+=textWordsCount
        return wordsInClass
  
    def WordsInClassWithRepeat(self,className):
      words=[]
      j=0
      for text in self.train_text:
        if(self.train_result[j]==className):
          words+= text.split()
        j+=1
      self.WordsInClass_list[className]=words


    def likelyhoodOfClass(self,word,className):
        count=0
        count=self.WordsInClass_list[className].count(word)
        return float(count+1)/(self.wordCount[className] + len(self.distinct_list))
    
    def WordIfClass(self):
        for className in self.class_list:
            for word in self.distinct_list:
                print("P("+word+"|"+className+") = "+str(self.likelyhood[className][word]))
    
    def WordCountInText(self,word,text):
        word_list=text.split()
        return word_list.count(word)
    
    def ProbClassOfText(self,className,text):
        p=1
        prior = self.Prior[className]
        word_list = text.split()
        likelyhoodArray=[]
        for word in word_list:
            likelyhoodArray.append(self.likelyhoodOfClass(word,className))
        return np.prod(np.array(likelyhoodArray))*prior
    
    def test(self,text,test_result):
        result=""
        prob=0
        for className in self.class_list:
            prob1=self.ProbClassOfText(className,text)
            if(prob<prob1):
                result=className
                prob=prob1
        return result==test_result
    
    def train(self,train_text,train_result):
        self.train_text=list(train_text)
        self.train_result=list(train_result)
        self.class_list=list(self.classes())
        c=0
        start1 = datetime.datetime.now()
        for className in self.class_list:
            print("className",c)
            c+=1
            self.WordsInClassWithRepeat(className)
            self.Prior[className]=self.PriorOfClass(className)
            self.wordCount[className] =self.WordsCountInClass(className)
        self.distinct_list=list(self.ngramSet(1))
        end1 = datetime.datetime.now()
        start2 = datetime.datetime.now()
        for className in self.class_list:
            dist={}
            c=0
            for word in self.distinct_list:
                print(className,word,c)
                c+=1
                dist[word]=self.likelyhoodOfClass(word,className)
            self.likelyhood[className]=dist
        end2 = datetime.datetime.now()
        
        return self.likelyhood,end1-start1,end2-start2
    
    def predict(self,text):
        result=""
        prob=0
        for className in self.class_list:
            prob1=self.ProbClassOfText(className,text)
            if(prob<prob1):
                result=className
                prob=prob1
        return result

    def predictMany(self,texts):
      result=[]
      for text in texts:
        result.append(self.predict(text))
      return result

    def score(self,test_data,test_result):
        # c=0
        # for i in range(len(test_data)):
        #     if(test_result[i]==self.predict(test_data[i])):
        #         c+=1
        #     print(i,test_result[i],test_result[i]==self.predict(test_data[i]))
        result = np.array(self.predictMany(test_data))
        test_result = np.array(test_result)
        return float(np.sum(result == test_result))/len(test_data)


# In[3]:


mnb = MultiNomialNaiveBayesClassifier()


# In[4]:



# In[9]:


import datetime
from sklearn.model_selection import train_test_split
# df1 = pd.read_csv("mbti_1.csv")
df = pd.read_csv("Datasets/train_E6oV3lV.csv")
dft = pd.read_csv("Datasets/test_tweets_anuFYb8.csv")

dfx = df["tweet"]
dfy = df["label"]
dfxt = dft["tweet"] 

dfx.head()
X = dfx.values
Y = dfy.values
X_test = dfx.values
Y = dfy.values
print(X_test)
from src.tweetcleaner import *
X = getStemmedDocument(X)
start = datetime.datetime.now()
like,diff1,diff2 = mnb.train(X,Y)
end= datetime.datetime.now()
print("time taken=",end-start)
print("diff1",diff1)
print("diff2",diff2)


# In[ ]:


difference=end-start
seconds_in_day = 24 * 60 * 60
divmod(difference.days * seconds_in_day + difference.seconds, 60)


# In[11]:


import pickle


# In[12]:


filename = 'Models/multinomial_naive_bayes.sav'
pickle.dump(mnb, open(filename, 'wb'))


# In[23]:


# loaded_model = pickle.load(open(filename, 'rb'))
# start = datetime.datetime.now()
# model = pickle.load(open(filename,'rb'))
# result = model.predictMany(["shut up"])
# end = datetime.datetime.now()
# print(result,end-start)


# In[14]:


# from sklearn.naive_bayes import MultinomialNB,BernoulliNB


# In[15]:


# clf = MultinomialNB()


# In[16]:


# df.info()

# get_ipython().magic(u'pinfo clf.fit')
# clf.fit(X_train,Y_train)


# In[17]:



# In[18]:


# model.predict("Shut up!")


# In[ ]:





# In[ ]:





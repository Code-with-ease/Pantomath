
import pandas as pd
import numpy as np
import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
import pickle
import tweepy



class PersonalityPredictor():

    def __init__(self):
        self.consumer_key = "KSJYU03lzzH8ySUEKVaom1RBR"
        self.consumer_secret = "c9nBuKvwLjFNg3KconDt0jxmVWB6K85QsHunCYspNhAzTlmRel"
        self.access_key = "929607063889571841-OaRHMUWEkaF0KDozhSbVP21lbImuGkq"
        self.access_secret = "1rMYWNFPC7w8T3BEMLBGO64oHh0j3H1xuOAKWHA1150qE"
        self.root_path = "Datasets/mbti_1.csv"
        self.data = pd.read_csv(self.root_path)

        self.stemmer = PorterStemmer()
        self.lemmatiser = WordNetLemmatizer()
        self.cachedStopWords = stopwords.words("english")
        # self.cntizer = CountVectorizer(analyzer="word",max_features=1500,tokenizer=None,preprocessor=None,stop_words=None,max_df=0.7,min_df=0.1)
        self.cntizer=pickle.load(open("Models/cntizer.pickle", 'rb'))
        # self.tfizer = TfidfTransformer()
        self.tfizer=pickle.load(open("Models/tfizer.pickle", 'rb'))
        self.Pers = {'I': 0, 'E': 1, 'N': 0, 'S': 1, 'F': 0, 'T': 1, 'J': 0, 'P': 1}
        self.Pers_list = [{0: 'I', 1: 'E'}, {0: 'N', 1: 'S'}, {0: 'F', 1: 'T'}, {0: 'J', 1: 'P'}]

        self.unique_type_list = ['INFJ', 'ENTP', 'INTP', 'INTJ', 'ENTJ', 'ENFJ', 'INFP', 'ENFP',
               'ISFP', 'ISTP', 'ISFJ', 'ISTJ', 'ESTP', 'ESFP', 'ESTJ', 'ESFJ']

        self.unique_type_list = [x.lower() for x in self.unique_type_list]

    def get_types(self,row):

        type_post = row['type']

        I = 0; N = 0
        T = 0; J = 0

        if type_post[0] == 'I':
          I = 1
        elif type_post[0] == 'E':
          I = 0

        if type_post[1] == 'N':
          N = 1
        elif type_post[1] == 'S':
           N = 0

        if type_post[2] == 'T':
          T = 1
        elif type_post[2] == 'F':
          T = 0

        if type_post[3] == 'J':
          J = 1
        elif type_post[3] == 'P':
          J = 0

        return pd.Series( {'IE':I, 'NS':N , 'TF': T, 'JP': J })

    def translate(self,personality):
        return [self.Pers[l] for l in personality]


    def translate_back(self,personality):
        s = ""
        for i, l in enumerate(personality):
            s += self.Pers_list[i][l]
        return s

    def data_cleaning(self,data):

        list_personality = []
        list_posts = []
        len_data = len(data)

        for row in data.iterrows():

            posts = row[1].posts
            temp = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', posts)
            temp = re.sub("[^a-zA-Z]", " ", temp)
            temp = re.sub(' +', ' ', temp).lower()

            try:
                temp = " ".join([self.lemmatiser.lemmatize(w) for w in temp.split(' ') if w not in self.cachedStopWords])
            except AttributeError as e:
                temp=" ".join([w for w in temp.split(' ') if w not in self.cachedStopWords])
                print("Ok done")
            for t in self.unique_type_list:
              temp = temp.replace(t, "")

            type_labelized = self.translate(row[1].type)

            list_personality.append(type_labelized)
            list_posts.append(temp)

        list_posts = np.array(list_posts)
        list_personality = np.array(list_personality)
        return list_posts, list_personality

    # def training(self,filename="SVC.pkl"):
    #
    #     data = self.data.join(self.data.apply (lambda row: self.get_types(row),axis=1))
    #     print(data)
    #
    #     list_posts,list_personality = self.data_cleaning(data)
    #
    #     model = LinearSVC(dual=True, random_state=7, intercept_scaling=0.7, fit_intercept=True)
    #
    #     X_cnt = self.cntizer.fit_transform(list_posts)
    #     X = self.tfizer.fit_transform(X_cnt).toarray()
    #
    #
    #
    #     Y1 = list_personality[:,0]
    #     Y2 = list_personality[:,1]
    #     Y3 = list_personality[:,2]
    #     Y4 = list_personality[:,3]
    #
    #     # Fitting the model for the type "IE: Introversion (I) / Extroversion (E)"
    #     model.fit(X,Y1)
    #     pickle.dump(model, open(filename+"1", 'wb'))
    #
    #     # Fitting the model for the type "NS: Intuition (N) – Sensing (S)"
    #     model.fit(X,Y2)
    #     pickle.dump(model, open(filename+"2", 'wb'))
    #
    #     # Fitting the model for th type "FT: Feeling (F) - Thinking (T)"
    #     model.fit(X,Y3)
    #     pickle.dump(model, open(filename+"3", 'wb'))
    #
    #     # Fitting the model for the type "JP: Judging (J) – Perceiving (P)"
    #     model.fit(X,Y4)
    #     pickle.dump(model, open(filename+"4", 'wb'))

    def get_personality(self,my_posts,filename="Models/SVC.pkl"):

        # Using the already trained models for the types : I/E , N/S , F/T , J/P resp
        model1 = pickle.load(open(filename+"1", 'rb'))
        model2 = pickle.load(open(filename+"2", 'rb'))
        model3 = pickle.load(open(filename+"3", 'rb'))
        model4 = pickle.load(open(filename+"4", 'rb'))

        # type passed is a dummy value
        mydata = pd.DataFrame(data={'type': ['INTJ'], 'posts': [my_posts]})

        posts,dummy = self.data_cleaning(mydata)

        my_X_cnt = self.cntizer.transform(posts)
        my_X_tfidf = self.tfizer.transform(my_X_cnt).toarray()

        result = []

        # Prediction made for type I/E
        y_pred = model1.predict(my_X_tfidf)
        result.append(y_pred[0])

        # Prediction made for type N/S
        y_pred = model2.predict(my_X_tfidf)
        result.append(y_pred[0])

        # Prediction made for type F/T
        y_pred = model3.predict(my_X_tfidf)
        result.append(y_pred[0])

        # Prediction made for type J/P
        y_pred = model4.predict(my_X_tfidf)
        result.append(y_pred[0])

        return self.translate_back(result)

    def get_tweets(self,username):
            # username=request.args.get('username')
            # Authorization to consumer key and consumer secret
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)

            # Access to user's access key and access secret
            auth.set_access_token(self.access_key, self.access_secret)

            # Calling api
            api = tweepy.API(auth)

            number_of_tweets = 200
            tweets = api.user_timeline(screen_name=username)
            # Empty Array
            tmp = []

            # create array of tweet information: username,
            # tweet id, date/time, text
            tweets_for_csv = [
                (tweet.text, tweet.user.screen_name, tweet.user.profile_image_url, tweet.id_str, tweet.created_at) for tweet
                in tweets]  # CSV file created
            for j, name, url, id, time in tweets_for_csv:
                # print(j)
                # Appending tweets to the empty array tmp
                tweet_url = "https://twitter.com/" + username + "/status/" + id
                tmp.append([j, username, url, tweet_url, time.date(), id])

                # Printing the tweets
            return tmp[0:3]


    def get_timeline(self,username):
        # username=request.args.get('username')
        # Authorization to consumer key and consumer secret
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)

        # Access to user's access key and access secret
        auth.set_access_token(self.access_key, self.access_secret)

        # Calling api
        api = tweepy.API(auth)

        # 200 tweets to be extracted
        number_of_tweets = 200

        tweets = api.user_timeline(screen_name=username, count=number_of_tweets, tweet_mode="extended")

        tweets_list = []
        for tweet in tweets:
            if (hasattr(tweet, 'retweeted_status')):
                text = tweet.retweeted_status.full_text
            else:
                text = tweet.full_text
            # replies = get_replies(username,tweet.id)
            tweet_json = {
                "text": text,
                "id_str": tweet.id_str,
                "in_reply_to_user_id_str": tweet.in_reply_to_user_id_str,
                "time": tweet.created_at
            }
            tweets_list.append(tweet_json)
        return tweets_list

    #
    # def get_replies(self):
    #     username = request.args.get('username')
    #     tweetId = request.args.get('tweetId')
    #
    #     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    #
    #     # Access to user's access key and access secret
    #     auth.set_access_token(access_key, access_secret)
    #
    #     # Calling api
    #     api = tweepy.API(auth)
    #     searched_tweets = api.search(q='to:${username}', since_id=tweetId, rpp=100, count=1000, tweet_mode="extended")
    #     replies = []
    #     for tweet in searched_tweets:
    #         if (tweet.in_reply_to_user_id_str == tweetId):
    #             if (hasattr(tweet, 'retweeted_status')):
    #                 text = tweet.retweeted_status.full_text
    #             else:
    #                 text = tweet.full_text
    #             tweet_json = {
    #                 "text": text,
    #                 "id_str": tweet.id_str,
    #                 "in_reply_to_user_id_str": tweet.in_reply_to_user_id_str,
    #                 "time": tweet.created_at}
    #             replies.append(tweet_json)
    #     # print(replies)
    #     return replies
    #
    #
    def get_tweets_arr(self,username):
        tweets_arr = []
        data = self.get_timeline(username)
        for d in data:
            tweets_arr.append(d["text"])
        return tweets_arr

if __name__ == '__main__':
    global data,X,list_personality,list_posts
    # userHandle = "@nightwarriorftw"
    # predictor=PersonalityPredictor()
    # tweets_arr_fetched=predictor.get_tweets_arr(userHandle)
    # posts = ""
    # for tweet in tweets_arr_fetched:
    #   posts+=tweet+" ||| "
    # print(predictor.get_personality(posts))
    # print(tweets_arr_fetched)
    # predictor=PersonalityPredictor()
    # print(predictor.get_personality(""))

    # predictor.training()
    # # Training to be done only once, then pickled model is saved
    # # training(data)
    #
    # userHandle = "@sidntrivedi012"
    # tweets_arr_fetched=get_tweets_arr(userHandle)
    # print(tweets_arr_fetched)
    #
    # # Combining all the posts to get a cummulative result
    # posts = ""
    # for tweet in tweets_arr_fetched:
    #   posts+=tweet+" ||| "
    #
    # # Fetching the personality of the posts
    # result = get_personality(posts)
    # print(result)


import tweepy 
# Fill the X's with the credentials obtained by
# following the above mentioned procedure. 

class TwitterFetcher:
        def __init__(self):
                self.consumer_key = "KSJYU03lzzH8ySUEKVaom1RBR"
                self.consumer_secret = "c9nBuKvwLjFNg3KconDt0jxmVWB6K85QsHunCYspNhAzTlmRel"
                self.access_key = "929607063889571841-cSa500NXfvmGFB3T1kFeTXDpEtUgXtQ"
                self.access_secret = "d6IiDsqv0MY6LTPthF5xPeuJRyeVMllWtpRkpw60zVMsg"
                # self.consumer_key = 'Q5kScvH4J2CE6d3w8xesxT1bm'
                # self.consumer_secret = 'mlGrcssaVjN9hQMi6wI6RqWKt2LcHAEyYCGh6WF8yq20qcTb8T'
                # self.access_key = '944440837739487232-KTdrvr4vARk7RTKvJkRPUF8I4VOvGIr'
                # self.access_secret = 'bfHE0jC5h3B7W3H18TxV7XsofG1xuB6zeINo2DxmZ8K1W'

        def get_timeline(self,username,getretweets,gettweets):
                auth = tweepy.OAuthHandler(self.consumer_key,self. consumer_secret)
                # Access to user's access key and access secret
                auth.set_access_token(self.access_key,self.access_secret)
                # Calling api
                api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,compression=True)
                # 200 tweets to be extracted
                number_of_tweets=200
                tweets = api.user_timeline(screen_name = username,count=number_of_tweets, tweet_mode="extended")
                tweets_list = []
                for tweet in tweets:
                        if(tweet._json["lang"]=="en"):


                                if(hasattr(tweet, 'retweeted_status')):
                                        if(getretweets):

                                                text = tweet.retweeted_status.full_text
                                                tweets_list.append(text)
                                elif(gettweets):

                                        text = tweet.full_text
                                        tweets_list.append(text)  
                # print("list recieved",len(tweets_list))
                return tweets_list

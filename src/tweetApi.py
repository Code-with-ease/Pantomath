import tweepy 
# Fill the X's with the credentials obtained by
# following the above mentioned procedure. 

class TwitterFetcher:
        def __init__(self):
                self.consumer_key = "KSJYU03lzzH8ySUEKVaom1RBR"
                self.consumer_secret = "c9nBuKvwLjFNg3KconDt0jxmVWB6K85QsHunCYspNhAzTlmRel"
                self.access_key = "929607063889571841-OaRHMUWEkaF0KDozhSbVP21lbImuGkq"
                self.access_secret = "1rMYWNFPC7w8T3BEMLBGO64oHh0j3H1xuOAKWHA1150qE"
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
                print("test 11")
                tweets = api.user_timeline(screen_name = username,count=number_of_tweets, tweet_mode="extended")
                print("test 12")
                tweets_list = []
                c=0
                c1=0
                c2=0
                for tweet in tweets:
                        # print(tweet._json["lang"])
                        if(tweet._json["lang"]=="en"):
                                print(c,hasattr(tweet, 'retweeted_status'))
                                c+=1
                                if(hasattr(tweet, 'retweeted_status')):
                                        if(getretweets):
                                                c1+=1
                                                text = tweet.retweeted_status.full_text
                                                tweets_list.append(text)
                                elif(gettweets):
                                        c2+=1
                                        text = tweet.full_text
                                        tweets_list.append(text)  
                # print("list recieved",len(tweets_list),"retweets=",c1,"tweets=",c2)
                return tweets_list

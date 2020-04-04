import tweepy 
from flask import Flask,jsonify,request
# Fill the X's with the credentials obtained by  
# following the above mentioned procedure. 
consumer_key = "KSJYU03lzzH8ySUEKVaom1RBR" 
consumer_secret = "c9nBuKvwLjFNg3KconDt0jxmVWB6K85QsHunCYspNhAzTlmRel"
access_key = "929607063889571841-OaRHMUWEkaF0KDozhSbVP21lbImuGkq"
access_secret = "1rMYWNFPC7w8T3BEMLBGO64oHh0j3H1xuOAKWHA1150qE"
app = Flask(__name__)
# Function to extract tweets 
@app.route('/tweets',methods=['GET','POST'])
def get_tweets(): 
        username=request.args.get('username')
        # Authorization to consumer key and consumer secret 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_key, access_secret) 
  
        # Calling api 
        api = tweepy.API(auth) 
  
        # 200 tweets to be extracted 
        number_of_tweets=200
        tweets = api.user_timeline(screen_name=username) 
        for tweet in tweets:
                print("\n",tweet)
        # Empty Array 
        tmp=[]  
        
        # create array of tweet information: username,  
        # tweet id, date/time, text 
        tweets_for_csv = [(tweet.text,tweet.user.screen_name,tweet.user.profile_image_url,tweet.id_str,tweet.created_at) for tweet in tweets] # CSV file created  
        for j,name,url,id,time in tweets_for_csv:
        	# print(j)
        	# Appending tweets to the empty array tmp
                tweet_url="https://twitter.com/"+username+"/status/"+id
                tmp.append([j,username,url,tweet_url,time.date(),id]) 
  
        # Printing the tweets 
        return jsonify(tweets=tmp[0:3])

@app.route('/timeline',methods=['GET','POST'])
def get_timeline(): 
        username=request.args.get('username')
        # Authorization to consumer key and consumer secret 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_key, access_secret) 
  
        # Calling api 
        api = tweepy.API(auth) 
  
        # 200 tweets to be extracted 
        number_of_tweets=200
        tweets = api.user_timeline(screen_name=username,count = number_of_tweets,exclude_replies=False,tweet_mode="extended")
        for tweet in tweets:
                print("\n",tweet.full_text)
        
        # create array of tweet information: username,  
        # tweet id, date/time, text 
        tweets_list = []
        for tweet in tweets:
                tweet_json={"text":tweet.full_text,"id_str":tweet.id_str,"replies":tweet.in_reply_to_user_id_str,"time":tweet.created_at}
                tweets_list.append(tweet_json)
        return jsonify(tweets=tweets_list)

@app.route('/replies',methods=['GET','POST'])
def get_replies():
        username=request.args.get('username')
        tweetid=request.args.get('tweetid')
        print(tweetid)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_key, access_secret) 
  
        # Calling api 
        api = tweepy.API(auth) 

        searched_tweets = api.search(q="to:${username}", sinceId = str(tweetid),rpp=100,count=1000,tweet_mode="extended")
        replies=[]
        # print(searched_tweets)
        for searched_tweet in searched_tweets:
                print(searched_tweet.in_reply_to_status_id_str)
                if(searched_tweet.in_reply_to_status_id_str==str(tweetid)):
                        replies.append({"reply by":searched_tweet.user.screen_name,"text":searched_tweet.full_text,"created_at":searched_tweet.created_at}) 
        return jsonify(replies=replies)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)

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

@app.route('/timeline',methods=['GET'])
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
        
        tweets = api.user_timeline(screen_name = username,count=number_of_tweets, tweet_mode="extended")

        tweets_list = []
        for tweet in tweets:
                if(hasattr(tweet, 'retweeted_status')):
                        text = tweet.retweeted_status.full_text
                else:
                        text = tweet.full_text
                # replies = get_replies(username,tweet.id)
                tweet_json={
                        "text":text,
                        "id_str":tweet.id_str,
                        "in_reply_to_user_id_str":tweet.in_reply_to_user_id_str,
                        "time":tweet.created_at
                }
                tweets_list.append(tweet_json)
        return jsonify(tweets=tweets_list)

@app.route('/replies',methods=["GET"])
def get_replies():
        username=request.args.get('username')
        tweetId=request.args.get('tweetId')

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_key, access_secret) 
  
        # Calling api 
        api = tweepy.API(auth) 
        searched_tweets = api.search(q='to:${username}',since_id=tweetId,rpp=100,count=1000, tweet_mode="extended")
        replies=[]
        for tweet in searched_tweets:
                if(tweet.in_reply_to_user_id_str==tweetId):
                        if(hasattr(tweet, 'retweeted_status')):
                                text = tweet.retweeted_status.full_text
                        else:
                                text = tweet.full_text
                        tweet_json={
                        "text":text,
                        "id_str":tweet.id_str,
                        "in_reply_to_user_id_str":tweet.in_reply_to_user_id_str,
                        "time":tweet.created_at}
                        replies.append(tweet_json)
        print(replies)
        return jsonify(replies=replies)
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)

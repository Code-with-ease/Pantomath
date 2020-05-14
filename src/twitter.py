import tweepy

consumer_key = 'Q5kScvH4J2CE6d3w8xesxT1bm'
consumer_secret = 'mlGrcssaVjN9hQMi6wI6RqWKt2LcHAEyYCGh6WF8yq20qcTb8T'
access_token = '944440837739487232-KTdrvr4vARk7RTKvJkRPUF8I4VOvGIr'
access_token_secret = 'bfHE0jC5h3B7W3H18TxV7XsofG1xuB6zeINo2DxmZ8K1W'


def get_tweets(username):
    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_token, access_token_secret)

    # Calling api
    api = tweepy.API(auth)

    # 200 tweets to be extracted
    number_of_tweets = 200
    tweets = api.user_timeline(screen_name=username)

    # Empty Array
    tmp = []

    # create array of tweet information: username,
    # tweet id, date/time, text
    tweets_for_csv = [tweet.text for tweet in tweets]  # CSV file created
    for j in tweets_for_csv:
        # Appending tweets to the empty array tmp
        tmp.append(j)

        # Printing the tweets
    print(tmp)


# Driver code
if __name__ == '__main__':
    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    get_tweets("codekhal")
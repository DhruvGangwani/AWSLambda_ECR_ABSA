import tweepy
import csv
import pandas as pd


def get_tweets(hashtag, consumer_key, consumer_secret, access_token, access_token_secret, tweet_count):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    
    tweet_text, tweet_date = list(), list()
    for tweet in tweepy.Cursor(api.search,q=hashtag, count=tweet_count, lang="en").items():
        tweet_text.append(tweet.text.encode('utf-8'))
        tweet_date.append(tweet.created_at)
        # csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
        
    content = pd.DataFrame({'text': tweet_text, 'date': tweet_date})
    return content


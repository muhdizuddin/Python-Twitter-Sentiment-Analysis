
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
  
class TwitterClient(object): 
    def __init__(self): 
        consumer_key = 'JD41eS67ZJhNk6CCX6xbrOhCs'
        consumer_secret = 'zoz6AiFxLI46K98a0iV6vrQD736k4iQozmPKpPgxqd2dbSLsGW'
        access_token = '1346277570535280648-B5jDKYdAaelydUxKQ1gMNPgGqfUUT4'
        access_token_secret = 'wtnwZDKHjXoks2inkeQfn9xmTHASCE7mBQgjKw9RgPTHO'
  
        try: 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret) 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 20): 
        tweets = [] 
  
        try: 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            for tweet in fetched_tweets: 
                parsed_tweet = {} 
  
                parsed_tweet['text'] = tweet.text 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            return tweets 
  
        except tweepy.TweepError as e: 
            print("Error : " + str(e)) 
  
def main(): 
    api = TwitterClient() 
    tweets = api.get_tweets(query = 'facility management covid-19', count = 500) 
  
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    print("Positive tweets percent: {} %".format(100*len(ptweets)/len(tweets))) 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    print("Negative tweets percent: {} %".format(100*len(ntweets)/len(tweets))) 
    print("Neutral tweets percent: {} %".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))) 

    print("\n\nPositive tweets:") 
    for tweet in ptweets[:20]: 
        print(tweet['text']) 
  
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:20]: 
        print(tweet['text']) 
  
main() 

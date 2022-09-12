import tweepy
from kafka import KafkaProducer
import twitterauth as auth
import utils

# Creates a producer to send data to the pyspark ( Consumer ).
producer = KafkaProducer(bootstrap_servers=["localhost:9092"], value_serializer=utils.json_serializer)

#Creates a streaming class to stream tweets.
class twitterStream(tweepy.StreamingClient):
    def on_connect(self):
        print("Twitter Client Connected")

    # On tweet it gets the raw tweet which will be processed later on pyspark.
    def on_tweet(self, raw_data):
        if raw_data.referenced_tweets == None:
            producer.send("tweet", raw_data.text) 
            #print(raw_data.text)     # for testing  (prints to console)  

    # Provides error message on why connection failed.        
    def on_error(self):
        self.disconnect()

    # Creates the rules. ( The keywords to filter by.)
    def adding_rules(self, keywords):
        for terms in keywords:
            self.add_rules(tweepy.StreamRule(terms))
    


    
# Twitter Streaming Code. Necessary, to send the data to pyspark.
if __name__ == "__main__":
    stream = twitterStream(bearer_token=auth.bearer_token)
    stream_terms = ['bitcoin','luna','etherum']
    stream.adding_rules(stream_terms)
    stream.filter(tweet_fields=['referenced_tweets'])

   


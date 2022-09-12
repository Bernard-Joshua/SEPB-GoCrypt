from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql import functions as F
import findspark
import time
import json
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = f'--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 pyspark-shell'

if __name__ == "__main__":

    findspark.init()

    # Creating a spark session
    sc = SparkSession.builder.master("local[*]") \
                    .appName('SparkByExamples.com') \
                    .getOrCreate()


    # Reading from producer
    tweet = sc \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("startingoffsets","earliest") \
        .option("subscribe", "tweet") \
        .load()
    
    # Cleaning/Transforming Data
    tweet_df = tweet.select(explode(split(tweet.value, "t_end")).alias("tweet_words"))
    tweet_df = tweet_df.na.replace('', None)
    tweet_df = tweet_df.na.drop()
    tweet_df = tweet_df.withColumn('Tweets', F.regexp_replace('tweet_words', r'http\S+', ''))
    tweet_df = tweet_df.withColumn('Tweets', F.regexp_replace('tweet_words', '@\w+', ''))
    tweet_df = tweet_df.withColumn('Tweets', F.regexp_replace('tweet_words', '#', ''))
    tweet_df = tweet_df.drop("tweet_words")


    #creating a one column dataframe.
    #tweet_df = tweet_df.selectExpr("CAST(value AS STRING)") \
            #####.option("truncate","false").start()

    #tweet_df.printSchema()

    # Load data to console / Will be changed later to load to Machine Learning Model
    query = tweet_df.writeStream.format("console").start()
    
    time.sleep(60) # sleep 10 seconds
    query.stop()


    
	#Count the number of tweets per User
    #user_counts = parsed.map(lambda tweet: (tweet['user']["screen_name"], 1)).reduceByKey(lambda x,y: x + y)


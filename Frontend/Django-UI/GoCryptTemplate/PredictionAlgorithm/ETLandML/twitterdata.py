import PredictionAlgorithm.ETLandML.twitterauth as auth

# Recent tweets stream.
def get_recent_tweets(term, today, yesterday):
    search_term = term
    tweets = auth.client.search_recent_tweets(query=search_term, end_time=today,start_time=yesterday, max_results=100) # Limit stream to 100 outputs at a time.
    return tweets.data

# For Testing only
# Current DateTime
# td = dt.datetime.today()
# td = td - dt.timedelta(hours=10) # Twitter recent stream needs atleast a 10 sec delay.
# Yesterday DateTime
# ytd = td - dt.timedelta(days = 1)
# data = get_recent_tweets("#bitcoin", today=td,yesterday=ytd)
# df = pd.DataFrame(data)
# df["polarity"] = df["text"].apply(sa.getPolarity)
# df["sentiment"] = df["polarity"].apply(sa.setClassification)

# print(sa.display(df))
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pygooglenews import GoogleNews
import datetime as dt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def load(term, df):
    # Query
    gn = GoogleNews()
    search = gn.search(term, when='1h')
    # Set to a dataframe.
    df = pd.DataFrame(search['entries'])
    df = df.drop(columns=['title_detail','links','link','id','guidislink','published_parsed','summary', 'summary_detail','sub_articles'])
    #del df['index']
    df = df.sort_values(by=['published'])
    #df.set_index()
    return df
    
def parse(text):
    return TextBlob(text).translate(to='en') # Translates any news headlines to english.

def getPolarity(text):
    return TextBlob(text).sentiment.polarity # Gets a compounded value of sentiment.

# Classifies Polarity
def setClassification(polarity):
    if polarity < 0:
        return "Negative"
    elif polarity > 0:
        return "Positive"
    else:
        return "Neutral"

# Wraapper function, makes it easier to integrate with Django.
def values(lang, country, crypto):
    df = pd.DataFrame()   
    df = load(crypto, df )
    df["polarity"] = df["title"].apply(getPolarity)
    df["sentiment"] = df["polarity"].apply(setClassification)
    np = df.groupby(["sentiment"]).count().to_numpy()
    values = [np[0][0], np[1][0], np[2][0]]
    return values

# For Testing.
print(values('en','US','bitcoin'))
#print(np)



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pygooglenews import GoogleNews
import datetime as dt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Translates foreign languages to en for better sentiment analysis.    
def parse(text):
    return TextBlob(text).translate(to='en') # Translates any news headlines to english.

# Polarity is the sentiment in numerical form.
def getPolarity(text):
    analyzer = SentimentIntensityAnalyzer()
    comp =  analyzer.polarity_scores(text)
    return comp['compound']

# Labels the sentiment.
def setClassification(polarity):
    if polarity < 0:
        return "Negative"
    elif polarity > 0:
        return "Positive"
    else:
        return "Neutral"

# Displaying the results
def display(df):
    sentiments = df.groupby(['sentiment'])['sentiment'].count()
    sentiments = sentiments / len(df) * 100

    return sentiments



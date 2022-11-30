"""
Copyright (c) 2022 - present GoCrypt
"""
import os
from django import template
import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from pycoingecko import CoinGeckoAPI 
from django.core.files import File
from .models import FavList
from tensorflow import keras
from keras.models import save_model
from keras.models import load_model
from django.http import JsonResponse
from PredictionAlgorithm.ETLandML.MLAlgorithms import sentimentAnalysis as sa
from PredictionAlgorithm.ETLandML.twitterdata import get_recent_tweets
import numpy as np
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
from yahoo_fin.stock_info import get_data
import pandas as pd

# CoinGeckoAPI define here to access in all function
cg = CoinGeckoAPI()

# Load index page after login
@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

# Load templates pages according to address or display error page
@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def marketlist(request):
    apidata = cg.get_coins_markets(vs_currency='usd', ids='bitcoin,ethereum,polkadot,cardano')
    favourite = False
    favarray = [[]]
    for i in apidata:
        if FavList.objects.filter(name = request.user, crypto = i['id']).exists():
                favourite = True
                value = {'id' : i['id'], 'favourite' : favourite}
                favarray.append(value)
                favourite = False
        else:
            value = {'id' : i['id'], 'favourite' : favourite}
            favarray.append(value)
    return render(request,"home/market.html",{'apidata':apidata, 'favarray': favarray})

def cryptocoin(request, id):
    id = id
    idLower = id.lower()

    # Call CoinGecko API to get crypto details
    apidata = cg.get_coins_markets(vs_currency='usd', ids=idLower, days='max')

    # Collect crypto symbol from API
    for a in apidata:
        symbol = a['symbol']

    # Sentiment Analysis Codes
    # DateTime for Sentiment Analysis
    td = dt.datetime.today()
    td = td - dt.timedelta(hours=10) # Twitter recent stream needs atleast a 10 sec delay.
    ytd = td - dt.timedelta(days = 1)

    # Format crypto name to match twitter hashtag.
    targetCrypto = "#{}".format(idLower)
    data = get_recent_tweets(targetCrypto, today=td,yesterday=ytd)
    df = pd.DataFrame(data)
    df["polarity"] = df["text"].apply(sa.getPolarity)
    df["sentiment"] = df["polarity"].apply(sa.setClassification)
    SAprediction = sa.display(df)

    # LSTM Codes
    targetCryptoLSTM = "{}-USD".format(symbol).upper()
    # create ticker for crypto
    df1 = []
    crypto = yf.Ticker(targetCryptoLSTM)

    # GET TODAYS DATE AND CONVERT IT TO A STRING WITH YYYY-MM-DD FORMAT (YFINANCE EXPECTS THAT FORMAT).
    yfdata = crypto.history(start=(dt.date.today() - dt.timedelta(days=7)).strftime('%Y-%m-%d'), end=dt.datetime.today().strftime('%Y-%m-%d'))
    yfdatalist = yfdata.values.tolist()
    
    for i in yfdatalist:
        # Store High Low CLose for each day in a 2 dimensional array.
        HLC = [i[1], i[2], i[3]]
        df1.append(HLC)
        # Loop through the whole array and get the last closing price for scaler reference.
        lastClosing = [i[3]]

    # Loading model
    if idLower == 'bitcoin':
        filepath = os.path.abspath('..')+"\\GoCryptTemplate\\PredictionAlgorithm\\Bitcoin_Model"
    elif idLower == 'ethereum':
        filepath = os.path.abspath('..')+"\\GoCryptTemplate\\PredictionAlgorithm\\Ethereum_Model"
    elif idLower == 'cardano':
        filepath = os.path.abspath('..')+"\\GoCryptTemplate\\PredictionAlgorithm\\Cardano_Model"
    elif idLower == 'polkadot':
        filepath = os.path.abspath('..')+"\\GoCryptTemplate\\PredictionAlgorithm\\Polkadot_Model"
    else:
        print("Crypto ID unidentified")

    model=keras.models.load_model(filepath)

    # 2 Scaler, one for processing input, one for collecting output.
    scaler = MinMaxScaler()
    inverse_scaler = MinMaxScaler()

    # Reshape both arrays to fit into the model.
    df_scaled = scaler.fit_transform(df1, (1,-1))
    df_scaled = df_scaled.reshape(1,7,3)

    lastClosingNP = np.array(lastClosing)
    df_scaled1 = lastClosingNP.reshape(1,1)
    df_scaled1 = inverse_scaler.fit_transform(df_scaled1)

    # Predict the daily Closing price with LSTM.
    prediction = model.predict(df_scaled)
    output = inverse_scaler.inverse_transform(prediction)
    LSTM = output[0][0]
    return render(request,"home/cryptodetails.html",{'apidata':apidata, 'id':id, 'SAPrediction':SAprediction, 'LSTM':LSTM})
    
# Get latest news to show in dashboard
def news(request):
	api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
	api = json.loads(api_request.content)
	return render(request, 'home/index.html', {'api': api,})

# To check if crypto has been added to favourite in database by user.
def checkinfavourites(request, crypto):
    favlist = FavList()
    username = request.user.__str__()
    isFavourite = False
    try:
        if FavList.objects.filter(name = request.user, crypto = crypto).exists():
            fav = FavList.objects.filter(name = request.user, crypto = crypto)
            fav.delete()
        else:
            favlist.name = username
            favlist.crypto = crypto
            favlist.save()
            isFavourite = True
    except (KeyError, favlist.DoesNotExist):
        return JsonResponse({'success': False, 'isFavourite':isFavourite})
    else:
        return JsonResponse({'success': True, 'isFavourite':isFavourite})

# Collect favourite crypto according to user and display in protfolio page.
def portfolio(request):
    apidata = cg.get_coins_markets(vs_currency='usd', ids='bitcoin,ethereum,polkadot,cardano')
    all_fav = FavList.objects.all()
    favlist = list(all_fav)
    return render(request,"home/portfolio.html",{'apidata':apidata, 'favarray': favlist})

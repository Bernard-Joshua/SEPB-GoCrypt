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
from django.http import JsonResponse
import keras
import tensorflow as tf
from tensorflow import keras
from keras.models import save_model
from keras.models import load_model

cg = CoinGeckoAPI()


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


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
    apidata = cg.get_coins_markets(vs_currency='usd', ids=id.lower(), days='max')
    return render(request,"home/cryptodetails.html",{'apidata':apidata, 'id':id})

def forecast(request, id):
    id = id
    apidata = cg.get_coins_markets(vs_currency='usd', ids=id.lower())
    return render(request,"home/forecast.html",{'apidata':apidata, 'id':id})

def news(request):
    
	api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
	api = json.loads(api_request.content)
	return render(request, 'home/index.html', {'api': api,})

@login_required
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

def portfolio(request):
    apidata = cg.get_coins_markets(vs_currency='usd', ids='bitcoin,ethereum,polkadot,cardano')
    all_fav = FavList.objects.all()
    favlist = list(all_fav)
    return render(request,"home/portfolio.html",{'apidata':apidata, 'favarray': favlist})

def bitcoinprediction(request):

    model=load_model("D:\fypvirtualenv\FYP\GoCrypt\SEPB-GoCrypt\Django-UI\GoCryptTemplate\SEPB_Model\Bitcoin_Model")

    predictions = model.predict()


    return request(
        json.dumps({"predictions": predictions}),
        content_type="application/json"
        )


    

# Loading the model
# model = tf.keras.models.load_model("my_h5_model.h5")

# def my_view(request):

#     predictions = model.predict(test_data)

#     return HTTPResponse(
#         json.dumps({"predictions": predictions}),
#         content_type="application/json"
#         )
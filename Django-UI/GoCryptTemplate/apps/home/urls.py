"""
Copyright (c) 2022 - present GoCrypt
"""

from django.urls import path, re_path   
from apps.home import views

urlpatterns = [

    
    path('', views.index, name='home'),
    path('market.html', views.marketlist, name='market'),
    path('portfolio.html', views.portfolio, name='portfolio'),
    path('cryptodetails.html/<id>', views.cryptocoin, name='cryptodetails'),
    path('forecast.html/<id>', views.forecast, name='forecast'),
    path('checkinfavourites/<crypto>', views.checkinfavourites, name='checkinfavourites'),
    path('index.html', views.news, name='news'),    
   
    re_path(r'^.*\.*', views.pages, name='pages'),

]

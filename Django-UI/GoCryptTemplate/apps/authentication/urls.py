# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present GoCrypt
"""
from django.contrib import admin
from django.urls import path, include, re_path
from .views import  login_view, register_user, password_reset_request
from django.conf import settings
from django.contrib.auth.views import LogoutView
from apps.home import views
from django.contrib.auth import views as auth_views
from django.apps import apps

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset_email/', auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_email.html'),
         name='password_reset_email'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'),
         name='password_reset_complete'),
    
 
]

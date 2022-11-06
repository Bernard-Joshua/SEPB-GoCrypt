# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present GoCrypt
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UpdateUserForm(forms.ModelForm):
        username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
        email = forms.EmailField(required=True,
                             widget=forms.TextInput(
                                attrs={'class': 'form-control'}))

class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
        avatar = forms.ImageField(widget=forms.FileInput(
            attrs={'class': 'form-control-file'}))
        bio = forms.CharField(widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 5}))

class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

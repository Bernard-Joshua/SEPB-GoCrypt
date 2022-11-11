# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present GoCrypt
"""
from django.db import models
from django.db.models import Model

# Model for User Favourite List
class FavList(models.Model):
    name = models.CharField(max_length=150)
    crypto = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'USER_FAV_LIST'


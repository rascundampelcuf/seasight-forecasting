# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:49:55 2020

@author: gizqu
"""

from django.conf.urls import include, url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.app, name='app'),
    url(r'^submit/', views.submit)
]
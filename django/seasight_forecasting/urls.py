# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:49:55 2020

@author: gizqu
"""

from django.conf.urls import include, url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/test', views.app, name='app'),
    url(r'^past/$', views.past, name='past'),
    url(r'^present/$', views.present, name='present'),
    url(r'^future/$', views.future, name='future'),
    url(r'^submit/', views.submit),
    url(r'^past/generateHistoricKML/', views.generateHistoricKML, name='generateHistoricKML'),
]
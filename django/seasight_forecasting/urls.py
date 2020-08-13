# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('past/', views.past, name='past'),
    path('past/', views.stop_thread, name='stop_thread'),
    path('present/', views.present, name='present'),
    path('future/', views.future, name='future'),
]
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:20:24 2020

@author: gizqu
"""

from random import randint

def GetBounds(alt, lat, lon):
    message = 'Alt {}_Lat {} Lon_{}'.format(alt, lat, lon)
    
    width = int(alt) * 25 / 2000
    height = int(alt) * 15 / 2000
    left = int(lon) - width
    right = int(lon) + width
    up = int(lat) + height
    down = int(lat) - height
    return left, right, up, down, message

def GetDataFromBounds(data, left, right, up, down):
    return data[(data['LAT'].between(down, up)) & (data['LON'].between(left, right))]
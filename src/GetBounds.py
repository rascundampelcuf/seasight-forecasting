# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:20:24 2020

@author: gizqu
"""

from random import randint

def GetBounds():
    altitude = [50, 4000]
    longitude = [-60, 10]
    latitude = [0, 60]
    
    alt = randint(altitude[0], altitude[1])
    lon = randint(longitude[0], longitude[1])
    lat = randint(latitude[0], latitude[1])
    
    message = 'Alt {}_Lat {} Lon_{}'.format(alt, lat, lon)
    
    width = alt * 25 / 2000
    height = alt * 15 / 2000
    left = lon - width
    right = lon + width
    up = lat + height
    down = lat - height
    return left, right, up, down, message

def GetDataFromBounds(data, left, right, up, down):
    return data[(data['LAT'].between(down, up)) & (data['LON'].between(left, right))]
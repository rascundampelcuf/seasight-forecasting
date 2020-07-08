import subprocess
from django.http import HttpResponseRedirect
from django.shortcuts import render

from seasight_forecasting.Clustering import *
from seasight_forecasting.GetBounds import *
from seasight_forecasting.GenerateKML import *

def index(request):
    return render(request, 'seasight_forecasting/index.html', {})

def app(request):
    return render(request, 'seasight_forecasting/app.html', {})

def past(request):
    return render(request, 'seasight_forecasting/past.html', {})

def present(request):
    return render(request, 'seasight_forecasting/present.html', {})

def future(request):
    return render(request, 'seasight_forecasting/future.html', {})

def generateHistoricKML(request):
    import ctypes  # An included library with Python install.
    alt = request.POST.get('dateFrom')[0]  
    ctypes.windll.user32.MessageBoxW(0, alt, "Your title", 0)
    return HttpResponseRedirect('/past')

def submit(request):
    alt = request.POST.get('altitude')
    lat = request.POST.get('latitude')
    lon = request.POST.get('longitude')
    n_clusters = 100
    data = LoadData('../data/dummy_data2.csv')
    left, right, up, down, message = GetBounds(alt, lat, lon)
    data = GetDataFromBounds(data, left, right, up, down)
    data = GetClusters(n_clusters, data)
    regions = GetRegions(n_clusters, data, InitCmap(data.SST))
    CreateKML(regions, '../data/final KMLs/SST_regions-' + message + '.kml')
    return HttpResponseRedirect('/')

import subprocess
from django.http import HttpResponseRedirect
from django.shortcuts import render

from seasight_forecasting.GenerateHistoricKML import *

def index(request):
    return render(request, 'seasight_forecasting/index.html', {})

def app(request):
    return render(request, 'seasight_forecasting/app.html', {})

def past(request):
    if request.method == 'GET':
        context = {}
    else:
        region = request.POST.get('region')
        dateFrom = request.POST.get('dateFrom')
        check = request.POST.get('check')    
        dateTo = request.POST.get('dateTo')
        alt = request.POST.get('altitude')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        message = GenerateHistoricKML(region, dateFrom, check, dateTo, alt, lat, lon)
        #ctypes.windll.user32.MessageBoxW(0, message, "Your title", 0)
        context = {'response': message, 'ok': 1, 'fail': 0}
    return render(request, 'seasight_forecasting/past.html', context)

def present(request):
    return render(request, 'seasight_forecasting/present.html', {})

def future(request):
    return render(request, 'seasight_forecasting/future.html', {})

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

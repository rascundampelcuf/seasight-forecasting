import subprocess
from django.http import HttpResponseRedirect
from django.shortcuts import render

from seasight_forecasting.ConfigurationFile import *
from seasight_forecasting.GenerateKMLMethods import *

from seasight_forecasting import global_vars

def index(request):
    LoadConfigFile()
    return render(request, 'seasight_forecasting/index.html', {})

def app(request):
    return render(request, 'seasight_forecasting/app.html', {})

def past(request):    
    min_date, max_date = GetDate()
    context = {'min_date': min_date, 'max_date': max_date}

    region = request.POST.get('region')
    dateFrom = request.POST.get('dateFrom')
    check = request.POST.get('check')
    dateTo = request.POST.get('dateTo')
    alt = request.POST.get('altitude')
    lat = request.POST.get('latitude')
    lon = request.POST.get('longitude')
    GenerateHistoricKML(region, dateFrom, check, dateTo, alt, lat, lon)
    return render(request, 'seasight_forecasting/past.html', context)

def present(request):
    region = request.POST.get('region')
    alt = request.POST.get('altitude')
    lat = request.POST.get('latitude')
    lon = request.POST.get('longitude')
    GenerateRealTimeKML(region, alt, lat, lon)
    return render(request, 'seasight_forecasting/present.html', {})

def future(request):
    region = request.POST.get('region')
    alt = request.POST.get('altitude')
    lat = request.POST.get('latitude')
    lon = request.POST.get('longitude')
    GenerateFutureKML(region, alt, lat, lon)
    return render(request, 'seasight_forecasting/future.html', {})

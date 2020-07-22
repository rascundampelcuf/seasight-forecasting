import subprocess
from django.http import HttpResponseRedirect
from django.shortcuts import render

from seasight_forecasting.GenerateKMLMethods import *

def index(request):
    return render(request, 'seasight_forecasting/index.html', {})

def app(request):
    return render(request, 'seasight_forecasting/app.html', {})

def past(request):
    if request.method == 'GET':
        min_date, max_date = GetDate()
        context = {'min_date': min_date, 'max_date': max_date}
    else:
        region = request.POST.get('region')
        dateFrom = request.POST.get('dateFrom')
        check = request.POST.get('check')
        dateTo = request.POST.get('dateTo')
        alt = request.POST.get('altitude')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        message = GenerateHistoricKML(region, dateFrom, check, dateTo, alt, lat, lon)
        context = {'response': message}
    return render(request, 'seasight_forecasting/past.html', context)

def present(request):
    if request.method == 'GET':
        context = {}
    else:
        region = request.POST.get('region')
        alt = request.POST.get('altitude')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        message = GenerateRealTimeKML(region, alt, lat, lon)
        context = {'response': message}
    return render(request, 'seasight_forecasting/present.html', context)

def future(request):
    if request.method == 'GET':
        context = {}
    else:
        region = request.POST.get('region')
        alt = request.POST.get('altitude')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        message = GenerateFutureKML(region, alt, lat, lon)
        context = {'response': message}
    return render(request, 'seasight_forecasting/future.html', context)

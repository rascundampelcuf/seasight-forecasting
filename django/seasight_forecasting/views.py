import subprocess
from django.http import HttpResponseRedirect
from django.shortcuts import render

from seasight_forecasting.ConfigurationFile import *
from seasight_forecasting.CaseMethods import *

from seasight_forecasting import global_vars

def index(request):
    LoadConfigFile()
    return render(request, 'seasight_forecasting/index.html', {})

def past(request):
    LoadConfigFile()
    min_date, max_date = GetDate()
    context = {'min_date': min_date, 'max_date': max_date}
    if request.method == 'POST':    
        region = request.POST.get('region')
        dateFrom = request.POST.get('dateFrom')
        check = request.POST.get('check')
        dateTo = request.POST.get('dateTo')
        GenerateHistoricKML(region, dateFrom, check, dateTo)
    return render(request, 'seasight_forecasting/past.html', context)

def present(request):
    LoadConfigFile()
    if request.method == 'POST':
        region = request.POST.get('region')
        GenerateRealTimeKML(region)
    return render(request, 'seasight_forecasting/present.html', {})

def future(request):
    LoadConfigFile()
    if request.method == 'POST':
        region = request.POST.get('region')
        GenerateFutureKML(region)
    return render(request, 'seasight_forecasting/future.html', {})

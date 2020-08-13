
from django.http import HttpResponseRedirect
from django.shortcuts import render
from seasight_forecasting import global_vars
from seasight_forecasting.utils import *
from seasight_forecasting.ConfigurationFile import *
from seasight_forecasting.CaseMethods import *

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
        startSendKMLThread()
    return render(request, 'seasight_forecasting/past.html', context)

def stop_thread(request):
    if request.method == 'POST':
        stopSendKMLThread()
    return render(request, 'seasight_forecasting/past.html', {})

def present(request):
    LoadConfigFile()
    if request.method == 'POST':
        region = request.POST.get('region')
        GenerateRealTimeKML(region)
        sendKmlToLG(global_vars.kml_destination_filename)
    return render(request, 'seasight_forecasting/present.html', {})

def future(request):
    LoadConfigFile()
    if request.method == 'POST':
        region = request.POST.get('region')
        GenerateFutureKML(region)
        sendKmlToLG(global_vars.kml_destination_filename)
    return render(request, 'seasight_forecasting/future.html', {})

def demo(request):
    LoadConfigFile()
    #if request.method == 'POST':
        #GenerateDemo()
    return HttpResponseRedirect("/")
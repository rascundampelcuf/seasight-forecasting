
from django.http import HttpResponseRedirect
from django.shortcuts import render
from seasight_forecasting import global_vars
from seasight_forecasting.utils import *
from seasight_forecasting.ConfigurationFile import *
from seasight_forecasting.CaseMethods import *

def index(request):
    LoadConfigFile()
    cleanVerbose()
    return render(request, 'index.html', {})

def run_historic(request):
    region = request.POST.get('region')
    dateFrom = request.POST.get('dateFrom')
    check = request.POST.get('check')
    dateTo = request.POST.get('dateTo')
    region = GetRegionFromFile(request.POST.get('region'))
    GenerateHistoricKML(region, dateFrom, check, dateTo)
    startSendKMLThread()
    flyToRegion(region)

def stop_thread():
    stopSendKMLThread()

def past(request):
    LoadConfigFile()
    min_date, max_date = GetDate()
    context = {'min_date': min_date, 'max_date': max_date}

    if request.method == 'POST':
        if request.POST.get("Submit") == "Submit":
            cleanVerbose()
            run_historic(request)
        if request.POST.get("Stop") == "Stop":
            stop_thread()

    return render(request, 'past.html', context)

def present(request):
    LoadConfigFile()
    if request.method == 'POST':
        cleanVerbose()
        region = GetRegionFromFile(request.POST.get('region'))
        GenerateRealTimeKML(region)
        sendKmlToLGCommon(global_vars.kml_destination_filename)
        flyToRegion(region)
    return render(request, 'present.html', {})

def future(request):
    LoadConfigFile()
    if request.method == 'POST':
        cleanVerbose()
        region = GetRegionFromFile(request.POST.get('region'))
        GenerateFutureKML(region)
        sendKmlToLGCommon(global_vars.kml_destination_filename)
        flyToRegion(region)
    return render(request, 'future.html', {})

def demo(request):
    LoadConfigFile()
    #if request.method == 'POST':
        #GenerateDemo()
    return HttpResponseRedirect("/")
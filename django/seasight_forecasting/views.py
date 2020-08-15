
from django.http import HttpResponseRedirect
from django.shortcuts import render
from seasight_forecasting import global_vars
from seasight_forecasting.utils import *
from seasight_forecasting.ConfigurationFile import *
from seasight_forecasting.CaseMethods import *

def index(request):
    LoadConfigFile()
    return render(request, 'index.html', {})

def run_historic(request):
    region = request.POST.get('region')
    dateFrom = request.POST.get('dateFrom')
    check = request.POST.get('check')
    dateTo = request.POST.get('dateTo')
    GenerateHistoricKML(region, dateFrom, check, dateTo)
    startSendKMLThread()

def stop_thread():
    stopSendKMLThread()

def past(request):
    LoadConfigFile()
    min_date, max_date = GetDate()
    context = {'min_date': min_date, 'max_date': max_date}

    if request.method == 'POST':
        if request.POST.get("Submit") == "Submit":
            run_historic(request)
        if request.POST.get("Stop") == "Stop":
            stop_thread()

    return render(request, 'past.html', context)



def present(request):
    LoadConfigFile()
    if request.method == 'POST':
        region = request.POST.get('region')
        GenerateRealTimeKML(region)
        sendKmlToLG(global_vars.kml_destination_filename)
    return render(request, 'present.html', {})

def future(request):
    LoadConfigFile()
    if request.method == 'POST':
        region = request.POST.get('region')
        GenerateFutureKML(region)
        sendKmlToLG(global_vars.kml_destination_filename)
    return render(request, 'future.html', {})

def demo(request):
    LoadConfigFile()
    #if request.method == 'POST':
        #GenerateDemo()
    return HttpResponseRedirect("/")
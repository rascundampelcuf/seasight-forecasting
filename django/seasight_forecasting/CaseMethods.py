
from seasight_forecasting import global_vars
from seasight_forecasting.Clustering import *
from seasight_forecasting.GenerateKML import *
from seasight_forecasting.ManageData import *
from seasight_forecasting.ManageModel import *

def GetDate():
    data = LoadData(global_vars.historic_file_path)
    data.time = pd.to_datetime(data.time, errors='coerce', format='%Y-%m-%d %H:%M:%S')
    min_date = str(data.time.min().date())
    max_date = str(data.time.max().date())
    return min_date, max_date

def PrepareData(data):
    data.time = pd.to_datetime(data.time, errors='coerce', format='%Y-%m-%d %H:%M:%S')
    data.lon = pd.to_numeric(data.lon, errors='coerce').fillna(0).astype(float)
    data.lat = pd.to_numeric(data.lat, errors='coerce').fillna(0).astype(float)
    data.sst = round(pd.to_numeric(data.sst, errors='coerce').fillna(0).astype(float), 1)
    return data

def CreateSingleFrameKML(data):
    print('Number of clusters: {}'.format(global_vars.number_of_clusters))
    data = GetClusters(global_vars.number_of_clusters, data)
    regions = GetRegions(global_vars.number_of_clusters, data, InitCmap(data.sst.min(), data.sst.max()), False)
    CreateKML(regions, False)
    return 'Created KML files in {}'.format(global_vars.kml_destination_path)

def GenerateHistoricKML(region, dateFrom, check, dateTo):
    data = LoadData(global_vars.historic_file_path)
    data = PrepareData(data)
    print('ORIGINAL DATA:')
    print(data)

    data = GetDataInDateRange(data, dateFrom, check, dateTo)
    print('DATA AFTER DATE FILTER:')
    print(data)

    data = GetDataFromRegion(data, region)
    print('DATA AFTER REGION FILTER:')
    print(data)

    try:
        regions = []
        for group in data.groupby(['time']):
            data = group[1]
            data = data.drop(['time'], axis=1)
            ngroup = GetClusters(global_vars.number_of_clusters, data)
            regions.append(GetRegions(global_vars.number_of_clusters, ngroup, InitCmap(data.sst.min(), data.sst.max()), group[0].date()))
        CreateKML(regions, True)
        message = 'Created KML files in {}'.format(global_vars.kml_destination_path)
    except Exception as e:
        message = "ERROR: {}".format(e)
    print(message)

def GenerateRealTimeKML(region):    
    data = GetDataFromAPI()
    data = PrepareData(data)
    data = data.drop(['time'], axis=1)
    print('ORIGINAL DATA:')
    print(data)

    data = GetDataFromRegion(data, region)
    print('DATA AFTER REGION FILTERING:')
    print(data)

    try:
        message = CreateSingleFrameKML(data)
    except Exception as e:
        message = "ERROR: {}".format(e)
    print(message)

def GenerateFutureKML(region):
    data = LoadData(global_vars.historic_file_path)
    data = data[data.time == data.time.tail(1)[data.time.tail(1).index.start]]
    data = PrepareData(data)
    data = data.drop(['time'], axis=1)    
    print('ORIGINAL DATA:')
    print(data)

    data = GetDataFromRegion(data, region)
    print('DATA AFTER REGION FILTERING:')
    print(data)

    data = PredictedData(data)
    print('PREDICTED DATA:')
    print(data)

    try:
        message = CreateSingleFrameKML(data)
    except Exception as e:
        message = "ERROR: {}".format(e)
    print(message)

from seasight_forecasting import global_vars

from seasight_forecasting.Clustering import *
from seasight_forecasting.GetBounds import *
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
    data.sst = pd.to_numeric(data.sst, errors='coerce').fillna(0).astype(float)
    return data

def CreateSingleFrameKML(data):
    print('Number of clusters: {}'.format(global_vars.number_of_clusters))
    data = GetClusters(global_vars.number_of_clusters, data)
    regions = GetRegions(global_vars.number_of_clusters, data, InitCmap(data['sst']), False)
    CreateKML(regions, global_vars.kml_destination, False)
    return 'Created KML file in {}'.format(global_vars.kml_destination)

def GenerateHistoricKML(region, dateFrom, check, dateTo, alt, lat, lon):
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
    # alt, lat, lon = GetParameters()
    #left, right, up, down = GetBounds(alt, lat, lon)
    #data = GetDataFromBounds(data, left, right, up, down)
    try:
        regions = []
        for group in data.groupby(['time']):
            data = group[1]
            data = data.drop(['time'], axis=1)
            ngroup = GetClusters(global_vars.number_of_clusters, data)
            regions.append(GetRegions(global_vars.number_of_clusters, ngroup, InitCmap(data['sst']), group[0].date()))
        CreateKML(regions, global_vars.kml_destination, True)
        message = 'Created KML file in {}'.format(global_vars.kml_destination)
    except Exception as e:
        message = "ERROR: {}".format(e)
    print(message)

def GenerateRealTimeKML(region, alt, lat, lon):    
    data = GetDataFromAPI()
    data = PrepareData(data)
    data = data.drop(['time'], axis=1)
    print('ORIGINAL DATA:')
    print(data)
    data = GetDataFromRegion(data, region)
    print('DATA AFTER REGION FILTERING:')
    print(data)
    # alt, lat, lon = GetParameters()
    # left, right, up, down = GetBounds(alt, lat, lon)
    # data = GetDataFromBounds(data, left, right, up, down)
    #try:
    message = CreateSingleFrameKML(data)
    #except Exception as e:
        #message = "ERROR: {}".format(e)
    print(message)

def GenerateFutureKML(region, alt, lat, lon):
    data = LoadData(global_vars.historic_file_path)
    data = data[data.time == data.time.tail(1)[data.time.tail(1).index.start]]
    data = PrepareData(data)
    data = data.drop(['time'], axis=1)    
    print('ORIGINAL DATA:')
    data = GetDataFromRegion(data, region)
    print('DATA AFTER REGION FILTERING:')
    print(data)
    model = LoadLRModel()
    data = LRPrediction(data, model)
    print('PREDICTED DATA:')
    print(data)

    #model = LoadRNNModel()
    #print(model)
    #data = data.drop(['time'], axis=1)
    #print(type(data.lon[0]))
    #data.lon = pd.to_numeric(data.lon, downcast="float")
    #data.lat = pd.to_numeric(data.lat, downcast="float")
    #data = NewPrediction(data, model)
    # alt, lat, lon = GetParameters()
    # left, right, up, down = GetBounds(alt, lat, lon)
    # data = GetDataFromBounds(data, left, right, up, down)
    try:
        message = CreateSingleFrameKML(data)
    except Exception as e:
        message = "ERROR: {}".format(e)
    print(message)
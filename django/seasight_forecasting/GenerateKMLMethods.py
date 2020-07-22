
from seasight_forecasting.ManageData import *
from seasight_forecasting.Clustering import *
from seasight_forecasting.GetBounds import *
from seasight_forecasting.GenerateKML import *

def GetDate():
    data = LoadData('../data/past.csv')
    data.time = pd.to_datetime(data.time, errors='coerce', format='%Y-%m-%d %H:%M:%S')
    min_date = str(data.time.min().date())
    max_date = str(data.time.max().date())
    return min_date, max_date

def GenerateHistoricKML(region, dateFrom, check, dateTo, alt, lat, lon):
    n_clusters = 200
    data = LoadData('../data/past.csv')
    data.time = pd.to_datetime(data.time, errors='coerce', format='%Y-%m-%d %H:%M:%S')
    data = GetDataInDateRange(data, dateFrom, check, dateTo)
    data.lon = pd.to_numeric(data.lon, downcast="float")
    data.lat = pd.to_numeric(data.lat, downcast="float")
    data.sst = pd.to_numeric(data.sst, downcast="float")
    data = GetDataFromRegion(data, region)
    # alt, lat, lon = GetParameters()
    #left, right, up, down = GetBounds(alt, lat, lon)
    #data = GetDataFromBounds(data, left, right, up, down)
    #try:
    regions = []
    for group in data.groupby(['time']):
        data = group[1]
        data = data.drop(['time'], axis=1)
        ngroup = GetClusters(n_clusters, data)
        regions.append(GetRegions(n_clusters, ngroup, InitCmap(data['sst']), group[0].date()))
    path = 'seasight_forecasting/static/seasight_forecasting/kml/SST_regions.kml'
    CreateKML(regions, path, True)
    message = 'Created KML file in {}'.format(path)
    #except Exception as e:
        #message = "ERROR: {}".format(e)
    return message

def GenerateRealTimeKML(region, alt, lat, lon):
    n_clusters = 200
    data = LoadData('../data/present.csv')
    data.lon = pd.to_numeric(data.lon, downcast="float")
    data.lat = pd.to_numeric(data.lat, downcast="float")
    data = data.drop(['time'], axis=1)
    data = GetDataFromRegion(data, region)
    # alt, lat, lon = GetParameters()
    # left, right, up, down = GetBounds(alt, lat, lon)
    # data = GetDataFromBounds(data, left, right, up, down)
    try:
        data = GetClusters(n_clusters, data)
        regions = GetRegions(n_clusters, data, InitCmap(data['sst']), False)
        path = 'seasight_forecasting/static/seasight_forecasting/kml/SST_regions.kml'
        CreateKML(regions, path, False)
        message = 'Created KML file in {}'.format(path)
    except Exception as e:
        message = "ERROR: {}".format(e)
    return message

def GenerateFutureKML(region, alt, lat, lon):
    n_clusters = 200
    data = LoadData('../data/future.csv')    
    data.lon = pd.to_numeric(data.lon, downcast="float")
    data.lat = pd.to_numeric(data.lat, downcast="float")
    data = data.drop(['time'], axis=1)
    data = GetDataFromRegion(data, region)
    # alt, lat, lon = GetParameters()
    # left, right, up, down = GetBounds(alt, lat, lon)
    # data = GetDataFromBounds(data, left, right, up, down)
    try:
        data = GetClusters(n_clusters, data)
        regions = GetRegions(n_clusters, data, InitCmap(data['sst']), False)
        path = 'seasight_forecasting/static/seasight_forecasting/kml/SST_regions.kml'
        CreateKML(regions, path, False)
        message = 'Created KML file in {}'.format(path)
    except Exception as e:
        message = "ERROR: {}".format(e)
    return message
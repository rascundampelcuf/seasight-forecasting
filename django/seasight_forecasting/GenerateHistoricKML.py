
from seasight_forecasting.Clustering import *
from seasight_forecasting.GetBounds import *
from seasight_forecasting.GenerateKML import *

def GenerateHistoricKML(region, dateFrom, check, dateTo, alt, lat, lon):
    n_clusters = 50
    data = LoadData('../data/dummy_data2.csv')
    # alt, lat, lon = GetParameters()
    left, right, up, down, label = GetBounds(alt, lat, lon)
    data = GetDataFromBounds(data, left, right, up, down)
    try:
        data = GetClusters(n_clusters, data)
        regions = GetRegions(n_clusters, data, InitCmap(data.SST))
        path = '../data/final KMLs/SST_regions-' + label + '.kml'
        CreateKML(regions, path)
        message = 'Created KML file in {}'.format(path)
    except Exception as e:
        message = "ERROR: {}".format(e)
    return message
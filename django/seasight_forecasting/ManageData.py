
import datetime
import geopandas as gpd
import pandas as pd
from shapely.ops import cascaded_union

def LoadData(data_path):    
    return pd.read_csv(data_path)

def GetDataFromRegion(data, region):
    regions = {
        "North Atlantic Ocean": '../data/regions/north_atlantic.geojson',
        "South Atlantic Ocean": '../data/regions/south_atlantic.geojson',
        "Indian Ocean": '../data/regions/indian.geojson',
        "West Pacific Ocean": '../data/regions/west_pacific.geojson',
        "East Pacific Ocean": '../data/regions/east_pacific.geojson',
    }
    regionFile = gpd.read_file(regions[region])
    pol = cascaded_union(regionFile['geometry'])
    pol_gpd= gpd.GeoDataFrame()
    pol_gpd['geometry'] = None
    pol_gpd.loc[0,'geometry'] = pol
    gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.lon, data.lat))
    data = gpd.sjoin(gdf, pol_gpd, op = 'within')
    data = data.drop(['geometry', 'index_right'], axis=1)
    return data

def GetDataInDateRange(data, dateFrom, check, dateTo):
    data = data[data.time > dateFrom]
    if check:
        data = data[data.time < str((datetime.datetime.strptime(dateTo, '%Y-%m-%d') + datetime.timedelta(days=1)))]
    print(data)
    print(dateFrom)
    print(dateTo)
    return data
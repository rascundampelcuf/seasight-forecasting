
import cdsapi
import datetime
import os
import shutil
import zipfile
import geopandas as gpd
import pandas as pd
import xarray as xr
from shapely.ops import cascaded_union

def LoadData(data_path):    
    return pd.read_csv(data_path)

def GetDataFromAPI():
    data = ''
    tmpPath = 'tmp/'
    filePath = 'file/'

    os.mkdir(tmpPath)

    c = cdsapi.Client()
    c.retrieve(
        'satellite-sea-surface-temperature',
        {
            'processinglevel': 'level_4',
            'sensor_on_satellite': 'combined_product',
            'version': '2_0',
            'year': '2018',
            'month': '12',
            'day': '31',
            'variable': 'all',
            'format': 'zip',
        },
        tmpPath + 'download.zip')

    with zipfile.ZipFile(tmpPath + 'download.zip', 'r') as zip_ref:
        zip_ref.extractall(tmpPath + filePath)
    
    for filename in os.listdir(tmpPath + filePath):
        print('Downloaded file: {}'.format(filename))
        with xr.open_dataset(tmpPath + filePath + '/' + filename) as ds:
            df = (ds.to_dataframe()).dropna()
            df = df.rename(columns={"analysed_sst": "sst"})
            df = df.drop(['analysis_uncertainty', 'sea_ice_fraction', 'mask'], axis=1).reset_index()
            df['sst'] = df['sst'].apply(lambda x: x - 273,15)
            df['lat'] = df['lat'].apply(lambda x: round(x * 2) / 2)
            df['lon'] = df['lon'].apply(lambda x: round(x * 2) / 2)
            data = df.groupby(['time', 'lat', 'lon'])['sst'].mean().reset_index()
    
    shutil.rmtree(tmpPath, ignore_errors=True)
    print('Temporary files removed!')

    return data

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
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 16:51:18 2020

@author: gizqu
"""

import cdsapi

c = cdsapi.Client()

c.retrieve(
    'satellite-sea-surface-temperature',
    {
        'variable': 'all',
        'format': 'zip',
        'processinglevel': 'level_4',
        'sensor_on_satellite': 'combined_product',
        'version': '2_0',
        'year': '2018',
        'month': '01',
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
    },
    'download.zip')

#%%

import os
import xarray as xr

path = 'D:\\git\\Seasight-Forecasting\\src\\new\\'
target = 'D:\\git\\Seasight-Forecasting\\data\\'

for folder in os.listdir(path):
    print(folder)
    for filename in os.listdir(path + folder):
        print(filename)
        ds = xr.open_dataset(path + folder + '\\' + filename)
        df = (ds.to_dataframe()).dropna()
        df = df.rename(columns={"analysed_sst": "sst"})
        df = df.drop(['analysis_uncertainty', 'sea_ice_fraction', 'mask'], axis=1).reset_index()
        df['sst'] = df['sst'].apply(lambda x: x - 273,15)
        df['lat'] = df['lat'].apply(lambda x: round(x * 2) / 2)
        df['lon'] = df['lon'].apply(lambda x: round(x * 2) / 2)
        df = df.groupby(['time', 'lat', 'lon'])['sst'].mean().reset_index()
        target_file = target + folder + '.csv'
        df.to_csv(target_file, mode='a', index=False)
        print('{} file created!'.format(target_file))
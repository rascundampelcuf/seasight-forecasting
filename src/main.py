# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 12:26:04 2020

@author: gizqu
"""

from Clustering import *
from GetBounds import *
from GenerateKML import *

def main():
    n_clusters = 100
    data = LoadData('../data/dummy_data2.csv')
    left, right, up, down, message = GetBounds()
    data = GetDataFromBounds(data, left, right, up, down)
    data = GetClusters(n_clusters, data)
    regions = GetRegions(n_clusters, data, InitCmap(data.SST))
    CreateKML(regions, '../data/final KMLs/SST_regions-' + message + '.kml')

if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 12:28:13 2020

@author: gizqu
"""

# Import libraries
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial import ConvexHull
import math
import numpy as np

#%%

data_path = '../data/dummy_data2.csv'
X = pd.read_csv(data_path)

n_clusters = 31

cluster = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
cluster.fit_predict(X)

X['labels'] = cluster.labels_


kwargs = dict(alpha=0.0, lmax=1.0)

regions = []

for cluster in range(n_clusters):
    points = X[X.labels == cluster]
    point_cloud = points[['rLAT', 'rLON']].to_numpy()

    point_cloud = points[['rLON', 'rLAT']].to_numpy()
    hull = ConvexHull(point_cloud)

    pts = np.vstack([point_cloud[x] for x in hull.simplices])
    pp = list(set([tuple(row) for row in pts]))
    
    cent=(sum([p[0] for p in pp])/len(pp),sum([p[1] for p in pp])/len(pp))
    pp.sort(key=lambda p: math.atan2(p[1]-cent[1],p[0]-cent[0]))

    pp.append(pp[0])
    regions.append(pp)

#%%

def GetCoords(region):
    string = ''
    for p in region:
        string += '{},{},0\n'.format(p[0], p[1])
    return string

from lxml import etree
from pykml.factory import KML_ElementMaker as KML

fich_kml = KML.kml(
    KML.Document(        
        KML.Folder(
            KML.name('Temperature regions'),
            id='lugares'
            )
        )
    )

for region in regions:
    fich_kml.Document.Folder.append(
        KML.Placemark(
            KML.Polygon(
                KML.outerBoundaryIs(
                    KML.LinearRing(
                        KML.coordinates(GetCoords(region))
                        )
                    )
                )
            )
        )

f = open("test4.kml", "w")
out = etree.tostring(fich_kml, pretty_print=True).decode("utf-8")
f.write(out)
f.close()
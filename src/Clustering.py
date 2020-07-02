# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 12:28:13 2020

@author: gizqu
"""

# Import libraries
import math
import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from scipy.spatial import ConvexHull
from sklearn.cluster import AgglomerativeClustering

#%%

def rgb_to_hex(rgb):
    return 'ff%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

data_path = '../data/dummy_data2.csv'
X = pd.read_csv(data_path)

n_clusters = 31

cluster = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
cluster.fit_predict(X)

X['labels'] = cluster.labels_

norm = mpl.colors.Normalize(X.SST.min(), X.SST.max())
cmap = cm.viridis_r
m = cm.ScalarMappable(norm=norm, cmap=cmap)

regions = []

for cluster in range(n_clusters):
    points = X[X.labels == cluster]
    point_cloud = points[['rLAT', 'rLON']].to_numpy()

    point_cloud = points[['rLON', 'rLAT']].to_numpy()
    hull = ConvexHull(point_cloud)
    # Get first point from ConvexHull lines in order to create a polygon
    pts = np.vstack([point_cloud[x] for x in hull.simplices])
    pp = list(set([tuple(row) for row in pts]))
    # Compute centroid
    cent=(sum([p[0] for p in pp])/len(pp),sum([p[1] for p in pp])/len(pp))
    # Sort by polar angle
    pp.sort(key=lambda p: math.atan2(p[1]-cent[1],p[0]-cent[0]))

    pp.append(pp[0])
    pp.append(rgb_to_hex(m.to_rgba(points.SST.mean())))
    pp.append(cluster)
    regions.append(pp)
#%%
import matplotlib as mpl
import matplotlib.cm as cm
norm = mpl.colors.Normalize(X.SST.min(), X.SST.max())
cmap = cm.viridis
x = 21.100008


m = cm.ScalarMappable(norm=norm, cmap=cmap)
print(m.to_rgba(x))

print(cmap(21.1))

#%%

def GetCoords(region):
    string = ''
    for p in region:
        string += '{},{},0\n'.format(p[0], p[1])
    return string

fich_kml = KML.kml(
    KML.Document(        
        KML.Folder(
            KML.name('Temperature regions'))
        )
    )

for region in regions:
    styleNumber = region.pop()
    color = region.pop()
    fich_kml.Document.Folder.append(
        KML.Placemark(
            KML.Style(
            KML.PolyStyle(
                KML.color(color)
                )
            ),
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
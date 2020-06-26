# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 14:20:33 2020

@author: gizqu
"""

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial import distance
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as shc
from polylidar import extractPlanesAndPolygons, extractPolygons, Delaunator

#%%

data_path = '../data/dummy_data2.csv'
data = pd.read_csv(data_path)

#%%

X = data
print(X)

#%%

plt.figure(figsize=(10, 7))
plt.scatter(X.rLON, X.rLAT)
plt.show()

#%%

plt.figure(figsize=(10, 7))
dend = shc.dendrogram(shc.linkage(X, method='ward'))
#%%

cluster = AgglomerativeClustering(n_clusters=31, affinity='euclidean', linkage='ward')
cluster.fit_predict(X)
print(cluster.labels_)
X['labels'] = cluster.labels_

plt.figure(figsize=(10, 7))
plt.scatter(X.rLON, X.rLAT, c=cluster.labels_, cmap='rainbow')
plt.show()

#%%

kwargs = dict(alpha=0.0, lmax=1.0)

points = X[X.labels == 28]
point_cloud = points[['rLAT', 'rLON']].to_numpy()
delaunay, planes, polygons = extractPlanesAndPolygons(point_cloud, **kwargs)
polygons = extractPolygons(point_cloud, **kwargs)
print(polygons)
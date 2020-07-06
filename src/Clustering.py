# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 12:28:13 2020

@author: gizqu
"""

# Import libraries
import math
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pylab as pl
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from scipy.spatial import ConvexHull
from sklearn.cluster import AgglomerativeClustering

def LoadData(data_path):    
    return pd.read_csv(data_path)

def GetCoords(region):
    string = ''
    for p in region:
        string += '{},{},0\n'.format(p[0], p[1])
    return string

def rgb_to_hex(rgb):
    return 'ff%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def InitCmap(SST):
    norm = mpl.colors.Normalize(SST.min(), SST.max())
    cmap = cm.viridis_r
    smap = cm.ScalarMappable(norm=norm, cmap=cmap)
    
    
    fig = plt.figure(figsize=(8, 3), facecolor = "white")
    fig.patch.set_alpha(0.0) 
    ax = fig.add_axes([0.05, 0.80, 0.9, 0.15])
    ax.patch.set_alpha(0.0)
    cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                orientation='horizontal')

    return smap

def GetClusters(n_clusters, data):
    cluster = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
    cluster.fit_predict(data)    
    data['labels'] = cluster.labels_
    return data

def GetRegions(n_clusters, data, cmap):
    regions = []
    for cluster in range(n_clusters):
        points = data[data.labels == cluster]    
        point_cloud = points[['LON', 'LAT']].to_numpy()
        hull = ConvexHull(point_cloud)
        # Get first point from ConvexHull lines in order to create a polygon
        pts = np.vstack([point_cloud[x] for x in hull.simplices])
        region = list(set([tuple(row) for row in pts]))
        # Compute centroid
        cent=(sum([p[0] for p in region])/len(region),sum([p[1] for p in region])/len(region))
        # Sort by polar angle
        region.sort(key=lambda p: math.atan2(p[1]-cent[1],p[0]-cent[0]))
        # Copied the first element in the last position in order to close the circle
        region.append(region[0])
        # Convert the mean temperature value into RGB values into HEX value
        region.append(rgb_to_hex(cmap.to_rgba(points.SST.mean())))
        regions.append(region)
    return regions

def CreateKML(regions, path):
    fich_kml = KML.kml(
        KML.Document(        
            KML.Folder(
                KML.name('Temperature regions'))
            )
        )
    
    for region in regions:
        color = region.pop()
        fich_kml.Document.Folder.append(
            KML.Placemark(
                KML.Style(
                KML.PolyStyle(
                    KML.color(color),
                    KML.outline(0)
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
    
    f = open(path, "w")
    out = etree.tostring(fich_kml, pretty_print=True).decode("utf-8")
    f.write(out)
    f.close()


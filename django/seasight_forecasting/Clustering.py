# -*- coding: utf-8 -*-

# Import libraries
import datetime
import math
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
from sklearn.cluster import AgglomerativeClustering

from seasight_forecasting import global_vars

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
    mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='horizontal')
    plt.savefig(global_vars.image_destination_path + 'colorbar.png')
    return smap

def GetClusters(n_clusters, data):
    cluster = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
    cluster.fit_predict(data)    
    data['labels'] = cluster.labels_
    return data

def GetRegions(n_clusters, data, cmap, date):
    regions = []
    for cluster in range(n_clusters):
        points = data[data.labels == cluster]    
        point_cloud = points[['lon', 'lat']].to_numpy()
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
        region.append(rgb_to_hex(cmap.to_rgba(points['sst'].mean())))
        if date:
            date_from = date
            date_to = date_from + datetime.timedelta(days=1)
            region.append([str(date_from), str(date_to)])
        regions.append(region)
    return regions


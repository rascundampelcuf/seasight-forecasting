# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 14:20:33 2020

@author: gizqu
"""


# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.spatial import distance

#%%

data_path = '../data/dummy_data.csv'
data = pd.read_csv(data_path)

#%%

data2 = data[:100]
print(data2)


methods = ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward']

fig, ax = plt.subplots(4, 2, figsize=(8, 8))
plt.subplots_adjust(hspace = .4)

for i in range(len(methods)):
    threshold = 0.3
    linkage = hierarchy.linkage(data2, method=methods[i])
    
    clusters = hierarchy.fcluster(linkage, threshold, criterion='distance')
    
    temp = 421+i
    ax=plt.subplot(temp)
    
    hierarchy.dendrogram(linkage, color_threshold=0.3)
    ax.set_title('Method: {}'.format(methods[i]))
plt.show()
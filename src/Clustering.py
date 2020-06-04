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

data2 = data[:25]
print(data2)


data2 = distance.squareform(data2)
threshold = 0.3
linkage = hierarchy.linkage(data2, method="single")
clusters = hierarchy.fcluster(linkage, threshold, criterion="distance")

plt.subplot(111)
hierarchy.dendrogram(linkage, color_threshold=0.3)
plt.show()
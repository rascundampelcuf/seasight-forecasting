# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 09:34:47 2020

@author: gizqu
"""

# Import libraries
import simplekml
from lxml import etree
import xml.etree.ElementTree as ET
import pandas as pd
from pykml.factory import KML_ElementMaker as KML

#%%

def GetCoordinates(tree):
    root = tree.getroot()
    coords = root.findall('.//{http://www.opengis.net/kml/2.2}coordinates')[0].text
    coords = coords.strip()
    coords = str.splitlines(coords)
    coords = [tuple(x.strip().split(',')) for x in coords]
    return coords

def GenerateKML(tree):
    coords = GetCoordinates(tree)
    
    kml = simplekml.Kml()
    pol = kml.newpolygon()
    pol.outerboundaryis.coords = coords
    pol.style.linestyle.color = simplekml.Color.green
    pol.style.linestyle.width = 5
    pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.green)
    print(pol)
    kml.save("Polygon.kml")
    

kml_file = '../data/KMLs/NorthAtlanticOcean.kml'
tree = ET.parse(kml_file)
GenerateKML(tree)

#%%

data_path = '../data/dummy_data.csv'
data = pd.read_csv(data_path)

#%%
data2 = data[:25]

fich_kml = KML.kml(
    KML.Document(
        KML.Folder(
            KML.name('Temperatures'),
            id='lugares'
            )
        )
    )

for _, row in data2.iterrows():
    fich_kml.Document.Folder.append(
        KML.Placemark(
            KML.Style(
                
                ),
            KML.Point(
                KML.coordinates("{0},{1},0".format(row.LON,row.LAT))
                )           
            )
        )

f = open("test.kml", "w")
out = etree.tostring(fich_kml, pretty_print=True).decode("utf-8")
f.write(out)
f.close()
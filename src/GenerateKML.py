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
import matplotlib

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

def GenerateSquareCoordsFromCenter(lon, lat, width):
    point_a = '\n{},{},0\n'.format(lon - width/2, lat + width/2)
    point_b = '{},{},0\n'.format(lon + width/2, lat + width/2)
    point_c = '{},{},0\n'.format(lon + width/2, lat - width/2)
    point_d = '{},{},0\n'.format(lon - width/2, lat - width/2)
    return ' '.join([point_a, point_b, point_c, point_d])

def GetColorFromTemperature(temp):
    cmap = matplotlib.cm.get_cmap('Spectral')
    rgb = cmap(temp)[:3]
    print(rgb)
    return matplotlib.colors.rgb2hex(rgb)[1:]

data2 = data[:25]

fich_kml = KML.kml(
    KML.Document(        
        KML.Folder(
            KML.name('Temperature regions'),
            id='lugares'
            )
        )
    )

for _, row in data2.iterrows():
    fich_kml.Document.Folder.append(
        KML.Placemark(
            KML.name('{}, {}'.format(row.LON, row.LAT)),
            KML.Style(
                # KML.PolyStyle(KML.color('{}'.format(GetColorFromTemperature(row.SST))))
                KML.LineStyle(KML.color('ff008000'), KML.width('5')),
                KML.PolyStyle(KML.color('64008000'))
            ),
            KML.Polygon(
                KML.outerBoundaryIs(
                    KML.LinearRing(
                        KML.coordinates(GenerateSquareCoordsFromCenter(row.LON, row.LAT, 0.5))
                        )
                    )
                )
            )
        )

f = open("test.kml", "w")
out = etree.tostring(fich_kml, pretty_print=True).decode("utf-8")
f.write(out)
f.close()
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 09:34:47 2020

@author: gizqu
"""

# Import libraries
import simplekml
import xml.etree.ElementTree as ET

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
    

kml_file = '../KMLs/NorthAtlanticOcean.kml'
tree = ET.parse(kml_file)
GenerateKML(tree)

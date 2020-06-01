# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 09:34:47 2020

@author: gizqu
"""

# Import libraries
from simplekml import Kml
import xml.etree.ElementTree as ET

def GetCoordinates(tree):
    root = tree.getroot()
    coords = root.findall('.//{http://www.opengis.net/kml/2.2}coordinates')[0].text
    coords = coords.strip()
    coords = str.splitlines(coords)
    coords = [x.strip() for x in coords]
    return coords

def GenerateKML(tree):
    coords = GetCoordinates(tree)
    

kml_file = '../KMLs/NorthAtlanticOcean.kml'
tree = ET.parse(kml_file)
GenerateKML(tree)

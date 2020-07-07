# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 09:34:47 2020

@author: gizqu
"""

# Import libraries
from lxml import etree
from pykml.factory import KML_ElementMaker as KML

def GetCoords(region):
    string = ''
    for p in region:
        string += '{},{},0\n'.format(p[0], p[1])
    return string

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
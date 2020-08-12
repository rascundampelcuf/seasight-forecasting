# -*- coding: utf-8 -*-

# Import libraries
import itertools
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from seasight_forecasting import global_vars

def GetCoords(region):
    string = ''
    for p in region:
        string += '{},{},20000\n'.format(p[0], p[1])
    return string

def CreateColorbarKML():
    kml = KML.kml(
        KML.Document(
            KML.Folder(
                KML.ScreenOverlay(
                    KML.name('Colorbar'),
                    KML.Icon(KML.href('http://{}:8000/static/img/colorbar.png'.format(global_vars.server_IP))),
                    KML.overlayXY(x="0", y="0", xunits="fraction", yunits="fraction"),
                    KML.screenXY(x="0.02", y="0.02", xunits="fraction", yunits="fraction"),
                    KML.rotationXY(x="0", y="0", xunits="fraction", yunits="fraction"),
                    KML.size(x="0", y="0", xunits="fraction", yunits="fraction")
                )
            )
        )
    )
    f = open(global_vars.kml_destination_path + 'slave_{}.kml'.format(global_vars.screen_for_colorbar), "w")
    out = etree.tostring(kml, pretty_print=True).decode("utf-8")
    f.write(out)
    f.close()

def CreateLogosKML():
    kml = KML.kml(
        KML.Document(
            KML.Folder(
                KML.ScreenOverlay(
                    KML.name('Logos'),
                    KML.Icon(KML.href('http://{}:8000/static/logos/Logos.png'.format(global_vars.server_IP))),
                    KML.overlayXY(x="0", y="1", xunits="fraction", yunits="fraction"),
                    KML.screenXY(x="0.02", y="0.9", xunits="fraction", yunits="fraction"),
                    KML.rotationXY(x="0", y="0", xunits="fraction", yunits="fraction"),
                    KML.size(x="0.5", y="0.5", xunits="fraction", yunits="fraction")
                )
            )
        )
    )
    f = open(global_vars.kml_destination_path + 'slave_{}.kml'.format(global_vars.screen_for_logos), "w")
    out = etree.tostring(kml, pretty_print=True).decode("utf-8")
    f.write(out)
    f.close()

def CreateRegionsKML(regions, withDate):
    kml = KML.kml(
        KML.Document(
            KML.Folder(
                KML.name('Temperature regions'))
            )
        )
    
    if withDate:
        regions = list(itertools.chain.from_iterable(regions))
    for region in regions:
        date_from = ''
        date_to = ''
        if withDate:
            dates = region.pop()
            date_from = dates[0]
            date_to = dates[1]
        color = region.pop()

        kml.Document.Folder.append(
            KML.Placemark(
                KML.TimeSpan(
                    KML.begin(date_from),
                    KML.end(date_to)
                ),
                KML.Style(
                KML.PolyStyle(
                    KML.color(color),
                    KML.outline(0)
                    )
                ),
                KML.Polygon(
                    KML.altitudeMode('absolute'),
                    KML.outerBoundaryIs(
                        KML.LinearRing(
                            KML.coordinates(GetCoords(region))
                            )
                        )
                    )
                )
            )
    
    f = open(global_vars.kml_destination_path + global_vars.kml_destination_filename, "w")
    out = etree.tostring(kml, pretty_print=True).decode("utf-8")
    f.write(out)
    f.close()

def CreateKML(regions, withDate):
    CreateRegionsKML(regions, withDate)
    CreateColorbarKML()
    CreateLogosKML()
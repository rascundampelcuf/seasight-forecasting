# -*- coding: utf-8 -*-

# Import libraries
import itertools
from lxml import etree
from pykml.factory import KML_ElementMaker as KML

def GetCoords(region):
    string = ''
    for p in region:
        string += '{},{},20000\n'.format(p[0], p[1])
    return string

def CreateKML(regions, path, withDate):
    fich_kml = KML.kml(
        KML.Document(
            KML.Folder(
                KML.name('Temperature regions'))
            )
        )
    
    fich_kml.Document.Folder.append(
        KML.ScreenOverlay(
            KML.name('Colorbar'),
            KML.Icon(KML.href('http://localhost:8000/static/seasight_forecasting/img/colorbar.png')),
            KML.overlayXY(x="0", y="0", xunits="fraction", yunits="fraction"),
            KML.screenXY(x="0.02", y="0.02", xunits="fraction", yunits="fraction"),
            KML.rotationXY(x="0", y="0", xunits="fraction", yunits="fraction"),
            KML.size(x="0", y="0", xunits="pixels", yunits="pixels")
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

        fich_kml.Document.Folder.append(
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
    
    f = open(path, "w")
    out = etree.tostring(fich_kml, pretty_print=True).decode("utf-8")
    f.write(out)
    f.close()
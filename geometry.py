from qgis.core import *


def buildPolygon(segements):
    origins, ends = [], []

    for segement in segements:
        origins.append(segement[0])
        ends.append(segement[-1])

    points = ends[ : ] + origins[-1: :-1]
    poly = QgsGeometry.fromPolygon([points])

    return poly

def is_inside(polygon, point):
    return polygon.contains(point)

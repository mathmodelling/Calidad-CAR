from qgis.core import *
from math import sqrt

def getSegments(layer):
    segments = []

    for f_seccion in layer.getFeatures():
        segments.append(f_seccion.geometry().asPolyline())

    return segments

def distance(a, b):
    return sqrt(a.sqrDist(b))

def buildConvexPolygon(segments):

    origins = [points[0] for points in segments[1 : -1]]
    ends = [points[-1] for points in segments[1: -1]]
    borders = segments[0] + segments[-1]

    points = borders + origins + ends

    return QgsGeometry.fromMultiPoint(points).convexHull()

def intersectionPoints(layerA, layerB):
    points = []
    for featA in layerA.getFeatures():
        for featB in layerB.getFeatures():
            inter = intersection(featA.geometry(), featB.geometry())
            if inter is not None:
                points.append(inter)

    qgsPoints = [QgsPoint(point) for point in points]
    return qgsPoints

def intersectionLayerGeometry(layer, geometry):
    intersections = []
    for feature in layer.getFeatures():

        temp = intersection(feature.geometry(), geometry)
        if temp is not None:
            intersections.append(temp)

    # print intersections
    return intersections[0]

def intersection(A, B):
    if A.intersects(B):
        inter = A.intersection(B)
        if inter.wkbType() == QGis.WKBPoint:
            return inter.asPoint()
    return None

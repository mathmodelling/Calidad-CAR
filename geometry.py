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

    print intersections
    return intersections[0]

def intersection(A, B):
    if A.intersects(B):
        inter = A.intersection(B)
        if inter.wkbType() == QGis.WKBPoint:
            return inter.asPoint()
    return None

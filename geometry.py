from qgis.core import *
from math import sqrt

def getSegments(layer):
    """Get the segments of a layer

    :param layer
    :type layer: QgsVectorLayer

    :returns: The list of segements
    :rtype: Polyline List
    """
    segments = []

    for f_seccion in layer.getFeatures():
        segments.append(f_seccion.geometry().asPolyline())

    return segments

def distance(a, b):
    """Compute the distance between ponint a and point b
    :param a: Point a
    :type a: QgsPoint

    :param b: Point b
    :type b: QgsPoint

    :returns: The distance between point a and b
    :rtype: Double
    """
    return sqrt(a.sqrDist(b))

def buildConvexPolygon(segments):
    """Builds a convex polygon from a set of segements
       taking all the points of the bounding segements,
       an just the begin and end points of the inside
       segments

    :param segements:
    :type segements: List of Polylines

    :returns: A convex polygon containing all the points
              described above.
    :rtype: QgsGeometry
    """
    origins = [points[0] for points in segments[1 : -1]]
    ends = [points[-1] for points in segments[1: -1]]
    borders = segments[0] + segments[-1]

    points = borders + origins + ends

    return QgsGeometry.fromMultiPoint(points).convexHull()

def intersectionPoints(layerA, layerB):
    """Get the intersection points between two layers

    :param layerA
    :type layerA: QgsVectorLayer

    :param layerB
    :type layerB: QgsVectorLayer

    :returns: A list of the intersection points
    :rtype: QgsPoint List
    """
    points = []
    for featA in layerA.getFeatures():
        for featB in layerB.getFeatures():
            inter = intersection(featA.geometry(), featB.geometry())
            if inter is not None:
                points.append(inter)

    qgsPoints = [QgsPoint(point) for point in points]
    return qgsPoints

def intersectionLayerGeometry(layer, geometry):
    """Get the first intersection point between a layer and a
       geometry.

    :param layer
    :type layer: QgsVectorLayer

    :param geometry
    :type geometry: QgsGeometry

    :returns: A point if there is an intersection between the layer
              and the geometry, return None otherwise.
    :rtype: QgsPointXY
    """
    intersections = []
    for feature in layer.getFeatures():

        temp = intersection(feature.geometry(), geometry)
        if temp is not None:
            intersections.append(temp)

    if len(intersections) > 0:
        return intersections[0]
    return None

def intersection(A, B):
    """Get the intersection point between two geometries

    :param A: Geometry A
    :type A: QgsGeometry

    :param B: Geometry B
    :type B: QgsGeometry

    :returns: If there is an intersection between the geometries
              returns a point
    :rtype: QgsPointXY
    """
    if A.intersects(B):
        inter = A.intersection(B)
        if inter.wkbType() == QGis.WKBPoint:
            return inter.asPoint()
    return None

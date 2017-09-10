# -*- coding: utf-8 -*-

"""Este módulo contiene utilidades geometricas, que se utilizan en la
clase CalidadCAR."""
from qgis.core import *
from math import sqrt

def getSegments(layer):
    """Retorna los segmentos de layer.

    :param layer: Capa de la cual se van a obtener los segementos
    :type layer: QgsVectorLayer

    :returns: La lista de segmentos
    :rtype: Lista de Polylines
    """
    segments = []

    for f_seccion in layer.getFeatures():
        segments.append(f_seccion.geometry().asPolyline())

    return segments

def distance(a, b):
    """Cálcula la distancia entre un punto a, y un punto b.

    :param a: Punto a
    :type a: QgsPoint

    :param b: Punto b
    :type b: QgsPoint

    :returns: Distancia entre a y b.
    :rtype: Double
    """
    return sqrt(a.sqrDist(b))

def buildConvexPolygon(segments):
    """Construye un polígono convexo a partir de un conjungo de segementos,
       tomando todos los puntos de los segmentos que estan al extremo inicial, y final,
       y solo el punto de inicio y el punto final de los segementos intermedios.

    :param segements:
    :type segements: Lista de Polylines

    :returns: Un polígono convexo que envuelve todos los puntos que se acabarón de
              describir.
    :rtype: QgsGeometry
    """
    origins = [points[0] for points in segments[1 : -1]]
    ends = [points[-1] for points in segments[1: -1]]
    borders = segments[0] + segments[-1]

    points = borders + origins + ends

    return QgsGeometry.fromMultiPoint(points).convexHull()

def intersectionPoints(layerA, layerB):
    """Obtiene los puntos de intersección entre dos capas.

    :param layerA: Capa que se va a intersectar con layerB.
    :type layerA: QgsVectorLayer

    :param layerB: Capa que se va a intersectar con layerA.
    :type layerB: QgsVectorLayer

    :returns: La lista de los puntos de intersección
    :rtype: Lista de QgsPoints
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
    """Obtiene la primera inresección entre una capa y una geometría.

    :param layer: Capa
    :type layer: QgsVectorLayer

    :param geometry: Geometría
    :type geometry: QgsGeometry

    :returns: El punto de insersección, en caso de que exita, returna None de otra forma.
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
    """Optiene el punto de insersección entre dos geometrías.

    :param A: Geometría A fsdfsdf
    :type A: QgsGeometry fsdfsd

    :param B: Geometría B
    :type B: QgsGeometry

    :returns: El punto de insersección, en caso de que exita, returna None de otra forma.
    :rtype: QgsPointXY
    """
    if A.intersects(B):
        inter = A.intersection(B)
        if inter.wkbType() == QGis.WKBPoint:
            return inter.asPoint()
    return None

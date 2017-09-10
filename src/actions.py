# -*- coding: utf-8 -*-

import geometry
import layer_manager as manager
from PyQt4.QtCore import (QFileInfo, QVariant)
from abc import ABCMeta, abstractmethod
from qgis.core import ( QgsField,
                        QgsVectorJoinInfo,
                        QgsVectorLayer)

class BaseAction:
    __metaclass__ = ABCMeta
    @abstractmethod
    def pre(self):
        pass
    @abstractmethod
    def pro(self):
        pass
    @abstractmethod
    def pos(self):
        pass

class LayerAction(BaseAction):
    def __init__(self):
        self.layers = []

    def pre(self):
        # Delete all layeres
        eje = manager.get_layer('ejes')
        fondo = manager.get_layer('fondo')
        hidro = manager.get_layer('hidrografia')
        secciones = manager.get_layer('secciones')
        manager.remove_layers([eje, fondo, hidro, secciones])

    def pro(self, layers):
        # Load layers and populate self.layers
        for layer in layers:
            path, name = layer
            layerInfo = QFileInfo(path)

            if layerInfo.suffix() == 'tif':
                layer = manager.load_raster_layer(path, name)
                if layer is not None:
                    self.layers.append(layer)

            elif layerInfo.suffix() == 'shp':
                if name == 'secciones' or name == 'ejes':
                    layer = manager.load_vector_layer(path, name)
                else:
                    layer = manager.load_vector_layer(path, name, (57, 165, 232))

                if layer is not None:
                    self.layers.append(layer)

    def pos(self):
        #Add the layers to the map registry
        manager.add_layers(self.layers)

class CSVAction(BaseAction):

    def __init__(self):
        self.shp = None
        self.sheet = None

    def pre(self):
        self.shp = manager.get_layer('secciones')
        return self.shp

    def pro(self):
        return [field.name() for field in self.shp.pendingFields()]

    def pos(self, layer, csv_cols, csv_field, shp_cols, shp_field):
        sheet = layer
        manager.add_layers([sheet])

        #Columnas del archivo CSV
        columns = csv_cols
        #Columnas del archivo shp
        field_names = shp_cols

        # print field_names
        # print 10 * '*'
        # print columns
        # print 10 * '*'

        #Filtra las columnas existentes, para evitar información duplicada
        columns = [col for col in columns if 'csv_' + col not in field_names]
        # print columns
        if columns == []:
            #No hay columnas nuevas para unir
            return

        joinObject = QgsVectorJoinInfo()
        joinObject.joinLayerId = sheet.id()
        joinObject.joinFieldName = csv_field
        joinObject.targetFieldName = shp_field

        joinObject.setJoinFieldNamesSubset(columns)
        joinObject.memoryCache = True
        self.shp.addJoin(joinObject)

class AddSectionAction(BaseAction):
    def __init__(self):
        self.seccionesLayer = None
        self.tempLayer = None

    def pre(self):
        #Check wheter or not there is a secciones layer
        self.seccionesLayer = manager.get_layer('secciones')
        return self.seccionesLayer is not None

    def pro(self):
        self.tempLayer = manager.get_layer('temp')
        if self.tempLayer is None:
            crs = self.seccionesLayer.crs().authid()

            self.tempLayer = QgsVectorLayer('LineString?crs='+crs, 'temp', 'memory')

            pr = self.tempLayer.dataProvider()
            fields = self.seccionesLayer.pendingFields()
            pr.addAttributes(fields)

            manager.add_layers([self.tempLayer])

    def pos(self, iface, csvAction):
        csvAction.setEnabled(False)
        iface.setActiveLayer(self.tempLayer)
        self.tempLayer.startEditing()

class ConcentrationPointsAction(BaseAction):
    def __init__(self):
        self.eje = None
        self.secciones = None
        self.work_layer = None

    def pre(self):
        #Verifica que las capas necesarias para realizar el proceso estan cargadas
        self.secciones = manager.get_layer('secciones')
        self.eje = manager.get_layer('ejes')

        return self.secciones is not None and self.eje is not None

    def pro(self):
        #Crea la capa de salida, con las nuevas secciones (en caso de que existan)
        self.work_layer = self.addFeature(self.secciones)

        temp = manager.get_layer('temp')
        if temp is not None:
            """En caso de que existan secciones temporales, se combinaran con la
               capa de secciones, para crear la capa work_layer"""
            for new_feature in temp.getFeatures():
                segements = geometry.getSegments(self.work_layer)
                point = geometry.intersectionLayerGeometry(self.eje, new_feature.geometry())
                if point is None: continue
                idx = self.place(segements, point)
                # print 'IDX: ', idx
                self.work_layer = self.addFeature(self.work_layer, new_feature, idx)

    def pos(self, iface):
        #Agrega la capa de salida, y abre la tabla de atributos
        output = manager.get_layer('output')
        if output is not None:
            manager.remove_layers([output])

        #Mostrar la capa de trabajo work_layer
        manager.add_layers([self.work_layer])

        self.work_layer.dataProvider().addAttributes([QgsField(u'concentracion', QVariant.Double)])
        self.work_layer.startEditing()
        iface.showAttributeTable(self.work_layer)


    def addFeature(self, layerA, feature = None, idx = -1):
        """Inserta una característica (feature) en una capa en un orden establecido

        :param layerA: Capa en la que se va a insertar la característica (feature)
        :type layerA: QgsVectorLayer

        :param feature: Característica (feature) que se va a insertar en la capa.
        :type feature: QgsFeature

        :param idx: Indice de la nueva característica (feature) que se va a insertar.
        :type idx: Integer

        :returns: Una nueva capa con la característica insertada en el pocisión idx.
        :rtype: QgsVectorLayer
        """
        crs = layerA.crs().authid()
        tempLayer = QgsVectorLayer('LineString?crs='+crs, 'output', 'memory')
        pr = tempLayer.dataProvider()
        fields = layerA.pendingFields()

        for f in fields:
            pr.addAttributes([f])

        features = list(layerA.getFeatures())
        if idx != -1:
            features.insert(idx + 1, feature)

        tempLayer.updateFields()

        for feature in features:
            pr.addFeatures([feature])

        tempLayer.updateExtents()
        return tempLayer

    def place(self, segments, p):
        """Ubica un punto entre los dos segmentos consecutivos a los que pertenece.

        :param segments: Lista de segmentos
        :type segments: Lista de QgsSegments

        :param p: punto que se va a ubicar en la lista de segmentos
        :type point: QgsPoint

        """
        low, hi = 0, len(segments)
        mid, cont = 0, 0

        while(low <= hi):
            mid =  low + ((hi - low) / 2)
            if self.check(segments[low : mid + 1], p):
                hi = mid
            else:
                low = mid
            cont += 1
            #Sacurity trigger
            if cont == 20: break

        return low

    # def place(self, segments, p):
    #     for i in xrange(len(segments) - 1):
    #         if self.check([segments[i], segments[i + 1]], p):
    #             return i
    #     return None

    def check(self, segments, point):
        """Verifica si un punto se encuentra entre dos segmentos

        :param segments: Lista de segmentos entre los que se puede encontrar el punto.
        :type segments: Lista de QgsSegments

        :param point: punto sobre el cual se va a hacer la verificación
        :type point: QgsPoint

        :returns: Un booleano que indica si la condición se cumple o no.
        :rtype: Boolean
        """
        if len(segments) == 1 : return False
        polygon = geometry.buildConvexPolygon(segments)
        # layer =  QgsVectorLayer('Polygon?crs=epsg:3116', 'poly' , "memory")
        # pr = layer.dataProvider()
        # poly = QgsFeature()
        # poly.setGeometry(polygon)
        # pr.addFeatures([poly])
        # layer.updateExtents()
        # QgsMapLayerRegistry.instance().addMapLayers([layer])
        return polygon.contains(point)

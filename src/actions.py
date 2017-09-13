# -*- coding: utf-8 -*-

import copy
import time
import geometry
import numpy as np
import datetime as dtm
import layer_manager as manager
from modelling import calidad_car
from abc import ABCMeta, abstractmethod
from PyQt4.QtCore import (QFileInfo, QVariant)

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
        # self.work_layer.dataProvider().addAttributes([QgsField(u'concentracion', QVariant.Double)])
        # self.work_layer.startEditing()
        # iface.showAttributeTable(self.work_layer)


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

class ModellingAction(BaseAction):
    def __init__(self):
        self.eje = None
        self.work_layer = None

    def pre(self):
        #Verifica que las capas necesarias estan cargagas
        self.eje = manager.get_layer('ejes')
        self.work_layer = manager.get_layer('output')

        return self.eje is not None and self.work_layer is not None

    def pro(self):
        #Inicializa variables y retorna los nombres de las colmunmas de la tabla
        #de atributos de la capa de trabajo output

        self.concentration_values = []
        self.vel_values = []

        self.field_names = [field.name() for field in self.work_layer.pendingFields()]

        return self.field_names

    def pos(self, vel_name, conc_name):
        np.set_printoptions(precision=2)
        concen_idx = self.work_layer.fieldNameIndex(conc_name)
        vel_idx = self.work_layer.fieldNameIndex(vel_name)

        for feature in self.work_layer.getFeatures():
            #Esto podría lanzar una exepción
            #Precisión de 4 digitos, para evitar problemas con matplotlib
            cnt = format(feature.attributes()[concen_idx], '.4f')
            velo = format(feature.attributes()[vel_idx], '.4f')
            self.concentration_values.append(float(cnt))
            self.vel_values.append(float(velo))

        points = geometry.intersectionPoints(self.eje, self.work_layer)
        distances = []
        for i in xrange(len(points)):
            #Precisión de 4 digitos, para evitar problemas con matplotlib
            dist = geometry.distance(points[0], points[i])
            distances.append(float(format(dist, '.4f')))

        dx = np.array(distances)
        cn = np.array(self.concentration_values)

        c_i = np.array([dx, cn]).T
        va = np.array(self.vel_values)
        cd = np.array([1.5 for x in self.vel_values])

        c_i_copy = copy.deepcopy(c_i)
        va_copy = copy.deepcopy(va)
        cd_copy = copy.deepcopy(cd)

        self.apply_modelling(c_i_copy, va_copy, cd_copy, 1)

    def apply_modelling(self, c_i, va, cd, flag):
        # Numero de pasos en el teimpo a ejecutar
        nt = 20
        # Número de nodos espaciales
        nx = 10

        c_f = np.arange(0.0, nt + 1.0)
        amplitud, fase, frecuencia, z = 1.0, 0.0, 0.35, 1.0
        c_f = amplitud * np.sin(frecuencia * c_f + fase) + z

        mcon = np.empty((nt + 1, np.size(c_i, axis=0)))
        mcon[0, :] = c_i[:, 1]
        for i in range(1, nt):
            # Asignación de condición de frontera. Se hace cambiando primer valor de c_i
            c_i[0, 1] = c_f[i]
            # Evolución de la concentración para t + dt
            con, t_step = calidad_car.calidad_explicito(c_i, va, cd)
            # Se guardan las concentraciones del momento t+dt
            mcon[i, :] = con
            # Actualizar condición inicial
            c_i[:, 1] = con
        # return mcon, t_step

        paso_x = 10

        print calidad_car.grafica(mcon, t_step, paso_x, srow=11, scol=80, flag=flag)

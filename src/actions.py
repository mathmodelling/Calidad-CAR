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
    """Clase base que define la estructura de una acción."""
    __metaclass__ = ABCMeta
    @abstractmethod
    def pre(self):
        """En este método puede definir y verificar condiciones iniciales necesarias para que se pueda realizar una acción."""
        pass
    @abstractmethod
    def pro(self):
        """En este método se puede implementar la funcionalidad esencial de la acción."""
        pass
    @abstractmethod
    def pos(self):
        """En este método se pueden implementar procesos que se deben realizar una vez se ha concluido con éxito el llamado al método pos."""
        pass

class LayerAction(BaseAction):
    """Esta clase representa la acción encargada de cargar las capas necesarias."""
    def __init__(self):
        self.layers = []

    def pre(self):
        """Este método se encarga de eliminar todas las capas cargagas previamente en el registro de QGIS (QgsMapLayerRegistry)."""
        # Delete all layeres
        eje = manager.get_layer('ejes')
        fondo = manager.get_layer('fondo')
        hidro = manager.get_layer('hidrografia')
        secciones = manager.get_layer('secciones')
        manager.remove_layers([eje, fondo, hidro, secciones])

    def pro(self, layers):
        """Este método se encarga de cargar todas las capas en layers, y de llenar self.layers

        :param layers: Lista de las rutas de todas las capas que se van a cargar.
        :type layers: Lista str
        """
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
        """Este método se encarga de agregar todas las capas cargadas en el registro de QGIS (QgsMapLayerRegistry). """
        manager.add_layers(self.layers)

class CSVAction(BaseAction):
    """Esta acción se encarga de cargar un archivo CSV, y de unirlo con la tabla de atributos de la capa de secciones."""
    def __init__(self):
        self.shp = None
        self.sheet = None

    def pre(self):
        """Este método se encarga de obtener la capa de secciones del administrador de las capas cargadas (manager) y lo retorna.

        :returns: La capa de secciones en caso de que la encuentre, retorna Nonde de otra forma.
        :rtype: QgsVectorLayer"""

        self.shp = manager.get_layer('secciones')
        return self.shp

    def pro(self):
        """Este método se encarga de guardar en una lista todos los nombres de las columnas de la tabla de atributos de self.shp y la retorna.

        :returns: Lista con todos los nombres de las columnas de la tabla de atributos de self.shp
        :rtype: Lista str
        """
        return [field.name() for field in self.shp.pendingFields()]

    def pos(self, layer, csv_cols, csv_field, shp_cols, shp_field):
        """Este método se encarga de realizar la unión entre el archivo CSV que se cargo, y la tabla de atributos de self.shp.

        :param layer: Capa del archivo CSV.
        :type layer: QgsVectorLayer

        :param csv_cols: Lista con las columnas de la capa CSV que se van a unir.
        :type csv_cols: Lista str

        :param csv_field: Campo de la capa CSV que se va a usar como columna de unión.
        :type csv_field: str

        :param shp_cols: Lista de columnas de la tabla de atributos de self.shp que se van a unir.
        :type shp_cols: Lista str

        :param shp_field: Campo de la capa self.shp que se va a usar como columna de unión.
        :type shp_field: str
        """
        sheet = layer
        manager.add_layers([sheet])

        #Columnas del archivo CSV
        columns = csv_cols
        #Columnas del archivo shp
        field_names = shp_cols

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
    """Esta acción se encarga de implementar la funcionalidad para agregar secciones."""
    def __init__(self):
        self.seccionesLayer = None
        self.tempLayer = None

    def pre(self):
        """Verifica si existe la capa de secciones.

        :returns: Un booleano que indica si ya esta cargada la capa de secciones:
        :rtype: bool
        """
        self.seccionesLayer = manager.get_layer('secciones')
        return self.seccionesLayer is not None

    def pro(self):
        """Crea una capa temporal para almacenar las secciones, en caso de que no exista."""
        self.tempLayer = manager.get_layer('temp')
        if self.tempLayer is None:
            crs = self.seccionesLayer.crs().authid()

            self.tempLayer = QgsVectorLayer('LineString?crs='+crs, 'temp', 'memory')

            pr = self.tempLayer.dataProvider()
            fields = self.seccionesLayer.pendingFields()
            pr.addAttributes(fields)

            manager.add_layers([self.tempLayer])

    def pos(self, iface, csvAction):
        """Deshabilita la acción de realizar unión entre la tabla de atributos de la capa de secciones y un archivo CSV, selecciona la capa temporal para agregar secciones, y la pone en modo de edición."""
        csvAction.setEnabled(False)
        iface.setActiveLayer(self.tempLayer)
        self.tempLayer.startEditing()

class ConcentrationPointsAction(BaseAction):
    """Esta ación se encarga de fusionar la capa de secciones temporales (temp) con la capa de secciones."""
    def __init__(self):
        self.eje = None
        self.secciones = None
        self.work_layer = None

    def pre(self):
        """Verifica que las capas necesarias para realizar esta acción estan cargadas.

        :returns: Un booleano que indica si se cumple o no la condición.
        :rtype: bool
        """
        self.secciones = manager.get_layer('secciones')
        self.eje = manager.get_layer('ejes')

        return self.secciones is not None and self.eje is not None

    def pro(self):
        """Crea una capa de salida con las secciones de la capa de secciones, y las secciones agregadas por el usuario."""
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
        """Agrega la capa de salida (output) al gestor de capas de QGIS."""

        #Elimina la capa output en caso de de que exista
        output = manager.get_layer('output')
        if output is not None:
            manager.remove_layers([output])

        #Mostrar la capa de trabajo work_layer
        manager.add_layers([self.work_layer])

        #self.work_layer.dataProvider().addAttributes([QgsField(u'concentracion', QVariant.Double)])
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
    """Esta acción se encarga de aplicar el modelo matemático sobre la información cargada por el usuario."""
    def __init__(self):
        self.eje = None
        self.work_layer = None

    def pre(self):
        """Verifica que las capas necesarias para realizar esta acción estan cargadas.

        :returns: Un booleano que indica si se cumple o no la condición.
        :rtype: bool
        """
        self.eje = manager.get_layer('ejes')
        self.work_layer = manager.get_layer('output')

        return self.eje is not None and self.work_layer is not None

    def pro(self):
        """Inicializa variables necesarias para trabajar, y retorna los nombres de las columnas de la tabla de atributos de la capa de trabajo output.

        :returns: Lista de columnas de la capa de trabajo output.
        :rtype: Lista str
        """
        self.concentration_values = []
        self.vel_values = []

        self.field_names = [field.name() for field in self.work_layer.pendingFields()]

        return self.field_names

    def pos(self, vel_name, conc_name, flag = 0):
        """Aplica el modelo matemático sobre la información.

        :param vel_name: Nombre de la columna en la que se encuetra la información de la velocidad.
        :type vel_name: str

        :param conc_name: Nombre de la columna en la que se encuetra la información de los puntos de concentracion.
        :type conc_name: str

        :param flag: Bandera que indica que gráfica se va a desplegar.
        :type falg: bool
        """
        np.set_printoptions(precision=2)
        concen_idx = self.work_layer.fieldNameIndex(conc_name)
        vel_idx = self.work_layer.fieldNameIndex(vel_name)

        for feature in self.work_layer.getFeatures():
            #Esto podría lanzar una exepción
            cnt = feature.attributes()[concen_idx].replace(',', '.')
            velo = feature.attributes()[vel_idx].replace(',', '.')

            #Precisión de 4 digitos, para evitar problemas con matplotlib
            cnt = format(float(cnt), '.4f')
            velo = format(float(velo), '.4f')


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

        self.apply_modelling(c_i_copy, va_copy, cd_copy, flag)

    def apply_modelling(self, c_i, va, cd, flag):
        """Método auxilar que abstrae la forma en la que se aplica el modelo matemático."""
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

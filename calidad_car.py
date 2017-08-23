# -*- coding: utf-8 -*-
"""

"""
from qgis.core import (QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem,
QgsMapLayerRegistry, QgsCoordinateReferenceSystem, QgsVectorJoinInfo,
QGis, QgsPoint, QgsFeature, QgsGeometry, QgsField)

from qgis.gui import QgsMapToolEmitPoint
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo,QVariant
from PyQt4.QtGui import QAction, QIcon, QColor, QMessageBox


import resources
from calidad_car_dialog import Ui_Dialog as CalidadCARDialog
from dialogo_csv import CSVDialog
from dialogo_concentracion import DialogoConcentracion
import os.path
import pandas

from random import randint

import geometry
from src import layer_manager as manager

class CalidadCAR:
    """Implementación del plugin."""

    def __init__(self, iface):
        """Constructor.

        :param iface: Una instancia de la interfaz que será pasada a esta clase,
            la cual proveé una ligadura con la cual se podrá manipular la aplicación
            de QGIS en tiempo de ejecución.
        :type iface: QgsInterface
        """
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CalidadCAR_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Calidad CAR')
        self.toolbar = self.iface.addToolBar(u'CalidadCAR')
        self.toolbar.setObjectName(u'CalidadCAR')

        self.layers = []
        self.dlg = CalidadCARDialog()
        # self.csvDialog = CSVDialog()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CalidadCAR', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Agrega una acción la la barra de herramientas, y al menú del plugin.

        :param icon_path: Ruta del icono. Puede ser la ruta de un recurso recurso
            (ejemplo: ':/plugins/foo/bar.png') o una ruta normal del sistema de archivos
        :type icon_path: str

        :param text: Texto que será mostrado en el menu de opciones de plugin para esta accion.
        :type text: str

        :param callback: Función que será llamada cuando se hace click sobre la acción.
        :type callback: function

        :param enabled_flag: Una bandera que indica si la acción debería ser activada
            por defecto. Por defecto este valor esta en True.
        :type enabled_flag: bool

        :param add_to_menu: Una bandera indicando si la acción debería ser agregada
            al menú de opciones del plugin. Por defecto esta en True
        :type add_to_menu: bool

        :param add_to_toolbar: Una bandera indicando si la acción debería ser agregada
            a la barra de herramientas del plugin. Por defecto esta en True
        :type add_to_toolbar: bool

        :param status_tip: Texto opcional que aparecerá cuando el puntero del mouse
            se pocisione sobre la acción.
        :type status_tip: str

        :param parent: Widget padre de la nueva acción. Por defecto será None
        :type parent: QWidget

        :param whats_this: Texto opcional para mostrar en la barra de estatus,
            cuando el puntero del mouse se pocisione sobre la acción.

        :returns: La acción que fue creada. Notar que la acción también es
            agregada a self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Crea las entradas del menu, y las acciones de la barra de herramientas
            dentro de la interfaz de QGIS"""

        icon_path = ':/plugins/CalidadCAR/icons/layers-icon.png'
        self.addLayersAction = self.add_action(
            icon_path,
            text=self.tr(u'Cargar fondos'),
            callback=self.cargarCapas,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icons/csv-join-icon-add.png'
        self.addCsvAction = self.add_action(
            icon_path,
            text=self.tr(u'Unir CSV'),
            callback=self.addCsv,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icons/add-section-icon.png'
        self.addSectionAction = self.add_action(
            icon_path,
            text=self.tr(u'Agregar sección'),
            callback=self.addSection,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icons/start-icon.png'
        self.intersctionAction = self.add_action(
            icon_path,
            text=self.tr(u'Calcular'),
            callback=self.intersection,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icons/refresh-icon.png'
        self.intersctionAction = self.add_action(
            icon_path,
            text=self.tr(u'Limpiar'),
            callback=self.clean,
            parent=self.iface.mainWindow())

        # self.intersctionAction.setEnabled(False)
        # self.addSectionAction.setEnabled(False)
        # self.addCsvAction.setEnabled(False)

    def clean(self):
        """Recarga el plugin, limpiando todas las capas cargadas, excepto, las
           capas de salida de información."""
        for layer in self.layers:
            QgsMapLayerRegistry.instance().removeMapLayer(layer)

        csv_layers = QgsMapLayerRegistry.instance().mapLayersByName("csv")
        for layer in csv_layers:
            QgsMapLayerRegistry.instance().removeMapLayer(layer)

        tempLayer = QgsMapLayerRegistry.instance().mapLayersByName("temp")
        for layer in tempLayer:
            layer.commitChanges()
            QgsMapLayerRegistry.instance().removeMapLayer(layer)

        self.layers = []

    def addSection(self):
        """Utiliza una capa llamada temp, para insertar las nuevas secciones,
           esta operación solo podrá ser realizada si existe la capa de secciones.

           En caso de que no exista la capa temp, se creara una nueva, con el crs
           de la capa de secciones.
        """
        tempLayer = None
        try:
            seccionesLayer = QgsMapLayerRegistry.instance().mapLayersByName("secciones")[0]
        except IndexError:
            self.errorDialog(u'No se encontró la capa de secciones.',
                    u'Asegurate de agregarla con la opción de cargar fondos.')
            return

        try:
            tempLayer = QgsMapLayerRegistry.instance().mapLayersByName("temp")[0]
        except IndexError:
            crs = seccionesLayer.crs().authid()

            tempLayer = QgsVectorLayer('LineString?crs='+crs, 'temp', 'memory')

            pr = tempLayer.dataProvider()
            fields = seccionesLayer.pendingFields()
            pr.addAttributes(fields)

            QgsMapLayerRegistry.instance().addMapLayer(tempLayer)

        self.iface.setActiveLayer(tempLayer)
        tempLayer.startEditing()

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

    def intersection(self):
        """Este método se encarga de recopilar toda la información, para posteriormente
           aplicarle la lógica del plugin.

           Para que el usuario pueda realizar esta operación, necesariamente, tienen
           que estar cargadas la capa de ejes, y la capa de secciones transversales.
        """
        try:
            secciones = QgsMapLayerRegistry.instance().mapLayersByName("secciones")[0]
            eje = QgsMapLayerRegistry.instance().mapLayersByName("ejes")[0]
        except IndexError:
            self.errorDialog(u'No se encontraron algunas de las capas necesarias para realizar esta operación.',
                    u'Asegurate de agregar la capa de secciones, y la capa del eje con la opción Configurar Fondo.')
            return

        work_layer = self.addFeature(secciones)

        try:
            """En caso de que existan secciones temporales, se combinaran con la
               capa de secciones, para crear la capa work_layer"""
            temp = QgsMapLayerRegistry.instance().mapLayersByName("temp")[0]

            for new_feature in temp.getFeatures():
                segements = geometry.getSegments(work_layer)
                point = geometry.intersectionLayerGeometry(eje, new_feature.geometry())
                if point is None: continue
                idx = self.place(segements, point)
                # print 'IDX: ', idx
                work_layer = self.addFeature(work_layer, new_feature, idx)

        except IndexError:
            pass

        #Mostrar la capa de trabajo work_layer
        QgsMapLayerRegistry.instance().addMapLayer(work_layer)

        work_layer.dataProvider().addAttributes([QgsField(u'Concentración', QVariant.Int)])
        work_layer.startEditing()
        self.iface.showAttributeTable(work_layer)

        #Crar un DataFrame de pandas con la tabla de atributos de la capa de trabajo
        table = [row.attributes() for row in work_layer.getFeatures()]
        field_names = [field.name() for field in work_layer.pendingFields() ]
        pd_frame = pandas.DataFrame(table, columns = field_names)
        print pd_frame

        #Crear un DataFrame de pandas con las distancias de la sucesión de secciones
        points = geometry.intersectionPoints(eje, work_layer)

        distances = [0]
        for i in xrange(len(points) - 1):
            distances.append(geometry.distance(points[i], points[i + 1]))
        # print distances

        pd_dataframe = pandas.DataFrame(distances, columns = ['Distancia'])
        print pd_dataframe


    def addCsv(self):
        """Crea una capa a partir de un archivo CSV, y une la información que
           contiene esta, con la tabla de atributos de la capa de secciones,
           la cual tendrá que existir, para que se pueda realizar esta operación.
        """
        try:
            shp = QgsMapLayerRegistry.instance().mapLayersByName("secciones")[0]
        except IndexError:
            self.errorDialog(u'No se encontró la capa de secciones.',
            u'Asegurate de agregarla con la opción de Cargar fondos.')
            return

        sheet = None
        field_names = [field.name() for field in shp.pendingFields() ]
        csvDialog = CSVDialog(field_names)
        result = csvDialog.exec_()
        if result and csvDialog.getLayer():
            # print csvDialog.getSelectedColumns()

            sheet = csvDialog.getLayer()
            QgsMapLayerRegistry.instance().addMapLayer(sheet)

            #Columnas del archivo CSV
            columns = csvDialog.getSelectedColumns()
            #Filtra las columnas existentes, para evitar información duplicada
            field_names = [field.name() for field in shp.pendingFields() ]

            columns = [col for col in columns if 'csv' + col not in field_names]

            if columns == []:
                #No hay columnas nuevas para unir
                return

            shpField = csvDialog.getJoinFieldTarget()
            csvField = csvDialog.getJoinField()
            joinObject = QgsVectorJoinInfo()
            joinObject.joinLayerId = sheet.id()
            joinObject.joinFieldName = csvField
            joinObject.targetFieldName = shpField

            joinObject.setJoinFieldNamesSubset(columns)
            joinObject.memoryCache = True
            shp.addJoin(joinObject)

            # self.addSectionAction.setEnabled(True)
            # self.intersctionAction.setEnabled(True)


    def unload(self):
        """Remueve el menú del plugin, y las acciones de la barra de herramientas
           de la interfaz de QGIS."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Calidad CAR'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def addLayers(self):
        """Carga las capas que el usuario ingreso en el dialog de cargar fondos,
           los fondos se volverán a cargar cada vez que se llame este método, en
           caso de que el usuario quiera recargar un fondo."""

        manager.remove_layers(self.layers)
        self.layers = []

        files = self.dlg.getFilePaths()

        #Cargar los fondos que se encuentrán en el dialogo de cargar fondos.
        for layer in files:
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

        manager.add_layers(self.layers)

    def cargarCapas(self):
        """Run method that performs all the real work"""
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            self.addLayers()
            # self.addCsvAction.setEnabled(True)

    def errorDialog(selg, text, detail):
        """Dialogo de error que se lanzará cuando el usuario intente hacer una
           operación que no esta permitida.

        :param text: Identificador principal del error.
        :type text: str

        :param name: Información detallada del error.
        :type name: str
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(detail)
        msg.setWindowTitle("Error")
        msg.exec_()

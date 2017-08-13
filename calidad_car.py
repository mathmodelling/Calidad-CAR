# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CalidadCAR
                                 A QGIS plugin
 Test
                              -------------------
        begin                : 2017-07-24
        git sha              : $Format:%H$
        copyright            : (C) 2017 by cbdavide
        email                : cbdavide
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo
from PyQt4.QtGui import QAction, QIcon, QColor, QMessageBox
from qgis.core import (QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem,
                       QgsMapLayerRegistry, QgsCoordinateReferenceSystem, QgsVectorJoinInfo,
                       QGis, QgsPoint, QgsFeature, QgsGeometry)

from qgis.gui import QgsMapToolEmitPoint


# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from calidad_car_dialog import Ui_Dialog as CalidadCARDialog
from dialogo_csv import CSVDialog
import os.path
import pandas

from random import randint
import geometry

class CalidadCAR:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
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
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
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
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/CalidadCAR/icons/layers-icon.png'
        self.addLayersAction = self.add_action(
            icon_path,
            text=self.tr(u'Cargar fondo'),
            callback=self.run,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icons/csv-join-icon-add.png'
        self.addCsvAction = self.add_action(
            icon_path,
            text=self.tr(u'Join'),
            callback=self.addCsv,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icons/add-section-icon.png'
        self.addSectionAction = self.add_action(
            icon_path,
            text=self.tr(u'Agregar sección'),
            callback=self.addSection,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icons/icon.png'
        self.intersctionAction = self.add_action(
            icon_path,
            text=self.tr(u'Calcular'),
            callback=self.intersection,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icons/icon.png'
        self.intersctionAction = self.add_action(
            icon_path,
            text=self.tr(u'Limpiar'),
            callback=self.clean,
            parent=self.iface.mainWindow())

        # self.intersctionAction.setEnabled(False)
        # self.addSectionAction.setEnabled(False)
        # self.addCsvAction.setEnabled(False)

    def clean(self):
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
        """Check if point c is between points a and b."""
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
        try:
            secciones = QgsMapLayerRegistry.instance().mapLayersByName("secciones")[0]
            eje = QgsMapLayerRegistry.instance().mapLayersByName("ejes")[0]
        except IndexError:
            self.errorDialog(u'No se encontraron algunas de las capas necesarias para realizar esta operación.',
                    u'Asegurate de agregar la capa de secciones, y la capa del eje con la opción Configurar Fondo.')
            return

        work_layer = self.addFeature(secciones)

        try:
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

        #Paint the work_layer
        QgsMapLayerRegistry.instance().addMapLayer(work_layer)

        #DataFrame with the attribute table
        table = [row.attributes() for row in work_layer.getFeatures()]
        field_names = [field.name() for field in work_layer.pendingFields() ]
        pd_frame = pandas.DataFrame(table, columns = field_names)
        print pd_frame

        #DataFrame of distances
        points = geometry.intersectionPoints(eje, work_layer)

        distances = [0]
        for i in xrange(len(points) - 1):
            distances.append(geometry.distance(points[i], points[i + 1]))
        # print distances

        pd_dataframe = pandas.DataFrame(distances, columns = ['Distancia'])
        print pd_dataframe

    def addCsv(self):
        # """Join operation"""
        try:
            shp = QgsMapLayerRegistry.instance().mapLayersByName("secciones")[0]
        except IndexError:
            self.errorDialog(u'No se encontró la capa de secciones.',
            u'Asegurate de agregarla con la opción de Cargar fondos.')
            return

        sheet = None
        # Run the dialog event loop
        field_names = [field.name() for field in shp.pendingFields() ]
        csvDialog = CSVDialog(field_names)
        result = csvDialog.exec_()
        if result and csvDialog.getLayer():
            # print csvDialog.getSelectedColumns()

            sheet = csvDialog.getLayer()
            QgsMapLayerRegistry.instance().addMapLayer(sheet)
            #Get the shape layer called secciones

            columns = csvDialog.getSelectedColumns()
            field_names = [field.name() for field in shp.pendingFields() ]

            columns = [col for col in columns if 'csv' + col not in field_names]

            if columns == []:
                #There is nothing to join
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
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Calidad CAR'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def addLayers(self):
        #Borrando las capas
        for layer in self.layers:
            QgsMapLayerRegistry.instance().removeMapLayer(layer)

        self.layers = []
        files = self.dlg.getFilePaths()

        for layer in files:
            path, name = layer
            layerInfo = QFileInfo(path)

            if layerInfo.suffix() == 'tif':
                self.addRasterLayer(path, name)
            elif layerInfo.suffix() == 'shp':
                self.addVectorLayer(path, name)

        for layer in self.layers:
            QgsMapLayerRegistry.instance().addMapLayer(layer)

    def addVectorLayer(self, path, name):
        layer = QgsVectorLayer(path, name, 'ogr')
        if not layer.isValid():
            return

        # Cambiar el color del layer
        symbol_layer = layer.rendererV2().symbols()[0].symbolLayer(0)
        if name == 'ejes' or name == 'secciones':
            symbol_layer.setColor(QColor(0, 0, 0))
        else:
            symbol_layer.setColor(QColor(randint(0, 50),randint(0, 255),163))

        self.layers.append(layer)

    def addRasterLayer(self, path, name):
        rlayer = QgsRasterLayer(path, name)
        if not rlayer.isValid(): return
        self.layers.append(rlayer)

    def run(self):
        """Run method that performs all the real work"""
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            self.addLayers()
            self.addCsvAction.setEnabled(True)

    def errorDialog(selg, text, detail):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(detail)
        msg.setWindowTitle("Error")
        msg.exec_()

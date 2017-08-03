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
from PyQt4.QtGui import QAction, QIcon, QColor
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
from math import sqrt
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
        # crs = QgsCoordinateReferenceSystem(3116)
        # self.iface.mapCanvas().mapRenderer().setDestinationCrs(crs)
        self.layers = []
        # self.sheet = None
        # self.work_layer = QgsVectorLayer('LineString?crs=epsg:3116&field=id:integer&field=name:string(20)&index=yes', 'temporal_points', 'memory')
        # self.work_layer.setCrs(QgsCoordinateReferenceSystem(3116, True))
        self.dlg = CalidadCARDialog()
        self.csvDialog = CSVDialog()

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

        icon_path = ':/plugins/CalidadCAR/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Cargar fondo'),
            callback=self.run,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Join'),
            callback=self.run2,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Intersection'),
            callback=self.intersection,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Agregar sección'),
            callback=self.addSection,
            parent=self.iface.mainWindow())

    def addSection(self):
        # self.work_layer = QgsVectorLayer('LineString?crs=epsg:3116&field=id:integer&field=name:string(20)&index=yes', 'temp', 'memory')
        tempLayer = None
        seccionesLayer = QgsMapLayerRegistry.instance().mapLayersByName("secciones")[0]

        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            print layer.name()
            if layer.name() == 'temp':
                self.iface.setActiveLayer(layer)
                tempLayer = self.iface.activeLayer()

        if tempLayer is None:
            tempLayer = QgsVectorLayer('LineString', 'temp', 'memory')
            QgsMapLayerRegistry.instance().addMapLayer(tempLayer)

        pr = tempLayer.dataProvider()
        fields = seccionesLayer.pendingFields()

        for f in fields:
            pr.addAttributes([f])

        # tempLayer.updateFields()
        #
        # feats1 = lyr[1].getFeatures()
        # for feature in feats1:
        #   pr.addFeatures([feature])
        #
        # feats3 = lyr[3].getFeatures()
        # for feature in feats3:
        #   pr.addFeatures([feature])

        # vl.updateExtents()

        tempLayer.startEditing()

    def distance(self, a, b):
        return sqrt(a.sqrDist(b))

    def check(self, segements, point):
        """Check if point c is between points a and b."""
        if len(segements) == 1 : return False
        polygon = geometry.buildPolygon(segements)
        # layer =  QgsVectorLayer('Polygon?crs=epsg:3116', 'poly' , "memory")
        # pr = layer.dataProvider()
        # poly = QgsFeature()
        # poly.setGeometry(polygon)
        # pr.addFeatures([poly])
        # layer.updateExtents()
        # QgsMapLayerRegistry.instance().addMapLayers([layer])
        return polygon.contains(point)

    def place(self, segements, p):
        low, hi = 0, len(segements)
        mid, cont = 0, 0

        while(low <= hi):
            mid =  low + ((hi - low) / 2)
            if self.check(segements[low : mid + 1], p):
                hi = mid
            else:
                low = mid
            cont += 1
            #Sacurity trigger
            if cont == 20: break

        return low

    def getSegments(self, layer):
        segements = []

        for f_seccion in layer.getFeatures():
            segements.append(f_seccion.geometry().asPolyline())

        return segements


    def intersection(self):
        secciones = QgsMapLayerRegistry.instance().mapLayersByName("secciones")[0]
        eje = QgsMapLayerRegistry.instance().mapLayersByName("ejes")[0]
        points = []
        for f_eje in eje.getFeatures():
            for f_seccion in secciones.getFeatures():
                if f_eje.geometry().intersects(f_seccion.geometry()):
                    inter = f_eje.geometry().intersection(f_seccion.geometry())
                    if inter.wkbType() == QGis.WKBPoint:
                        points.append(inter.asPoint())

        qgsPoints = [QgsPoint(point) for point in points]
        print qgsPoints
        distances = [0]
        for i in xrange(len(qgsPoints) - 1):
            distances.append(sqrt(qgsPoints[i].sqrDist(qgsPoints[i + 1])))
        # print distances

        pd_dataframe = pandas.DataFrame(distances, columns = ['Distancia'])
        # print pd_dataframe

        newPoints = []
        temp = QgsMapLayerRegistry.instance().mapLayersByName("temp")[0]
        for f_eje in eje.getFeatures():
            for f_seccion in temp.getFeatures():
                if f_eje.geometry().intersects(f_seccion.geometry()):
                    inter = f_eje.geometry().intersection(f_seccion.geometry())
                    if inter.wkbType() == QGis.WKBPoint:
                        newPoints.append(inter.asPoint())

        segs = self.getSegments(secciones)
        # for point in newPoints:
            # print self.place(segs, point)
        for point in newPoints:
            print self.place(segs, point)

        # layer =  QgsVectorLayer('Polygon?crs=epsg:3116', 'poly' , "memory")
        # pr = layer.dataProvider()
        # poly = QgsFeature()
        # poly.setGeometry(geometry.buildPolygon(segs))
        # pr.addFeatures([poly])
        # layer.updateExtents()
        # QgsMapLayerRegistry.instance().addMapLayers([layer])

        # print polygone.contains(newPoints[0])
    def run2(self):
        # """Join operation"""
        shp = None
        sheet = None
        # Run the dialog event loop
        result = self.csvDialog.exec_()
        if result and self.csvDialog.getLayer():
            print self.csvDialog.getSelectedColumns()

            sheet = self.csvDialog.getLayer()
            QgsMapLayerRegistry.instance().addMapLayer(sheet)
            #Get the shape layer called secciones
            layers = QgsMapLayerRegistry.instance().mapLayers().values()
            for layer in layers:
                if layer.name() == 'secciones':
                    self.iface.setActiveLayer(layer)
                    shp = self.iface.activeLayer()

            if shp == None: return

            columns = self.csvDialog.getSelectedColumns()
            field_names = [field.name() for field in shp.pendingFields() ]
            #Avoid duplitcate columns
            for new_col in columns:
                if 'csv_' + new_col in field_names:
                    columns.remove(new_col)

            shpField = 'RiverStatio'
            csvField = self.csvDialog.getJoinField()
            joinObject = QgsVectorJoinInfo()
            joinObject.joinLayerId = sheet.id()
            joinObject.joinFieldName = csvField
            joinObject.targetFieldName = shpField
            joinObject.setJoinFieldNamesSubset(columns)
            joinObject.memoryCache = True
            shp.addJoin(joinObject)
            # shp.updateFields()

            table = [row.attributes() for row in shp.getFeatures()]
            field_names = [field.name() for field in shp.pendingFields() ]
            print field_names

            pd_frame = pandas.DataFrame(table, columns = field_names)
            print pd_frame

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
        # Take the "CRS for new layers" config, overwrite it while loading layers and...
        #Borrando las capas
        for layer in self.layers:
            QgsMapLayerRegistry.instance().removeMapLayer(layer)
        self.layers = []
        #Paint all the layers
        files = self.dlg.getFilePaths()
        # print files

        for layer in files:
            path, name = layer
            layerInfo = QFileInfo(path)

            if layerInfo.suffix() == 'tif':
                self.addRasterLayer(path, name)
            elif layerInfo.suffix() == 'shp':
                self.addVectorLayer(path, name)

        for layer in self.layers:
            QgsMapLayerRegistry.instance().addMapLayer(layer)


        # QgsMapLayerRegistry.instance().addMapLayer(self.work_layer)
        # self.layers.insert(0, QgsMapCanvasLayer(self.work_layer))
        # self.canvas.setLayerSet(self.layers)
        # ... then set the "CRS for new layers" back

    def addVectorLayer(self, path, name):
        layerProvider = 'ogr'

        layer = QgsVectorLayer(path, name, 'ogr')
        if not layer.isValid():
            print 'invalid'
            return

        # myLayer = qgis.utils.iface.activeLayer()
        layer.setCrs(QgsCoordinateReferenceSystem(3116, QgsCoordinateReferenceSystem.EpsgCrsId))

        #Sets canvas CRS
        my_crs = QgsCoordinateReferenceSystem(3116, QgsCoordinateReferenceSystem.EpsgCrsId)
        self.iface.mapCanvas().mapRenderer().setDestinationCrs(my_crs)

        # print 'ProjAcronym: ', layer.crs().projectionAcronym()
        # print 'toWkt: ', layer.crs().toWkt()
        # itera = layer.getFeatures()
        # for feature in itera:
        #     for attrs in feature.attributes():
        #         obj = attrs.toPyObject()
        #         print type(obj)
        #         # for k, v in obj:
        #         #     print k , ': ', v

        # Cambiar el color del layer
        symbol_layer = layer.rendererV2().symbols()[0].symbolLayer(0)
        symbol_layer.setColor(QColor(randint(0, 50),randint(0, 255),163))

        # QgsMapLayerRegistry.instance().addMapLayer(layer)
        # if self.canvas.layerCount() == 0:
        #     self.canvas.setExtent(layer.extent())
        # my_crs = QgsCoordinateReferenceSystem(3116, QgsCoordinateReferenceSystem.EpsgCrsId)
        # layer.setCrs(my_crs)
        # crs = layer.crs()
        # crs.createFromId(3116)
        # layer.setCrs(QgsCoordinateReferenceSystem(3116, True))
        self.layers.append(layer)
        # self.layers.insert(0, layer)
        # self.canvas.setLayerSet(self.layers)


    def addRasterLayer(self, path, name):
        rlayer = QgsRasterLayer(path, name)

        if not rlayer.isValid():
            print "Layer failed to load!"
            return

        # print 'ProjAcronym: ', rlayer.crs().projectionAcronym()
        # print 'toWkt: ', rlayer.crs().toWkt()

        # QgsMapLayerRegistry.instance().addMapLayer(rlayer)
        # if self.canvas.layerCount() == 0:
        #     self.canvas.setExtent(rlayer.extent())

        self.layers.append(rlayer)


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            self.addLayers()

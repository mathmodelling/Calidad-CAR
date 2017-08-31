# -*- coding: utf-8 -*-
"""Este módulo es el que articula toda la funcionalidad del plugin,
y esta compuesto por la clase CalidadCAR."""

from qgis.core import ( QGis,
                        QgsField,
                        QgsPoint,
                        QgsFeature,
                        QgsGeometry,
                        QgsVectorLayer,
                        QgsRasterLayer,
                        QgsVectorJoinInfo,
                        QgsMapLayerRegistry,
                        QgsCoordinateReferenceSystem,
                        QgsCoordinateReferenceSystem)

from PyQt4.QtCore import ( QVariant,
                           qVersion,
                           QSettings,
                           QFileInfo,
                           QTranslator,
                           QCoreApplication)

from PyQt4.QtGui import ( QIcon,
                          QColor,
                          QAction,
                          QMessageBox)


import util
import os.path
import geometry
import resources
import numpy as np

from dialogo_csv import CSVDialog
from src import layer_manager as manager
from dialogo_concentracion import DialogoConcentracion
from calidad_car_dialog import Ui_Dialog as CalidadCARDialog
# import pandas

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

        icon_path = ':/plugins/CalidadCAR/icons/csv-join.png'
        self.addCsvAction = self.add_action(
            icon_path,
            text=self.tr(u'Unir CSV'),
            callback=self.addCsv,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icons/add-section.png'
        self.addSectionAction = self.add_action(
            icon_path,
            text=self.tr(u'Agregar sección'),
            callback=self.addSection,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/CalidadCAR/icons/concentration-icon.png'
        self.intersctionAction = self.add_action(
            icon_path,
            text=self.tr(u'Agregar puntos de concentración'),
            callback=self.concentrationPoints,
            parent=self.iface.mainWindow())

        # icon_path = ':/plugins/CalidadCAR/icons/start-icon.png'
        icon_path = ':/plugins/CalidadCAR/icons/execute.png'
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
        # self.addCsvAction.setEnabled(False)

    def clean(self):
        """Recarga el plugin, limpiando todas las capas cargadas, excepto, las
           capas de salida de información."""
        manager.remove_layers(self.layers)

        csv_layers = manager.get_all_layers("csv")
        manager.remove_layers(csv_layers)

        tempLayer = manager.get_layer("temp")
        if tempLayer is not None:
            tempLayer.commitChanges()
            manager.remove_layers([tempLayer])

        self.addCsvAction.setEnabled(True)
        self.layers = []

    def addSection(self):
        """Utiliza una capa llamada temp, para insertar las nuevas secciones,
           esta operación solo podrá ser realizada si existe la capa de secciones.

           En caso de que no exista la capa temp, se creara una nueva, con el crs
           de la capa de secciones.
        """
        if self.addCsvAction.isEnabled():
            title = u'Agregar sección transversal'
            detail = u'Una vez creada la capa de secciones no podrás unir más archivos CSV a la tabla de atributos de la capa de secciones.\n\n¿Deseas crear la capa de secciones?'

            if not util.questionDialog(self, title, detail):
                return

        tempLayer = None

        seccionesLayer = manager.get_layer('secciones')
        if seccionesLayer is None:
            util.errorDialog(self, u'No se encontró la capa de secciones.',
            u'Asegurate de agregarla en el diálogo de cargar fondos.')
            return

        #Bloquear acción de realizar más uniones con archivos CSV
        self.addCsvAction.setEnabled(False)

        tempLayer = manager.get_layer('temp')
        if tempLayer is None:
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

    def concentrationPoints(self):
        """Este método se encarga de recopilar toda la información, para permitirle al usuario ingresar los puntos de concentración.

           Para que el usuario pueda realizar esta operación, necesariamente, tienen que estar cargadas la capa de ejes, y la capa de secciones transversales.
        """
        secciones = manager.get_layer('secciones')
        eje = manager.get_layer('ejes')

        if secciones == None or eje == None:
            util.errorDialog(self, u'No se encontraron algunas de las capas necesarias para realizar esta operación.',
                    u'Asegurate de agregar la capa de secciones, y la capa del eje en el diálogo de Cargar Fondos.')
            return

        work_layer = self.addFeature(secciones)

        temp = manager.get_layer('temp')
        if temp is not None:
            """En caso de que existan secciones temporales, se combinaran con la
               capa de secciones, para crear la capa work_layer"""

            for new_feature in temp.getFeatures():
                segements = geometry.getSegments(work_layer)
                point = geometry.intersectionLayerGeometry(eje, new_feature.geometry())
                if point is None: continue
                idx = self.place(segements, point)
                # print 'IDX: ', idx
                work_layer = self.addFeature(work_layer, new_feature, idx)

        output = manager.get_layer('output')
        if output is not None:
            manager.remove_layers([output])

        #Mostrar la capa de trabajo work_layer
        manager.add_layers([work_layer])

        work_layer.dataProvider().addAttributes([QgsField(u'concentracion', QVariant.Double)])
        work_layer.startEditing()
        self.iface.showAttributeTable(work_layer)

    def intersection(self):
        """Se encarga de aplicar el modelo matemático a la información para determinar la calidad del agua.
        """

        work_layer = manager.get_layer('output')
        eje = manager.get_layer('ejes')

        if work_layer is None or eje is None:
            util.errorDialog(self, u'No se encontraron algunas de las capas necesarias para realizar esta operación.', u'Asegurate de agregar los puntos de concentración, y la capa del eje en el diálogo de Cargar Fondos.')
            return

        concentration_values = []
        vel_values = []

        field_names = [field.name() for field in work_layer.pendingFields()]
        text = u'Selecciona la columna en la que se encuentra la información ' +\
               ' de la velocidad:'

        vel_name = util.comboBoxDialog(self, u'Velocidad', text, field_names)
        if vel_name is None:
            util.errorDialog(self, u'La información de la velocidad es necesaria.',
        		u'Puedes agregarla con la opción de Unir CSV')
            return

        concen_idx = work_layer.fieldNameIndex('concentracion')
        vel_idx = work_layer.fieldNameIndex(vel_name)

        for feature in work_layer.getFeatures():
            try:
                concentration_values.append(float(feature.attributes()[concen_idx]))
                vel_values.append(float(feature.attributes()[vel_idx]))
            except TypeError:
                util.errorDialog(self, u'Uno de los valores en la columna de velocidad o puntos de concentración es nulo',
                u'Asegurate de que no hay valores nulos en la tabla.')
                return

        points = geometry.intersectionPoints(eje, work_layer)
        distances = [0]
        for i in xrange(len(points) - 1):
            distances.append(geometry.distance(points[i], points[i + 1]))
        # print distances
        condiciones_iniciales = np.array([distances, concentration_values]).T
        print condiciones_iniciales
        velocidad = np.array(vel_values)
        print velocidad

    def addCsv(self):
        """Crea una capa a partir de un archivo CSV, y une la información que
           contiene esta, con la tabla de atributos de la capa de secciones,
           la cual tendrá que existir, para que se pueda realizar esta operación.
        """
        shp = manager.get_layer('secciones')

        if shp is None:
            util.errorDialog(self, u'No se encontró la capa de secciones.',
            u'Asegurate de agregarla en el diálogo de Cargar fondos.')
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
        """Función que se ejecuta cuando el usuario hace click en la acción de Cargar Fondos"""
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            self.addLayers()
            # self.addCsvAction.setEnabled(True)

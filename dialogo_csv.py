# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog, QAbstractItemView, QMessageBox
from PyQt4.QtCore import QFileInfo, Qt

from qgis.core import QgsVectorLayer
from dialogs.dialogo_csv_base import Ui_DialogoCSV

# FORM_CLASS, _ = uic.loadUiType(os.path.join(
    # os.path.dirname(__file__), 'dialogo_csv_base.ui'))

CSV_SUFFIX = '?type=csv&geomType=none&subsetIndex=no&watchFile=no&delimiter=,'

class CSVDialog(QtGui.QDialog, Ui_DialogoCSV):
    """ Este diálogo es el encargado de carvar un archivo CSV, y
        de recolectar la información necesaria para unirlo con la
        capa de secciones.
    """
    def __init__(self, fields, parent=None):
        """Constructor de la clase.

        :param fields: Lista de strings que usara para llenar el combo box
                       self.comboJoinFieldTarget.
        :type a: Lista str
        """
        super(CSVDialog, self).__init__(parent)
        self.setupUi(self)

        self.fields = fields
        self._layer = None

        self.configWidgets()

    def configWidgets(self):
        """Configura los componentes gráficos del diálogo."""
        self.buttonLoadFile.clicked.connect(self.handler)
        self.buttonAddColumn.clicked.connect(self.addItem)
        self.buttonRemoveColumn.clicked.connect(self.removeItem)
        self.buttonClear.clicked.connect(self.clear)

        self.listSource.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listTarget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.comboJoinFieldTarget.addItems(self.fields)

    def getLayer(self):
        """Devuelve la el archivo CSV cargado como capa de QGIS.

        :returns: La capa de qgis del archivo CSV que el usuario cargo.
        :rtype: QgsVectorLayer.
        """
        return self._layer

    def getJoinField(self):
        """ Retorna el campo del archivo CSV sobre el cual se va a hacer la unión.

        :returns: Campo sobre el cual se a hacer la unión
        :rtype: str
        """
        return  str(self.comboJoinField.currentText())

    def getJoinFieldTarget(self):
        """ Retorna el campo de la capa secciones sobre el cual se va a hacer la unión
            con el archivo CSV.

        :returns: Campo sobre el cual se a hacer la unión
        :rtype: str
        """
        return str(self.comboJoinFieldTarget.currentText())

    def getSelectedColumns(self):
        """ Retorna todos los campos de self.listTarget, los cuales contienen
            las columnas seleccionadas para unir a la capa de secciones.

        :returns: Lista de las columnas seleccionadas.
        :rtype: Lista str.
        """

        if self.listTarget.count() > 0:
            """ En caso de que self.listTarget no contenga elementos, se seleccionarán
                los elementos de self.listSource.
            """
            items = self.getItems(self.listTarget)
        else:
            items = self.getItems(self.listSource)

        if self.getJoinField() in items:
            items.remove(self.getJoinField())

        return items

    def getItems(self, list):
        """Función auxiliar que extrae el texto de los items gráficos de la lista
           que se le pase.

        :param list: Lista de items a los cuales se les va a extraer el texto.
        :type list: QListWidget

        :returns: Lista del título de cada item.
        :rtype: Lista str
        """
        return [str(list.item(i).text()) for i in xrange(list.count())]

    def clear(self):
        """Limpia los componentes gráficos del diálogo.
        """
        self.editPath.setText('')
        self.listSource.clear()
        self.listTarget.clear()
        self.comboJoinField.clear()

    def handler(self):
        """Maneja el evento de click del botón self.buttonLoadFile"""

        layerPath = QFileDialog.getOpenFileName(self, u'Abrir CSV', '.', 'CSV (*.CSV)')
        layerInfo = QFileInfo(layerPath)
        self.editPath.setText(layerPath)

        try:
            self._layer = self.loadLayer(layerPath)
            columns = [field.name() for field in self._layer.pendingFields()]
            self.pupulateLists(columns)
        except:
            self.errorDialog(u'Error al cargar el archivo CSV',
                u'Asegurate de que el archivo no esta corrupto.')
            self.editPath.setText('')

    def pupulateLists(self, columns = []):
        """Llena las listas self.listSource, y self.comboJoinField con los nombres
           columnas del archivo CSV.

        :param columns: Son las columnas que se van a instertar en las listas.
        :type columns: Lista str
        """
        self.listSource.addItems(columns)
        self.comboJoinField.addItems(columns)

    def addItem(self):
        """Agrega los items seleccionados de self.listSource a self.listTarget.
        """
        for item in self.listSource.selectedItems():
            item.setHidden(True)
            self.listTarget.addItem(item.text())

    def removeItem(self):
        """Remueve los items seleccionados de self.listTarget."""
        for item in self.listTarget.selectedItems():
            source_index = self.listSource.findItems(item.text(), Qt.MatchExactly)
            source_index[0].setHidden(False)
            self.deleteItem(self.listTarget, item)

    def deleteItem(self, list, item):
        """Función auxiliar que remueve el un item de una lista.

        :param list: Lista de la cual se va a eliminar el item.
        :type list: QListWidget

        :param item: Item que se va a eliminar.
        :type item: QListWidgetItem
        """
        list.takeItem(list.row(item))

    def loadLayer(self, path, name = 'csv'):
        """Esta función crea una capa de QGIS, a partir de un archivo CSV, lanza una
           excepción en caso de que el archivo no sea válido.

        :param path: Ruta del archivo CSV.
        :type path: str

        :param name: Nombre que se le asignará a la capa, por defecto es csv.
        :type name: str

        :returns: En caso de que no acurra ningun error, retorna la capa del archivo
                  CSV.
        :rtype: QgsVectorLayer
        """

        #Formating the uri
        path = 'file:///' + path.replace('\\', '/') + CSV_SUFFIX
        layer = QgsVectorLayer(path, name, 'delimitedtext')

        if not layer.isValid():
            raise Error('Invalid Layer')

        return layer

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

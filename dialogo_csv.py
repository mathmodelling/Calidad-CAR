# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog, QAbstractItemView
from PyQt4.QtCore import QFileInfo, Qt

from qgis.core import QgsVectorLayer
from dialogo_csv_base import Ui_DialogoCSV
# FORM_CLASS, _ = uic.loadUiType(os.path.join(
    # os.path.dirname(__file__), 'dialogo_csv_base.ui'))

CSV_SUFFIX = '?type=csv&geomType=none&subsetIndex=no&watchFile=no&delimiter=,'

class CSVDialog(QtGui.QDialog, Ui_DialogoCSV):
    def __init__(self, fields, parent=None):
        """Constructor."""
        super(CSVDialog, self).__init__(parent)
        self.setupUi(self)

        self.fields = fields
        self._layer = None

        self.configWidgets()

    def configWidgets(self):
        """Configuration of the dialog's graphic elements."""
        self.buttonLoadFile.clicked.connect(self.handler)
        self.buttonAddColumn.clicked.connect(self.addItem)
        self.buttonRemoveColumn.clicked.connect(self.removeItem)
        self.buttonClear.clicked.connect(self.clear)

        self.listSource.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listTarget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.comboJoinFieldTarget.addItems(self.fields)

    def getLayer(self):
        """
        :returns: the qgis layer of the CSV file.
        :rtype: QgsVectorLayer.
        """
        return self._layer

    def getJoinField(self):
        return  str(self.comboJoinField.currentText())

    def getJoinFieldTarget(self):
        return str(self.comboJoinFieldTarget.currentText())

    def getSelectedColumns(self):
        """ Get all the columns of the listTarget.

        :returns: Array of columns.
        :rtype: String array.
        """
        if self.listTarget.count() > 0:
            """ Return the items of the listTarget if the user
                selected at least one element, otherwise return
                the elements of the listSource.
            """
            items = self.getItems(self.listTarget)
        else:
            items = self.getItems(self.listSource)

        if self.getJoinField() in items:
            items.remove(self.getJoinField())

        return items

    def getItems(self, list):
        return [str(list.item(i).text()) for i in xrange(list.count())]

    def clear(self):
        self.editPath.setText('')
        self.listSource.clear()
        self.listTarget.clear()
        self.comboJoinField.clear()

    def handler(self):
        """Handle function of the buttonLoadFile."""
        layerPath = QFileDialog.getOpenFileName(self, u'Abrir CSV', '.', 'CSV (*.CSV)')
        layerInfo = QFileInfo(layerPath)
        self.editPath.setText(layerPath)

        try:
            self._layer = self.loadLayer(layerPath)
            columns = [field.name() for field in self._layer.pendingFields()]
            self.pupulateLists(columns)
        except:
            #TODO: Alert the user with an error dialog
            self.editPath.setText('')

    def pupulateLists(self, columns = []):
        """Populate the listSource and the comboJoinField
            with the columns names.

        :param columns: The columns that are going to be inserted
            in the listSource
        :type columns: String array.
        """
        self.listSource.addItems(columns)
        self.comboJoinField.addItems(columns)

    def addItem(self):
        """Add the selected items in the source list, to the
           target list.
        """
        for item in self.listSource.selectedItems():
            item.setHidden(True)
            self.listTarget.addItem(item.text())

    def removeItem(self):
        """Remove the selected items form the target list."""
        for item in self.listTarget.selectedItems():
            source_index = self.listSource.findItems(item.text(), Qt.MatchExactly)
            source_index[0].setHidden(False)
            self.deleteItem(self.listTarget, item)

    def deleteItem(self, list, item):
        list.takeItem(list.row(item))

    def loadLayer(self, path, name = 'csv'):
        """Load a CSV layer, raise an error if the layer is not valid.

        :param path: Path of the csv layer.
        :type path: String

        :param name: Name of the layer, default value csv
        :type name: String

        :returns: If there is not it returns the qgis layer, with
            the information loaded.
        :rtype: QgsVectorLayer
        """

        #Formating the uri
        path = 'file:///' + path.replace('\\', '/') + CSV_SUFFIX
        print path
        layer = QgsVectorLayer(path, name, 'delimitedtext')

        if not layer.isValid():
            raise Error('Invalid Layer')
        else:
            print 'hiyaaa'

        return layer

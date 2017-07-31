# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog, QAbstractItemView
from PyQt4.QtCore import QFileInfo, Qt

from qgis.core import QgsVectorLayer

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dialogo_csv_base.ui'))

CSV_SUFFIX = '?type=csv&geomType=none&subsetIndex=no&watchFile=no&delimiter=,'

class CSVDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CSVDialog, self).__init__(parent)

        self.setupUi(self)
        self.configWidgets()
        self._layer = None

    def configWidgets(self):
        """Configuration of the dialog's graphic elements."""
        self.buttonLoadFile.clicked.connect(self.handler)
        self.buttonAddColumn.clicked.connect(self.addItem)
        self.buttonRemoveColumn.clicked.connect(self.removeItem)

        self.listSource.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listTarget.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def getLayer(self):
        """
        :returns: the qgis layer of the CSV file.
        :rtype: QgsVectorLayer.
        """
        return self._layer

    def getSelectedColumns(self):
        """ Get all the columns of the listTarget.

        :returns: Array of columns.
        :rtype: String array.
        """
        return [str(self.listTarget.item(i).text()) for i in xrange(self.listTarget.count())]

    def handler(self):
        """Handle function of the buttonLoadFile."""
        layerPath = QFileDialog.getOpenFileName(self, u'Abrir CSV', '.', 'CSV (*.CSV)')
        layerInfo = QFileInfo(layerPath)
        self.editPath.setText(layerPath)

        try:
            self._layer = self.loadLayer(layerPath)
            columns = [field.name() for field in self._layer.pendingFields()]
            self.pupulateSourceList(columns)
        except:
            #TODO: Alert the user with an error dialog
            self.editPath.setText('')

    def pupulateSourceList(self, columns = []):
        """Populate the listSource with columns

        :param columns: The columns that are going to be inserted
            in the listSource
        :type columns: String array.
        """
        self.listSource.addItems(columns)

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
            self.listTarget.takeItem(self.listTarget.row(item))


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
        layer = QgsVectorLayer(path + CSV_SUFFIX, name, 'delimitedtext')

        if not layer.isValid():
            raise Error('Invalid Layer')

        return layer

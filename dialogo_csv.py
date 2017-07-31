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
        self._layer = None

        self.buttonLoadFile.clicked.connect(self.handler)
        self.buttonAddColumn.clicked.connect(self.addItem)
        self.buttonRemoveColumn.clicked.connect(self.removeItem)

        self.listSource.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listTarget.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def getLayer(self):
        return self._layer

    def handler(self, title):
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
        self.listSource.addItems(columns)

    def addItem(self):
        """Add the selected items in the source list, to the
           target list."""
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
        layer = QgsVectorLayer(path + CSV_SUFFIX, name, 'delimitedtext')

        if not layer.isValid():
            raise Error('Invalid Layer')

        return layer

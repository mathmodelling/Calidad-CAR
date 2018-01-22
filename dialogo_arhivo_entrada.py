# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QFileInfo

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui', 'dialogo_crear_archivo_entrada.ui'))

FORM_CLASS_LOAD_FILE, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui', 'dialogo_cargar_archivo_base.ui'))

class InputFileDialog(QtGui.QDialog, FORM_CLASS):
    """Recibir información necesaria para crear el archivo de entrada"""

    def __init__(self, parent=None):
        """Constructor."""
        super(InputFileDialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButtonFind.clicked.connect(self.handler)

        validator = QtGui.QDoubleValidator()
        validatorInt = QtGui.QIntValidator()
        
        self.lineEditWD.setValidator(validator)
        self.lineEditSL.setValidator(validator)
        self.lineEditT.setValidator(validatorInt)

    def getT(self):
        """Retorna el valor T."""
        return self.lineEditT.text()

    def getWD(self):
        """Retorna el valor WD.
        """
        return self.lineEditWD.text()

    def getSL(self):
        """Retorna el valor SL"""
        return self.lineEditSL.text()

    def getFilePath(self):
        """Retorna la ruta del archivo que se va a crear.

        :returns: Ruta del archivo.
        :rtype: str.

        """
        return self.lineEditPath.text()

    def handler(self, title):
        """Maneja el evento de click sobre cualquiera de los botones de cargar archivo, con el fin de abrir un diálogo que le permita al usuario seleccionar el archivo de su sistema de archivos."""

        layerPath = QFileDialog.getSaveFileName(self, u'Crear archivo xls', '.', 'Archivo Excel (*.xls)')
        layerInfo = QFileInfo(layerPath)

        if layerPath == "" : return
        
        print layerInfo.fileName()

        if len(layerInfo.fileName()) < 5:
            layerPath += ".xls"
        elif layerInfo.fileName()[-4: ] != ".xls":
            layerPath += ".xls"

        self.lineEditPath.setText(layerPath)

class LoadInputFileDialog(QtGui.QDialog, FORM_CLASS_LOAD_FILE):
    def __init__(self, parent=None):
        """Constructor."""
        super(LoadInputFileDialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButtonFind.clicked.connect(self.handler)
        self.pushButtonOutput.clicked.connect(self.output)

    def getShowPlots(self):
        return self.checkBoxShow.isChecked()

    def getSavePlots(self):
        return self.checkBoxSave.isChecked()

    def getOutputPath(self):
        return self.lineEditOutput.text()
        
    def getFilePath(self):
        return self.lineEditPath.text()

    def output(self):
        path = QFileDialog.getExistingDirectory (self, 'Selecciona la carpeta de salida', '.', QFileDialog.ShowDirsOnly)
        self.lineEditOutput.setText(path)

    def handler(self):
        layerPath = QFileDialog.getOpenFileName(self, u'Abir archivo xls', '.', 'Archivo Excel (*.xls)')
        layerInfo = QFileInfo(layerPath)

        self.lineEditPath.setText(layerPath)
# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QFileInfo

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui', 'dialogo_crear_archivo_entrada.ui'))

class InputFileDialog(QtGui.QDialog, FORM_CLASS):
    """Recibir información necesaria para crear el archivo de entrada"""

    def __init__(self, parent=None):
        """Constructor."""
        super(InputFileDialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButtonFind.clicked.connect(self.handler)

        validator = QtGui.QDoubleValidator()
        self.lineEditWD.setValidator(validator)
        self.lineEditSL.setValidator(validator)

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

        layerPath = QFileDialog.getSaveFileName(self, u'Crear archivo xlsx', '.', 'Archivo Excel (*.xlsx)')
        layerInfo = QFileInfo(layerPath)

        if layerPath == "" : return
        
        print layerInfo.fileName()

        if len(layerInfo.fileName()) < 6:
            layerPath += ".xlsx"
        elif layerInfo.fileName()[-5: ] != ".xlsx":
            layerPath += ".xlsx"

        self.lineEditPath.setText(layerPath)
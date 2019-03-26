# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt import QtGui

from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtCore import QFileInfo

from .dialogs.calidad_car_dialog_base import Ui_Dialog as PUi_Dialog

# FORM_CLASS, _ = uic.loadUiType(os.path.join(
# os.path.dirname(__file__), 'calidad_car_dialog_base.ui'))

DEFAULT_LAYER = os.path.join(
    os.path.dirname(__file__),
    'data',
    'shapes',
    'Hidrografia.shp'
)


class Ui_Dialog(QDialog, PUi_Dialog):
    """Este diálogo es el encargado de permitirle al usuario cargar las capas necesarias."""

    def __init__(self, parent=None):
        """Constructor."""
        super(Ui_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.botonFindFondo.clicked.connect(lambda: self.handler('fondo'))
        self.botonFindHdr.clicked.connect(lambda: self.handler('hidr'))
        self.botonFindEjes.clicked.connect(lambda: self.handler('ejes'))
        self.botonFindSecciones.clicked.connect(lambda: self.handler('secc'))

        # Set the default layer
        self.capaHidrografia.setText(DEFAULT_LAYER)

    def getFilePaths(self):
        """Retorna la lista de rutas de las capas que el usuario desea cargar.

        :param list: Lista de items a los cuales se les va a extraer el texto.
        :type list: QListWidget

        :returns: La lista de las rutas de los archivos que el usuario selecciono.
        :rtype: Lista str.

        """

        filePaths = []
        if self.capaFondo.text():
            filePaths.append((self.capaFondo.text(), u'fondo'))
        if self.capaHidrografia.text():
            filePaths.append((self.capaHidrografia.text(), u'hidrografia'))
        if self.capaEjes.text():
            filePaths.append((self.capaEjes.text(), u'ejes'))
        if self.capaSecciones.text():
            filePaths.append((self.capaSecciones.text(), u'secciones'))

        return filePaths

    def handler(self, title):
        """
        Maneja el evento de click sobre cualquiera de los botones de
        cargar archivo, con el fin de abrir un diálogo que le permita al
        usuario seleccionar el archivo de su sistema de archivos.
        """

        layer_path = QFileDialog.getOpenFileName(
            self,
            'Abrir shapefile',
            '.',
            'Shapefiles (*.shp *.tif)'
        )

        layer_path = layer_path[0]

        if title == 'fondo':
            self.capaFondo.setText(layer_path)
        elif title == 'hidr':
            self.capaHidrografia.setText(layer_path)
        elif title == 'ejes':
            self.capaEjes.setText(layer_path)
        elif title == 'secc':
            self.capaSecciones.setText(layer_path)

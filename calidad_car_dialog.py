# -*- coding: utf-8 -*-
from __future__ import absolute_import

from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtWidgets import QDialog

from .dialogs.calidad_car_dialog_base import Ui_Dialog


class Ui_Dialog(QDialog, Ui_Dialog):
    """
    Este diálogo es el encargado de permitirle al usuario cargar las
    capas necesarias.
    """

    def __init__(self, parent=None):
        """Constructor."""
        super(Ui_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.botonFindFondo.clicked.connect(lambda: self.handler('fondo'))
        self.botonFindHdr.clicked.connect(lambda: self.handler('hidr'))
        self.botonFindEjes.clicked.connect(lambda: self.handler('ejes'))
        self.botonFindSecciones.clicked.connect(lambda: self.handler('secc'))

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

        layerPath, __ = QFileDialog.getOpenFileName(
            self,
            u'Abrir shapefile',
            '.',
            'Shapefiles (*.shp *.tif)'
        )

        if title == 'fondo':
            self.capaFondo.setText(layerPath)
        elif title == 'hidr':
            self.capaHidrografia.setText(layerPath)
        elif title == 'ejes':
            self.capaEjes.setText(layerPath)
        elif title == 'secc':
            self.capaSecciones.setText(layerPath)

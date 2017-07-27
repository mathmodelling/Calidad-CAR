# -*- coding: utf-8 -*-
"""
/***************************************************************************
 aDialog
                                 A QGIS plugin
 a
                             -------------------
        begin                : 2017-07-24
        git sha              : $Format:%H$
        copyright            : (C) 2017 by a
        email                : a
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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QFileInfo

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'calidad_car_dialog_base.ui'))


class Ui_Dialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Ui_Dialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.botonFindFondo.clicked.connect(lambda: self.handler('fondo'))
        self.botonFindHdr.clicked.connect(lambda: self.handler('hidr'))
        self.botonFindEjes.clicked.connect(lambda: self.handler('ejes'))
        self.botonFindSecciones.clicked.connect(lambda: self.handler('secc'))

    def getFilePaths(self):
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
        layerPath = QFileDialog.getOpenFileName(self, u'Abrir shapefile', '.', 'Shapefiles (*.shp *.tif)')
        layerInfo = QFileInfo(layerPath)

        if title == 'fondo':
            self.capaFondo.setText(layerPath)
        elif title == 'hidr':
            self.capaHidrografia.setText(layerPath)
        elif title == 'ejes':
            self.capaEjes.setText(layerPath)
        elif title == 'secc':
            self.capaSecciones.setText(layerPath)

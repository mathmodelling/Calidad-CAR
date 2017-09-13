# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui
from dialogs.parametros_base import Ui_Dialog

class SettingsDialog(QtGui.QDialog, Ui_Dialog):
    """Este diálogo es el encargado de permitirle al usuario cargar las capas necesarias."""

    def __init__(self, values, parent = None):
        """Constructor."""
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)

        self.comboVelocidad.addItems(values)
        self.comboConcentracion.addItems(values)

        #Para evitar que el usuario redimensione el diálogo
        self.setFixedSize(self.size())

    def getVelocidad(self):
        return str(self.comboVelocidad.currentText())

    def getConcentracion(self):
        return str(self.comboConcentracion.currentText())

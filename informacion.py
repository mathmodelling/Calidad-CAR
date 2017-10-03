# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui
from informacion_base import Ui_Dialog

class InformationDialog(QtGui.QDialog, Ui_Dialog):
    """Este diálogo es el encargado de permitirle al usuario cargar las capas necesarias."""

    def __init__(self, parent = None):
        """Constructor."""
        super(InformationDialog, self).__init__(parent)
        self.setupUi(self)

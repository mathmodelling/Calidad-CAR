# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui
from dialogs.combobox_base import Ui_Dialog

class ComboBoxDialog(QtGui.QDialog, Ui_Dialog):
    """Este diálogo es el encargado de permitirle al usuario cargar las capas necesarias."""

    def __init__(self, title, text, values, parent=None):
        """Constructor."""
        super(ComboBoxDialog, self).__init__(parent)
        self.setupUi(self)

        self.label.setText(text)
        self.setWindowTitle(title)
        self.comboBox.addItems(values)

        #Para evitar que el usuario redimensione el diálogo
        self.setFixedSize(self.size())

    def getSelectedItem(self):
        return str(self.comboBox.currentText())

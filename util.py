# -*- coding: utf-8 -*-

from __future__ import absolute_import
from qgis.PyQt.QtWidgets import QMessageBox
from .dialogo_combobox import ComboBoxDialog

def questionDialog(self, title, detail):
    """Este díalogo le hace una pregunta de Si/No al usuario.

    :param title: Título del diálogo
    :type title: str

    :param detail: Texto descriptivo del diálogo
    :type detail: str

    :returns: La respuesta del usuario
    :rtype: bool
    """
    reply = QMessageBox.question(self.iface.mainWindow(), title, detail,
        QMessageBox.Yes | QMessageBox.No)

    return reply == QMessageBox.Yes

def errorDialog(self, text, detail):
    """Dialogo de error que se lanzará cuando el usuario intente hacer una operación que no esta permitida.

    :param text: Identificador principal del error.
    :type text: str

    :param name: Información detallada del error.
    :type name: str
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setInformativeText(detail)
    msg.setWindowTitle("Error")
    msg.exec_()

def infoDialog(self, title, text, detail):
    """Dialogo de información.

    :param text: Identificador principal del mensaje.
    :type text: str

    :param name: Información detallada del mensaje.
    :type name: str
    """
    msg = QMessageBox()
    msg.setText(text)
    msg.setInformativeText(detail)
    msg.setWindowTitle(title)
    msg.exec_()

def comboBoxDialog(self, title, text, values):
    """Este diálogo le pide al usuario que seleccione una opción de un combobox y la retorna.

    :param title: Título del diálogo
    :type title: str

    :param text: Texto descriptivo del diálogo
    :type text: str

    :param values: Opciones con las que se va a llenar el combobox
    :type values: List str

    :returns: En caso de Aceptar retorna la opción que escogio, retorna None en caso de Cancelar
    :rtype: str
    """
    dialog = ComboBoxDialog(title, text, values)

    if dialog.exec_():
        return dialog.getSelectedItem()

    return None

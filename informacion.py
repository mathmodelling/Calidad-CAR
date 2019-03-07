# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

from qgis.PyQt.QtWidgets import QDialog
from .informacion_base import Ui_Dialog

DOC_PATH = "file:///" + os.path.join(
    os.path.dirname(__file__),
    'docs',
    'index.html'
).replace('\\', '/')

PLUGIN_URL = "http://plugins.qgis.org/plugins/CalidadCAR/"


class InformationDialog(QDialog, Ui_Dialog):
    """
    Este diálogo es el encargado de permitirle al usuario cargar las
    capas necesarias.
    """

    def __init__(self, parent = None):
        """Constructor."""
        super(InformationDialog, self).__init__(parent)
        self.setupUi(self)

        style_open = "<span style=\" text-decoration: underline; color:#2980b9;\">"
        style_close = "</span>"

        info = "<a href=\"%s\">%s%s%s</a>" % (
            PLUGIN_URL,
            style_open,
            u"Información de desarrollo",
            style_close
        )
        text = "<a href=\"%s\">%s%s%s</a>" % (
            DOC_PATH,
            style_open,
            u"Documentación",
            style_close
        )

        self.label_4.setText(text + " - " + info)

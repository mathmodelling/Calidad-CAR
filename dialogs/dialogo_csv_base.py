# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogo_csv_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from qgis.PyQt import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DialogoCSV(object):
    def setupUi(self, DialogoCSV):
        DialogoCSV.setObjectName(_fromUtf8("DialogoCSV"))
        DialogoCSV.resize(482, 409)
        self.buttonBox = QtGui.QDialogButtonBox(DialogoCSV)
        self.buttonBox.setGeometry(QtCore.QRect(380, 10, 81, 71))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.buttonAddColumn = QtGui.QPushButton(DialogoCSV)
        self.buttonAddColumn.setGeometry(QtCore.QRect(380, 250, 81, 28))
        self.buttonAddColumn.setObjectName(_fromUtf8("buttonAddColumn"))
        self.buttonRemoveColumn = QtGui.QPushButton(DialogoCSV)
        self.buttonRemoveColumn.setGeometry(QtCore.QRect(380, 280, 81, 28))
        self.buttonRemoveColumn.setObjectName(_fromUtf8("buttonRemoveColumn"))
        self.groupBox = QtGui.QGroupBox(DialogoCSV)
        self.groupBox.setGeometry(QtCore.QRect(10, 220, 461, 181))
        self.groupBox.setStyleSheet(_fromUtf8("QGroupBox { \n"
"     border: 1px solid gray; \n"
"     border-radius: 3px; \n"
" } "))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.listSource = QtGui.QListWidget(self.groupBox)
        self.listSource.setGeometry(QtCore.QRect(10, 30, 175, 141))
        self.listSource.setStyleSheet(_fromUtf8(""))
        self.listSource.setObjectName(_fromUtf8("listSource"))
        self.listTarget = QtGui.QListWidget(self.groupBox)
        self.listTarget.setGeometry(QtCore.QRect(190, 30, 175, 141))
        self.listTarget.setStyleSheet(_fromUtf8(""))
        self.listTarget.setObjectName(_fromUtf8("listTarget"))
        self.label = QtGui.QLabel(DialogoCSV)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.editPath = QtGui.QLineEdit(DialogoCSV)
        self.editPath.setGeometry(QtCore.QRect(20, 40, 311, 32))
        self.editPath.setObjectName(_fromUtf8("editPath"))
        self.buttonLoadFile = QtGui.QPushButton(DialogoCSV)
        self.buttonLoadFile.setGeometry(QtCore.QRect(330, 40, 41, 32))
        self.buttonLoadFile.setObjectName(_fromUtf8("buttonLoadFile"))
        self.label_2 = QtGui.QLabel(DialogoCSV)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 291, 31))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.comboJoinField = QtGui.QComboBox(DialogoCSV)
        self.comboJoinField.setGeometry(QtCore.QRect(20, 170, 351, 30))
        self.comboJoinField.setObjectName(_fromUtf8("comboJoinField"))
        self.buttonClear = QtGui.QPushButton(DialogoCSV)
        self.buttonClear.setGeometry(QtCore.QRect(380, 80, 81, 28))
        self.buttonClear.setObjectName(_fromUtf8("buttonClear"))
        self.label_3 = QtGui.QLabel(DialogoCSV)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 201, 31))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.comboJoinFieldTarget = QtGui.QComboBox(DialogoCSV)
        self.comboJoinFieldTarget.setGeometry(QtCore.QRect(20, 110, 351, 30))
        self.comboJoinFieldTarget.setObjectName(_fromUtf8("comboJoinFieldTarget"))
        self.groupBox.raise_()
        self.buttonBox.raise_()
        self.label.raise_()
        self.editPath.raise_()
        self.buttonLoadFile.raise_()
        self.label_2.raise_()
        self.comboJoinField.raise_()
        self.buttonClear.raise_()
        self.label_3.raise_()
        self.comboJoinFieldTarget.raise_()
        self.buttonAddColumn.raise_()
        self.buttonRemoveColumn.raise_()

        self.retranslateUi(DialogoCSV)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogoCSV.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogoCSV.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogoCSV)

    def retranslateUi(self, DialogoCSV):
        DialogoCSV.setWindowTitle(_translate("DialogoCSV", "Agregar capa CSV", None))
        self.buttonAddColumn.setText(_translate("DialogoCSV", "Agregar", None))
        self.buttonRemoveColumn.setText(_translate("DialogoCSV", "Eliminar", None))
        self.groupBox.setTitle(_translate("DialogoCSV", "Agregar columnas", None))
        self.label.setText(_translate("DialogoCSV", "Cargar CSV", None))
        self.buttonLoadFile.setText(_translate("DialogoCSV", "...", None))
        self.label_2.setText(_translate("DialogoCSV", "Campo de unión (Capa de Secciones):", None))
        self.buttonClear.setText(_translate("DialogoCSV", "Limpiar", None))
        self.label_3.setText(_translate("DialogoCSV", "Campo de unión (CSV):", None))


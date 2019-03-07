# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dialogo_parametros_base.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from future import standard_library
standard_library.install_aliases()
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(460, 417)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 370, 421, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 40, 421, 69))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.comboVelocidad = QtGui.QComboBox(self.layoutWidget)
        self.comboVelocidad.setObjectName(_fromUtf8("comboVelocidad"))
        self.verticalLayout.addWidget(self.comboVelocidad)
        self.layoutWidget1 = QtGui.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 140, 421, 69))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.comboConcentracion = QtGui.QComboBox(self.layoutWidget1)
        self.comboConcentracion.setObjectName(_fromUtf8("comboConcentracion"))
        self.verticalLayout_2.addWidget(self.comboConcentracion)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 220, 421, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 401, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.radioButtonTime = QtGui.QRadioButton(self.groupBox)
        self.radioButtonTime.setGeometry(QtCore.QRect(20, 60, 201, 26))
        self.radioButtonTime.setObjectName(_fromUtf8("radioButtonTime"))
        self.radioButtonDist = QtGui.QRadioButton(self.groupBox)
        self.radioButtonDist.setGeometry(QtCore.QRect(20, 90, 201, 26))
        self.radioButtonDist.setObjectName(_fromUtf8("radioButtonDist"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Configurar parámetros", None))
        self.label.setText(_translate("Dialog", "Selecciona la columna en la que se encuentra la información de la velocidad:", None))
        self.label_2.setText(_translate("Dialog", "Selecciona la columna en la que se encuentra la información de los puntos de concentración:", None))
        self.groupBox.setTitle(_translate("Dialog", "Salida", None))
        self.label_3.setText(_translate("Dialog", "Selecciona la gráfica de concentración de que deseas ver:", None))
        self.radioButtonTime.setText(_translate("Dialog", "Concentración / Tiempo", None))
        self.radioButtonDist.setText(_translate("Dialog", "Concentración / Distancia", None))


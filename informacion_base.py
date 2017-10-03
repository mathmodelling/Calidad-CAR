# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/informacion_base.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        Dialog.resize(370, 409)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(270, 360, 81, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 60, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 341, 131))
        self.label_2.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.icon = QtGui.QLabel(Dialog)
        self.icon.setGeometry(QtCore.QRect(250, 10, 111, 91))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 320, 351, 31))
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 220, 341, 81))
        self.label_5.setWordWrap(True)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Información", None))
        self.label.setText(_translate("Dialog", "Calidad-CAR", None))
        self.label_2.setText(_translate("Dialog", "Calidad-CAR es una herramienta para modelar matemáticamente la calidad del agua en los ríos. Esta herramienta asume que el usuario tiene los resultados del modelado del movimiento del agua con la herramienta Hec-Ras.", None))
        self.icon.setText(_translate("Dialog", "<html><head/><body><p><img src=\":/plugins/CalidadCAR/icons/logo.png\"/>.</p></body></html>", None))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p><a href=\"https://cbdavide.github.io/Calidad-CAR/help/manual_usuario.html\"><span style=\" text-decoration: underline; color:#2980b9;\">Documentación</span></a> — <a href=\"http://plugins.qgis.org/plugins/CalidadCAR/\"><span style=\" text-decoration: underline; color:#2980b9;\">Información de desarrollo</span></a></p></body></html>", None))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p align=\"justify\">Este es un desarrollo de la Corporación Autónoma Regional de Cundinamarca - <a href=\"https://www.car.gov.co/\"><span style=\" text-decoration: underline; color:#2980b9;\">CAR</span></a> Licenciado bajo los términos de la GNU GPL v3.0.</p></body></html>", None))

import resources

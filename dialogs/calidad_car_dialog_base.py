# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calidad_car_dialog_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        Dialog.resize(400, 300)
        self.botonCancelar = QtGui.QDialogButtonBox(Dialog)
        self.botonCancelar.setGeometry(QtCore.QRect(40, 240, 341, 32))
        self.botonCancelar.setOrientation(QtCore.Qt.Horizontal)
        self.botonCancelar.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.botonCancelar.setObjectName(_fromUtf8("botonCancelar"))
        self.capaFondo = QtGui.QLineEdit(Dialog)
        self.capaFondo.setGeometry(QtCore.QRect(170, 50, 160, 32))
        self.capaFondo.setObjectName(_fromUtf8("capaFondo"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 60, 111, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 131, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.capaHidrografia = QtGui.QLineEdit(Dialog)
        self.capaHidrografia.setGeometry(QtCore.QRect(170, 90, 160, 32))
        self.capaHidrografia.setObjectName(_fromUtf8("capaHidrografia"))
        self.botonFindFondo = QtGui.QPushButton(Dialog)
        self.botonFindFondo.setGeometry(QtCore.QRect(330, 50, 41, 32))
        self.botonFindFondo.setObjectName(_fromUtf8("botonFindFondo"))
        self.botonFindHdr = QtGui.QPushButton(Dialog)
        self.botonFindHdr.setGeometry(QtCore.QRect(330, 90, 41, 32))
        self.botonFindHdr.setObjectName(_fromUtf8("botonFindHdr"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 131, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.capaEjes = QtGui.QLineEdit(Dialog)
        self.capaEjes.setGeometry(QtCore.QRect(170, 130, 160, 32))
        self.capaEjes.setObjectName(_fromUtf8("capaEjes"))
        self.botonFindEjes = QtGui.QPushButton(Dialog)
        self.botonFindEjes.setGeometry(QtCore.QRect(330, 130, 41, 32))
        self.botonFindEjes.setObjectName(_fromUtf8("botonFindEjes"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 180, 131, 31))
        self.label_4.setTextFormat(QtCore.Qt.PlainText)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.capaSecciones = QtGui.QLineEdit(Dialog)
        self.capaSecciones.setGeometry(QtCore.QRect(170, 180, 160, 32))
        self.capaSecciones.setObjectName(_fromUtf8("capaSecciones"))
        self.botonFindSecciones = QtGui.QPushButton(Dialog)
        self.botonFindSecciones.setGeometry(QtCore.QRect(330, 180, 41, 32))
        self.botonFindSecciones.setObjectName(_fromUtf8("botonFindSecciones"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.botonCancelar, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.botonCancelar, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Configurar fondo", None))
        self.label.setText(_translate("Dialog", "Capa de fondo", None))
        self.label_2.setText(_translate("Dialog", "Capa de hidrografía", None))
        self.botonFindFondo.setText(_translate("Dialog", "...", None))
        self.botonFindHdr.setText(_translate("Dialog", "...", None))
        self.label_3.setText(_translate("Dialog", "Capa de ejes", None))
        self.botonFindEjes.setText(_translate("Dialog", "...", None))
        self.label_4.setText(_translate("Dialog", "Capa de secciones transversales", None))
        self.botonFindSecciones.setText(_translate("Dialog", "...", None))


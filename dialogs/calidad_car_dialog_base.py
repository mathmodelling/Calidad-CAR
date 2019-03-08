# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/calidad_car_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.botonCancelar = QtWidgets.QDialogButtonBox(Dialog)
        self.botonCancelar.setGeometry(QtCore.QRect(40, 240, 341, 32))
        self.botonCancelar.setOrientation(QtCore.Qt.Horizontal)
        self.botonCancelar.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.botonCancelar.setObjectName("botonCancelar")
        self.capaFondo = QtWidgets.QLineEdit(Dialog)
        self.capaFondo.setGeometry(QtCore.QRect(170, 50, 160, 32))
        self.capaFondo.setObjectName("capaFondo")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 60, 111, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 131, 20))
        self.label_2.setObjectName("label_2")
        self.capaHidrografia = QtWidgets.QLineEdit(Dialog)
        self.capaHidrografia.setGeometry(QtCore.QRect(170, 90, 160, 32))
        self.capaHidrografia.setObjectName("capaHidrografia")
        self.botonFindFondo = QtWidgets.QPushButton(Dialog)
        self.botonFindFondo.setGeometry(QtCore.QRect(330, 50, 41, 32))
        self.botonFindFondo.setObjectName("botonFindFondo")
        self.botonFindHdr = QtWidgets.QPushButton(Dialog)
        self.botonFindHdr.setGeometry(QtCore.QRect(330, 90, 41, 32))
        self.botonFindHdr.setObjectName("botonFindHdr")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 131, 20))
        self.label_3.setObjectName("label_3")
        self.capaEjes = QtWidgets.QLineEdit(Dialog)
        self.capaEjes.setGeometry(QtCore.QRect(170, 130, 160, 32))
        self.capaEjes.setObjectName("capaEjes")
        self.botonFindEjes = QtWidgets.QPushButton(Dialog)
        self.botonFindEjes.setGeometry(QtCore.QRect(330, 130, 41, 32))
        self.botonFindEjes.setObjectName("botonFindEjes")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 180, 131, 31))
        self.label_4.setTextFormat(QtCore.Qt.PlainText)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.capaSecciones = QtWidgets.QLineEdit(Dialog)
        self.capaSecciones.setGeometry(QtCore.QRect(170, 180, 160, 32))
        self.capaSecciones.setObjectName("capaSecciones")
        self.botonFindSecciones = QtWidgets.QPushButton(Dialog)
        self.botonFindSecciones.setGeometry(QtCore.QRect(330, 180, 41, 32))
        self.botonFindSecciones.setObjectName("botonFindSecciones")

        self.retranslateUi(Dialog)
        self.botonCancelar.accepted.connect(Dialog.accept)
        self.botonCancelar.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Configurar fondo"))
        self.label.setText(_translate("Dialog", "Capa de fondo"))
        self.label_2.setText(_translate("Dialog", "Capa de hidrografía"))
        self.botonFindFondo.setText(_translate("Dialog", "..."))
        self.botonFindHdr.setText(_translate("Dialog", "..."))
        self.label_3.setText(_translate("Dialog", "Capa de ejes"))
        self.botonFindEjes.setText(_translate("Dialog", "..."))
        self.label_4.setText(_translate("Dialog", "Capa de secciones transversales"))
        self.botonFindSecciones.setText(_translate("Dialog", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


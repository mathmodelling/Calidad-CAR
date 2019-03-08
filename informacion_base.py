# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/informacion_base.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(370, 409)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(270, 360, 81, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 60, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 341, 131))
        self.label_2.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.icon = QtWidgets.QLabel(Dialog)
        self.icon.setGeometry(QtCore.QRect(250, 10, 111, 91))
        self.icon.setObjectName("icon")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 320, 351, 31))
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 220, 341, 81))
        self.label_5.setWordWrap(True)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Información"))
        self.label.setText(_translate("Dialog", "Calidad-CAR"))
        self.label_2.setText(_translate("Dialog", "Calidad-CAR es una herramienta para modelar matemáticamente la calidad del agua en los ríos. Esta herramienta asume que el usuario tiene los resultados del modelado del movimiento del agua con la herramienta Hec-Ras."))
        self.icon.setText(_translate("Dialog", "<html><head/><body><p><img src=\":/plugins/CalidadCAR/icons/logo.png\"/>.</p></body></html>"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p><a href=\"https://cbdavide.github.io/Calidad-CAR/help/manual_usuario.html\"><span style=\" text-decoration: underline; color:#2980b9;\">Documentación</span></a> — <a href=\"http://plugins.qgis.org/plugins/CalidadCAR/\"><span style=\" text-decoration: underline; color:#2980b9;\">Información de desarrollo</span></a></p></body></html>"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p align=\"justify\">Este es un desarrollo de la Corporación Autónoma Regional de Cundinamarca - <a href=\"https://www.car.gov.co/\"><span style=\" text-decoration: underline; color:#2980b9;\">CAR</span></a> Licenciado bajo los términos de la GNU GPL v3.0.</p></body></html>"))

from . import resources

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


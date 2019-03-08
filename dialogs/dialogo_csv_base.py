# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dialogo_csv_base.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogoCSV(object):
    def setupUi(self, DialogoCSV):
        DialogoCSV.setObjectName("DialogoCSV")
        DialogoCSV.resize(482, 409)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogoCSV)
        self.buttonBox.setGeometry(QtCore.QRect(380, 10, 81, 71))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonAddColumn = QtWidgets.QPushButton(DialogoCSV)
        self.buttonAddColumn.setGeometry(QtCore.QRect(380, 250, 81, 28))
        self.buttonAddColumn.setObjectName("buttonAddColumn")
        self.buttonRemoveColumn = QtWidgets.QPushButton(DialogoCSV)
        self.buttonRemoveColumn.setGeometry(QtCore.QRect(380, 280, 81, 28))
        self.buttonRemoveColumn.setObjectName("buttonRemoveColumn")
        self.groupBox = QtWidgets.QGroupBox(DialogoCSV)
        self.groupBox.setGeometry(QtCore.QRect(10, 220, 461, 181))
        self.groupBox.setStyleSheet("QGroupBox { \n"
"     border: 1px solid gray; \n"
"     border-radius: 3px; \n"
" } ")
        self.groupBox.setObjectName("groupBox")
        self.listSource = QtWidgets.QListWidget(self.groupBox)
        self.listSource.setGeometry(QtCore.QRect(10, 30, 175, 141))
        self.listSource.setStyleSheet("")
        self.listSource.setObjectName("listSource")
        self.listTarget = QtWidgets.QListWidget(self.groupBox)
        self.listTarget.setGeometry(QtCore.QRect(190, 30, 175, 141))
        self.listTarget.setStyleSheet("")
        self.listTarget.setObjectName("listTarget")
        self.label = QtWidgets.QLabel(DialogoCSV)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 20))
        self.label.setObjectName("label")
        self.editPath = QtWidgets.QLineEdit(DialogoCSV)
        self.editPath.setGeometry(QtCore.QRect(20, 40, 311, 32))
        self.editPath.setObjectName("editPath")
        self.buttonLoadFile = QtWidgets.QPushButton(DialogoCSV)
        self.buttonLoadFile.setGeometry(QtCore.QRect(330, 40, 41, 32))
        self.buttonLoadFile.setObjectName("buttonLoadFile")
        self.label_2 = QtWidgets.QLabel(DialogoCSV)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 291, 31))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.comboJoinField = QtWidgets.QComboBox(DialogoCSV)
        self.comboJoinField.setGeometry(QtCore.QRect(20, 170, 351, 30))
        self.comboJoinField.setObjectName("comboJoinField")
        self.buttonClear = QtWidgets.QPushButton(DialogoCSV)
        self.buttonClear.setGeometry(QtCore.QRect(380, 80, 81, 28))
        self.buttonClear.setObjectName("buttonClear")
        self.label_3 = QtWidgets.QLabel(DialogoCSV)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 201, 31))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.comboJoinFieldTarget = QtWidgets.QComboBox(DialogoCSV)
        self.comboJoinFieldTarget.setGeometry(QtCore.QRect(20, 110, 351, 30))
        self.comboJoinFieldTarget.setObjectName("comboJoinFieldTarget")
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
        self.buttonBox.accepted.connect(DialogoCSV.accept)
        self.buttonBox.rejected.connect(DialogoCSV.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogoCSV)

    def retranslateUi(self, DialogoCSV):
        _translate = QtCore.QCoreApplication.translate
        DialogoCSV.setWindowTitle(_translate("DialogoCSV", "Agregar capa CSV"))
        self.buttonAddColumn.setText(_translate("DialogoCSV", "Agregar"))
        self.buttonRemoveColumn.setText(_translate("DialogoCSV", "Eliminar"))
        self.groupBox.setTitle(_translate("DialogoCSV", "Agregar columnas"))
        self.label.setText(_translate("DialogoCSV", "Cargar CSV"))
        self.buttonLoadFile.setText(_translate("DialogoCSV", "..."))
        self.label_2.setText(_translate("DialogoCSV", "Campo de unión (Capa de Secciones):"))
        self.buttonClear.setText(_translate("DialogoCSV", "Limpiar"))
        self.label_3.setText(_translate("DialogoCSV", "Campo de unión (CSV):"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogoCSV = QtWidgets.QDialog()
    ui = Ui_DialogoCSV()
    ui.setupUi(DialogoCSV)
    DialogoCSV.show()
    sys.exit(app.exec_())


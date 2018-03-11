import os
from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui', 'dialogo_dibujar_vertices.ui'))

class NoSelectedOption(Exception):
    def __str__(self):
        return "There is no option selected."

class NotLoadedPoints(Exception):
    def __str__(self):
        return "The user did not upload any points."

class DrawDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(DrawDialog, self).__init__(parent)
        self.setupUi(self)

        self.radioButtonDraw.clicked.connect(self.optionHandler)
        self.radioButtonLoad.clicked.connect(self.optionHandler)

    def optionHandler(self):
        if self.radioButtonDraw.isChecked():
            self.textEditPoints.setDisabled(True)
        else:
            self.textEditPoints.setDisabled(False)

    def getOption(self):
	   return self.radioButtonDraw.isChecked()

    def getCoords(self):
        points = []
        coords = self.textEditPoints.toPlainText()
        print coords

        for coord in coords.splitlines():
            x, y = [float(t) for t in coord.split()]
            points.append((x, y))

        return points

    def validate(self):
        if not self.radioButtonLoad.isChecked() and \
            not self.radioButtonDraw.isChecked():
            raise NoSelectedOption

        if self.radioButtonLoad.isChecked():
            points = self.getCoords()
            if points == []:
                raise NotLoadedPoints

        return True

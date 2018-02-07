#-*- encoding:utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
import sys


class paramForm(QtGui.QDialog):
    def __init__(self, params):
        super(paramForm, self).__init__()

        self.labels = {}
        self.texts = {}

        layout = QtGui.QGridLayout(self)
        counter = 0
        for comando in params:
            for parametro in comando:
                self.labels[counter] = QtGui.QLabel(parametro, self)
                self.texts[counter] = QtGui.QLineEdit(self)
                layout.addWidget(self.labels[counter], counter, 0)
                layout.addWidget(self.texts[counter], counter, 1)
                counter += 1

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        layout.addWidget(buttons)
        self.setLayout(layout)
        self.setModal(True)

    @staticmethod
    def getNewParams(oldParams):
        if not any(oldParams):
            return (oldParams, 1)
        dialog = paramForm(oldParams)
        result = dialog.exec_()

        count = 0
        listas_parametros = []
        for comando in oldParams:
            params = []
            for _ in comando:
                params.append(str(dialog.texts[count].text()))
                count += 1
            listas_parametros.append(params)
        return (listas_parametros, result == QDialog.Accepted)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    gui = paramForm.getNewParams(
        [["un parametro", "dos parametro"], ["tercer param"]])
    sys.exit(app.exec_())

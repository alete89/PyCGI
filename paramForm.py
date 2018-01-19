#-*- encoding:utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
import sys


class paramForm(QtGui.QDialog):
    def __init__(self, params):
        super(paramForm, self).__init__()

        # Debug
        # params = ["un parametro", "otro parametro"]
        # Debug
        self.labels = {}
        self.texts = {}

        layout = QtGui.QGridLayout(self)

        for p, parametro in enumerate(params):
            self.labels[p] = QtGui.QLabel(parametro, self)
            self.texts[p] = QtGui.QLineEdit(self)
            layout.addWidget(self.labels[p], p, 0)
            layout.addWidget(self.texts[p], p, 1)

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
        if not oldParams:
            return ([''], 1)
        dialog = paramForm(oldParams)
        result = dialog.exec_()
        params = [str(obj.text()) for obj in dialog.texts.values()]
        return (params, result == QDialog.Accepted)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    gui = paramForm()
    gui.show()
    sys.exit(app.exec_())

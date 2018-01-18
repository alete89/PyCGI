#-*- encoding:utf-8 -*-

from PyQt4 import QtGui
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
            self.texts[p] = QtGui.QTextEdit(self)
            layout.addWidget(self.labels[p], p, 0)
            layout.addWidget(self.texts[p], p, 1)

        self.acceptButton = QtGui.QPushButton("Confirmar", self)
        self.acceptButton.clicked.connect(self.confirmarFormulario)

        layout.addWidget(self.acceptButton)
        self.setLayout(layout)
        self.show()

    def confirmarFormulario(self):
        pass


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    gui = paramForm()
    gui.show()
    sys.exit(app.exec_())

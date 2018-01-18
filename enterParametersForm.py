#-*- encoding:utf-8 -*-

from PyQt4 import QtGui
import sys


class enterParametersForm(QtGui.QDialog):
    def __init__(self, params):
        super(enterParametersForm, self).__init__()

        self.table = QtGui.QTableWidget(self)

        self.acceptButton = QtGui.QPushButton("Confirmar", self)
        self.acceptButton.clicked.connect(self.confirmarFormulario)

        self.llenarFormulario(params)
        # Layout
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.acceptButton)
        self.setLayout(layout)
        self.show()

    def llenarFormulario(self, indicaciones):
        for i, indicacion in enumerate(indicaciones):
            filaActual = self.table.rowCount()
            self.table.insertRow(filaActual)  # filaActual o nada?
            self.table.setColumnCount(2)
            item = QtGui.QTableWidgetItem(indicacion.decode('utf8'))
            self.table.setItem(i, 0, item)
        self.show()

    def confirmarFormulario(self):
        pass


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    gui = enterParametersForm()
    gui.show()
    sys.exit(app.exec_())

#-*- encoding:utf-8 -*-

from PyQt4 import QtGui


class enterParametersForm(QtGui.QMainWindow):
    def __init__(self, indicaciones):
        super(enterParametersForm, self).__init__()

        self.table = QtGui.QTableWidget()
        self.llenarFormulario(indicaciones)

        self.acceptButton = QtGui.QPushButton("Confirmar")
        self.acceptButton.clicked.connect(self.confirmarFormulario)

        # Layout
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.acceptButton)
        self.setLayout(layout)

    def llenarFormulario(self, indicaciones):
        for i, indicacion in enumerate(indicaciones):
            filaActual = self.table.rowCount()
            self.table.insertRow(filaActual)  # filaActual o nada?
            self.table.setColumnCount(2)
            item = QtGui.QTableWidgetItem(indicacion.decode('utf8'))
            self.table.setItem(i, 0, item)

    def confirmarFormulario(self):
        pass

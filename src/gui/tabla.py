from PyQt4 import QtGui


class Tabla(QtGui.QTableWidget):
    def __init__(self):
        super(Tabla, self).__init__()
        self.dataset = []
        self.setSortingEnabled(True)

    def ShowDataSet(self, dataset, header=None):
        if header is None:
            header = []
        self.dataset = dataset
        self.setRowCount(0)
        self.setColumnCount(0)
        for rowdata in self.dataset:
            row = self.rowCount()
            self.insertRow(row)
            self.setColumnCount(len(rowdata))
            for column, data in enumerate(rowdata):
                item = QtGui.QTableWidgetItem(data.decode('utf8'))
                self.setItem(row, column, item)
        self.setHorizontalHeaderLabels(header)

    def addRow(self):
        self.insertRow(self.rowCount())

    def getDataSet(self):
        self.updateDataSet()
        return self.dataset

    def updateDataSet(self):
        dataset = []
        for row in range(self.rowCount()):
            rowData = []
            for column in range(self.columnCount()):
                currentItem = self.item(row, column)
                rowData.append(currentItem.text())
            dataset.append(rowData)
        self.dataset = dataset

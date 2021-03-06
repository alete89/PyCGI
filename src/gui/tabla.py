from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QHeaderView


class Tabla(QTableWidget):
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
                item = QTableWidgetItem(data.decode('utf8'))
                self.setItem(row, column, item)
        self.setHorizontalHeaderLabels(header)
        self.horizontalHeader().setResizeMode(QHeaderView.Interactive)

    def addRow(self):
        self.insertRow(self.rowCount())

    def delRow(self):
        self.removeRow(self.currentRow())
        self.setCurrentItem(None)

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

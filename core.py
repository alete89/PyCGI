# -*- coding: utf-8 -*-

# Default
import sys
import os
# Lib
import csvdb
import paramFinder
# GUI
from PyQt4.QtGui import QApplication
from PyQt4 import QtCore
# Forms
import mainWindow
import paramForm
import process


default_path = os.getcwd() + r"/nuevo.csv"


class Core():
    def __init__(self, instanciamw):
        self.mw = instanciamw
        self.proc = process.Process(self.mw)

    def fullDataSet(self, path=default_path):
        return csvdb.getDataFromCsv(path)

    def menuList(self, dataSet):
        distinct = csvdb.distinct(dataSet, 1)
        sortedList = csvdb.sortDataSet(distinct, 1)
        return csvdb.getColumn(sortedList, 1)

    def subMenuList(self, menu, dataSet):
        subMenuFilter = csvdb.dataFilter(dataSet, 1, menu)
        subMenuColumn = csvdb.getColumn(subMenuFilter, 2)
        subMenuSorted = csvdb.sortDataSet(subMenuColumn, 3, True)
        return csvdb.distinct(subMenuSorted, 2)

    def idList(self, menu, dataSet):
        subMenuFilter = csvdb.dataFilter(dataSet, 1, menu)
        return csvdb.getColumn(subMenuFilter, 0)

    def PreEjecutarComandos(self, subMenu):
        secuencia = csvdb.dataFilter(self.fullDataSet(), 2, subMenu)
        ordenada = csvdb.sortDataSet(secuencia, 4)

        cmd, params = paramFinder.findParameters(ordenada)

        newParams, ok = paramForm.paramForm.getNewParams(params)
        loops = csvdb.getColumn(ordenada, 6)

        if ok:
            self.proc.EjecutarComandos(cmd, newParams, loops)


class TerminalX(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        pass
        #self.emit(QtCore.SIGNAL("Activated( QString )"), core.proc.getOutput())


#core = Core()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vp = mainWindow.PyCGI()
    vp.show()
    sys.exit(app.exec_())

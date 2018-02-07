# -*- coding: utf-8 -*-

# Default
import os
# Lib
import csvdb
import paramFinder
import paramForm
import process


default_path = os.getcwd() + r"/tablaDeSecuencias.csv"


def fullDataSet(path=default_path):
    return csvdb.getDataFromCsv(path)


def menuList(dataSet):
    distinct = csvdb.distinct(dataSet, 1)
    sortedList = csvdb.sortDataSet(distinct, 1)
    return csvdb.getColumn(sortedList, 1)


def subMenuList(menu, dataSet):
    subMenuFilter = csvdb.dataFilter(dataSet, 1, menu)
    subMenuColumn = csvdb.getColumn(subMenuFilter, 2)
    subMenuSorted = csvdb.sortDataSet(subMenuColumn, 3, True)
    return csvdb.distinct(subMenuSorted, 2)


def idList(menu, dataSet):
    subMenuFilter = csvdb.dataFilter(dataSet, 1, menu)
    return csvdb.getColumn(subMenuFilter, 0)


def PreEjecutarComandos(subMenu, mw):
    mw.tabs.setCurrentWidget(mw.tab1)
    secuencia = csvdb.dataFilter(fullDataSet(), 2, subMenu)
    ordenada = csvdb.sortDataSet(secuencia, 4)

    cmd, params = paramFinder.findParameters(ordenada)

    newParams, ok = paramForm.paramForm.getNewParams(params)
    loops = csvdb.getColumn(ordenada, 6)
    if ok:
        process.EjecutarComandos(cmd, newParams, loops, mw)


def matarProceso(mw):
    process.killCurrentProcess(mw)


def getHeaders(path=default_path):
    return csvdb.getHeader(path)


def saveTable(table, path=default_path, header=getHeaders()):
    dataset = table.getDataSet()
    csvdb.SaveCSV(path, dataset, header)


if __name__ == '__main__':
    import sys
    import mainWindow
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    vp = mainWindow.PyCGI()
    vp.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

import os
from . import csvdb
from . import paramFinder
from . import process
from ..gui import paramForm

STARTING_PATH = os.getcwd()
CFG_PATH = STARTING_PATH + '/cfg'
TABLA_DE_SECUENCIAS_PATH = STARTING_PATH + r"/tablaDeSecuencias.csv"
process = process.Process()


def getTreeViewInitialPath():
    initial = getValueFromCfg('treeViewInitialPath=')
    if initial == '':
        from PyQt4 import QtCore
        initial = QtCore.QDir.rootPath()
    return initial


def getTreeViewRootPath():
    root = getValueFromCfg('treeViewRootPath=')
    if root == '':
        from PyQt4 import QtCore
        root = QtCore.QDir.rootPath()
    return root


def getValueFromCfg(clave):
    with open(CFG_PATH, 'r') as f:
        text = f.read()
    return text.split(clave)[1].split("\n")[0].replace("'", "").replace('"', '')


def fullDataSet(path=TABLA_DE_SECUENCIAS_PATH):
    return csvdb.getDataFromCsv(path)


def menuList(dataSet):
    distinct = csvdb.distinct(dataSet, 1)
    sortedList = csvdb.sortDataSet(distinct, 1)
    return csvdb.getColumn(sortedList, 1)


def subMenuList(menu, dataSet):
    subMenuFilter = csvdb.dataFilter(dataSet, 1, menu)
    subMenuDistinct = csvdb.distinct(subMenuFilter, 2)
    subMenuColumn = csvdb.getColumn(subMenuDistinct, 2)
    subMenuSorted = csvdb.sortDataSet(subMenuColumn, 0)
    return subMenuSorted


def idList(menu, dataSet):
    subMenuFilter = csvdb.dataFilter(dataSet, 1, menu)
    return csvdb.getColumn(subMenuFilter, 0)


def PreEjecutarComandos(subMenu, mw):
    mw.tabWidget.setCurrentWidget(mw.tabOutputs)
    secuencia = csvdb.dataFilter(fullDataSet(), 2, subMenu)
    ordenada = csvdb.sortDataSet(secuencia, 4)

    cmd, params = paramFinder.findParameters(ordenada)

    newParams, ok = paramForm.paramForm.getNewParams(params)
    loops = csvdb.getColumn(ordenada, 6)
    if ok:
        mw.terminalOutput.append("iniciando secuencia: " + subMenu)
        process.ejecutarSecuencia(cmd, newParams, loops, mw)


def matarProceso(mw):
    process.killCurrentProcess(mw)


def getHeaders(path=TABLA_DE_SECUENCIAS_PATH):
    return csvdb.getHeader(path)


def saveTable(table, path=TABLA_DE_SECUENCIAS_PATH, header=getHeaders()):
    dataset = table.getDataSet()
    csvdb.SaveCSV(path, dataset, header)

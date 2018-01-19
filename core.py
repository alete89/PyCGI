# -*- coding: utf-8 -*-

# import sys
from PyQt4.QtGui import QApplication
import sys
import os
import multiprocessing as mp
from PyQt4 import QtCore
import paramFinder
import csvdb
import mainWindow


lock = mp.Lock()
default_path = os.getcwd() + r"/nuevo.csv"

# Startup


def fullDataSet(path=default_path):
    return csvdb.getDataFromCsv(path)


def menuList(dataSet=fullDataSet()):
    distinct = csvdb.distinct(dataSet, 1)
    sortedList = csvdb.sortDataSet(distinct, 1)
    return csvdb.getColumn(sortedList, 1)


def subMenuList(menu, dataSet=fullDataSet()):
    subMenuFilter = csvdb.dataFilter(dataSet, 1, menu)
    subMenuColumn = csvdb.getColumn(subMenuFilter, 2)
    subMenuSorted = csvdb.sortDataSet(subMenuColumn, 3, True)
    return csvdb.distinct(subMenuSorted, 2)


def idList(menu, dataSet=fullDataSet()):
    subMenuFilter = csvdb.dataFilter(dataSet, 1, menu)
    return csvdb.getColumn(subMenuFilter, 0)

# Processes


def getOutput():
    salida = 'OUT: ' + str(processRun.readAllStandardOutput()).strip()
    error = 'ERR: ' + str(processRun.readAllStandardError()).strip()
    if salida:
        return salida
    else:
        return error


# esto?

processRun = QtCore.QProcess()
processRun.setProcessChannelMode(QtCore.QProcess.MergedChannels)
processRun.setReadChannelMode(QtCore.QProcess.MergedChannels)
processRun.readyRead.connect(getOutput)
# /esto?


class TerminalX(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        self.emit(QtCore.SIGNAL("Activated( QString )"), getOutput)


def PreEjecutarComandos(subMenu):
    print 'Seleccionado: ' + str(subMenu)
    secuencia = csvdb.dataFilter(fullDataSet(), 2, subMenu)
    ordenada = csvdb.sortDataSet(secuencia, 4)
    return paramFinder.findParameters(ordenada)


def EjecutarComandos():

    LoopDeProceso = [int(r) for r in LoopDeProceso]

    for OrdenDeSecuenciaTemp in OrdenDeSecuencia:

        Loop = LoopDeProceso[i] + 1

        for LoopDeProcesoTemp in range(Loop):

            ComandoDeSistemaTemp = ComandoDeSistema[i]
            ModuloPythonTemp = ModuloPython[i]

            if ComandoDeSistemaTemp:
                try:

                    cmd = str(ComandoDeSistemaTemp)
                    self.processRun.waitForFinished()
                    lock.acquire()
                    self.terminalDeProceso.append('>>> PROC ' + str(OrdenDeSecuenciaTemp)
                                                  + ': ' +
                                                  str(ComandoDeSistemaTemp) +
                                                  ' - LOOP:'
                                                    + str(LoopDeProcesoTemp))

                    self.terminalDeTexto.append(
                        '>>> PROC ' + str(OrdenDeSecuenciaTemp) + ':')
                    self.processRun.start(cmd)
                    self.connect(self.TermX, QtCore.SIGNAL(
                        "Activated ( QString ) "), self.dataReady)

                    lock.release()

                    QtCore.QCoreApplication.processEvents()

                except:

                    self.terminalDeProceso.append('>>> ERROR en el proceso '
                                                  + str(OrdenDeSecuenciaTemp) + ': '
                                                  + str(ComandoDeSistemaTemp) + ' - LOOP:'
                                                  + str(LoopDeProcesoTemp))

                    self.terminalDeTexto.append(
                        '>>> PROC: ' + str(ComandoDeSistemaTemp) + '\n')
                    break

        i = i + 1


def mainLoop():
    app = QApplication(sys.argv)
    vp = mainWindow.PyCGI()
    vp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    mainLoop()

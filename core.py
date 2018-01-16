# -*- coding: utf-8 -*-

# import sys
import os
import multiprocessing as mp
from PyQt4 import QtCore
import paramFinder
import csvdb
import re
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
    return csvdb.sortDataSet(subMenuColumn,3)


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


def PreEjecutarComandos(idFila):
    #global lock
    # Hasta aca lo unico que hice fue agarrar todos los datos de un
    # proceso y cargarlos en una nueva tabla de secuencias pero temporal
    # Ahora tengo que tomar todos los strings que contiene indicaciones
    # entre del tipo '(tipee su comando)' y armar con todos ellos un formulario

    # acá había un ciclo y un if ComandoDeSistemaTem:
    # entiendo que agregaba a la tabladesecuenciatemp sólo lo que tenía un comando escrito
    # ¿lo hacía para evitar un error más adelante? hace falta?

    print 'idFila: ' + str(idFila)
    secuencia = csvdb.dataFilter(fullDataSet(),0,idFila)
    paramFinder.findParameters(idFila, secuencia)


def EjecutarComandos():
    # global lock

    idFilaTemp = ''
    query = QtSql.QSqlQuery()  # reemplazar por CSV
    query.exec_("SELECT DISTINCT Coordenada FROM TablaDeSecuenciasTemp")

    while(query.next()):
        idFilaTemp = query.value(0).toString()

    ModuloPython = []
    ComandoDeSistema = []
    OrdenDeSecuencia = []
    LoopDeProceso = []

    query.exec_("SELECT ModuloPython,ComandoDeSistema,OrdenDeSecuencia,LoopDeProceso FROM TablaDeSecuenciasTemp where Coordenada='" +
                str(idFilaTemp) + "' ORDER BY OrdenDeSecuencia")

    while(query.next()):

        ModuloPythonTemp = query.value(0).toString()
        ComandoDeSistemaTemp = query.value(1).toString()
        OrdenDeSecuenciaTemp = query.value(2).toString()
        LoopDeProcesoTemp = query.value(3).toString()

        ModuloPython.append(ModuloPythonTemp)
        ComandoDeSistema.append(ComandoDeSistemaTemp)
        OrdenDeSecuencia.append(OrdenDeSecuenciaTemp)
        LoopDeProceso.append(LoopDeProcesoTemp)

    i = 0

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



if __name__ == '__main__':
    mainWindow.mainLoop()
# -*- coding: utf-8 -*-

# Default
import sys
import os
import multiprocessing as mp
# GUI
from PyQt4.QtGui import QApplication
from PyQt4 import QtCore
# Forms
import mainWindow
import core


lock = mp.Lock()


class Process():
    def __init__(self):
        self.processRun = QtCore.QProcess()

    def EjecutarComandos(self, comando, parametros, iteraciones):
        self.processRun.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.processRun.setReadChannelMode(QtCore.QProcess.MergedChannels)
        self.processRun.readyRead.connect(self.getOutput)

        # DEBUG
        print comando, parametros, iteraciones
        return

        for iteracion in enumerate(iteraciones):
            try:
                self.processRun.waitForFinished()
                lock.acquire()
                terminalDeProceso.append(
                    '>>> PROC ' + str(comando) + ' - LOOP:' + str(iteracion))
                terminalDeTexto.append(
                    '>>> PROC ' + str(OrdenDeSecuenciaTemp) + ':')
                processRun.start(cmd)
                connect(self.TermX, QtCore.SIGNAL(
                    "Activated ( QString ) "), self.dataReady)
                lock.release()
                QtCore.QCoreApplication.processEvents()
            except:
                self.terminalDeProceso.append('>>> ERROR en el proceso '
                                              + str(OrdenDeSecuenciaTemp) + ': '
                                              + str(ComandoDeSistemaTemp) +
                                              ' - LOOP:'
                                              + str(LoopDeProcesoTemp))
                self.terminalDeTexto.append(
                    '>>> PROC: ' + str(ComandoDeSistemaTemp) + '\n')

    def getOutput(self):
        salida = 'OUT: ' + str(self.processRun.readAllStandardOutput()).strip()
        error = 'ERR: ' + str(self.processRun.readAllStandardError()).strip()
        if salida:
            return salida
        else:
            return error

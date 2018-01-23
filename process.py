# -*- coding: utf-8 -*-

# Default
import multiprocessing as mp
# GUI
from PyQt4 import QtCore
# Forms


lock = mp.Lock()


class Process():
    def __init__(self, instanciamw):
        self.mainWindow = instanciamw
        self.processRun = QtCore.QProcess()
        # El canal stdout y stderr juntos
        self.processRun.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.processRun.setReadChannelMode(QtCore.QProcess.MergedChannels)
        # Slot cuando haya algo para leer
        self.processRun.readyRead.connect(self.getOutput)

    def EjecutarComandos(self, comandos, parametros, iteraciones):
        for c, comando in enumerate(comandos):
            parametro = parametros[c]
            iteracion = iteraciones[c]
            for _ in range(int(iteracion)):
                print comando, parametro
                self.processRun.waitForFinished()
                # o mandarle el string? '>>> PROC ' + str(comando) + ' - LOOP:' + str(it)
                self.processRun.start(comando, [parametro])
                #self.processRun.start([comando, parametro])
                QtCore.QCoreApplication.processEvents()

    def getOutput(self):
        salida = 'OUT: ' + str(self.processRun.readAllStandardOutput()).strip()
        error = 'ERR: ' + str(self.processRun.readAllStandardError()).strip()
        if salida:
            self.mainWindow.showOutputInTerminal(salida)
        else:
            self.mainWindow.showOutputInTerminal(error)

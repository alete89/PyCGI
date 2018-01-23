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
        self.process = QtCore.QProcess()
        self.lista = []
        # El canal stdout y stderr juntos
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.setReadChannelMode(QtCore.QProcess.MergedChannels)
        self.process.finished.connect(self.runNow)
        self.process.readyRead.connect(self.hayParaEscribir)

    def EjecutarComandos(self, comandos, parametros, iteraciones):
        self.lista = map(list, zip(comandos, parametros, iteraciones))
        self.runNow()

    def runNow(self):
        if (len(self.lista) == 0):
            return
        sublist = self.lista[0]
        if int(sublist[2]) == 0:
            del self.lista[0]
            self.runNow()
        else:
            sublist[2] = str(int(sublist[2]) - 1)
            self.process.start(sublist[0], [sublist[1]])

    def hayParaEscribir(self):
        self.mainWindow.showOutputInTerminal(self.process.readAll().data())

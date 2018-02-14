# -*- coding: utf-8 -*-

# Default
import sys
from PyQt4 import QtCore

if sys.platform == "win32":
    # Windows only
    from winstructs import WinProcInfo
    import ctypes


class Process():
    def __init__(self):
        self.proc = QtCore.QProcess()
        self.proc.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.proc.setReadChannelMode(QtCore.QProcess.MergedChannels)
        self.proc.finished.connect(self.processJustFinished)
        self.proc.readyRead.connect(self.hayParaEscribir)

        self.secuencia = []
        self.MainWindowInstance = None
        self.current_process = ""

    def ejecutarSecuencia(self, comandos, parametros, iteraciones, mw):
        self.MainWindowInstance = mw
        self.secuencia = map(list, zip(comandos, parametros, iteraciones))
        self.runNow()

    def runNow(self):
        if not self.secuencia:
            return
        instruccion = self.secuencia[0]
        if int(instruccion[2]) == 0:  # Iteraciones restantes
            # Si no hay más iteraciones, la saco de la lista.
            del self.secuencia[0]
            self.runNow()
        else:  # Quedan iteraciones
            instruccion[2] = str(int(instruccion[2]) - 1)  # Iteraciones -1
            self.current_process = instruccion[0]
            self.MainWindowInstance.showOutputInTerminal(
                "iniciando proceso: " + self.current_process)
            if not instruccion[1]:  # Si no hay parámetros
                self.proc.start(instruccion[0])  # lanzo sin parámetros
            else:
                # lanzo con parámetros
                self.proc.start(instruccion[0], instruccion[1])

    def hayParaEscribir(self):
        output = self.proc.readAll().data()
        self.MainWindowInstance.showOutputInTerminal(output)

    def getPid(self):
        try:
            if sys.platform == 'win32':
                LPWinProcInfo = ctypes.POINTER(WinProcInfo)
                struct = ctypes.cast(int(self.proc.pid()), LPWinProcInfo)
                pid = struct.contents.dwProcessID
            else:
                pid = int(self.proc.pid())
            return pid
        except TypeError:
            return "No hay proceso corriendo"

    def killCurrentProcess(self, mw):
        mw.showOutputInTerminal(str(self.getPid()))
        self.proc.kill()

    def processJustFinished(self):
        self.MainWindowInstance.showOutputInTerminal(
            "fin de proceso: " + self.current_process)
        self.runNow()

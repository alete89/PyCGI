# -*- coding: utf-8 -*-

# Default
import multiprocessing as mp
import sys
# no entiendo por qué no funciona importando ctypes directamente.
import ctypes.wintypes
# GUI
from PyQt4 import QtCore
# Forms


lock = mp.Lock()


class Process():
    def __init__(self, instanciamw):
        self.mainWindow = instanciamw  # La instancia de la ventana actual
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
            if not sublist[1]:
                self.process.start(sublist[0])
            else:
                self.process.start(sublist[0], [sublist[1]])

    def hayParaEscribir(self):
        self.mainWindow.showOutputInTerminal(self.process.readAll().data())

    def getPid(self):
        if sys.platform == 'win32':
            LPWinProcInfo = ctypes.POINTER(WinProcInfo)
            struct = ctypes.cast(int(self.process.pid()), LPWinProcInfo)
            pid = struct.contents.dwProcessID
        else:
            pid = int(self.process.pid())
        return pid

    def killCurrentProcess(self):
        self.mainWindow.showOutputInTerminal(str(self.getPid()))
        self.process.kill()


# windows only:
class WinProcInfo(ctypes.Structure):
    _fields_ = [
        ('hProcess', ctypes.wintypes.HANDLE),
        ('hThread', ctypes.wintypes.HANDLE),
        ('dwProcessID', ctypes.wintypes.DWORD),
        ('dwThreadID', ctypes.wintypes.DWORD),
    ]

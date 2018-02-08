# -*- coding: utf-8 -*-

# Default
import sys
# no entiendo por qué no funciona importando ctypes directamente.
# Windows Only:
if sys.platform == "win32":
    from winstructs import WinProcInfo
    import ctypes
# GUI
import PyQt4.QtCore


class Process():
    def __init__(self):
        self.proc = PyQt4.QtCore.QProcess()
        self.proc.setProcessChannelMode(PyQt4.QtCore.QProcess.MergedChannels)
        self.proc.setReadChannelMode(PyQt4.QtCore.QProcess.MergedChannels)
        self.proc.finished.connect(self.processJustFinished)
        self.proc.readyRead.connect(self.hayParaEscribir)

        self.lista = []
        self.MainWindowInstance = None
        self.current_process = ""

    def EjecutarComandos(self, comandos, parametros, iteraciones, mw):
        self.MainWindowInstance = mw
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
            self.current_process = sublist[0]
            self.MainWindowInstance.showOutputInTerminal(
                "iniciando proceso: " + self.current_process)
            if not sublist[1]:
                self.proc.start(sublist[0])
            else:
                self.proc.start(sublist[0], sublist[1])

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
        except UserWarning:
            pass  # VER

    def killCurrentProcess(self, mw):
        mw.showOutputInTerminal(str(self.getPid()))
        self.proc.kill()

    def processJustFinished(self):
        self.MainWindowInstance.showOutputInTerminal(
            "fin de proceso: " + self.current_process)
        self.runNow()

# -*- coding: utf-8 -*-

# Default
import sys
# no entiendo por qué no funciona importando ctypes directamente.
import ctypes.wintypes
# GUI
import PyQt4.QtCore


nProcess = PyQt4.QtCore.QProcess()
lista = []
WINDOW_INSTANCE = None


def EjecutarComandos(comandos, parametros, iteraciones, mw):
    global lista
    global WINDOW_INSTANCE
    WINDOW_INSTANCE = mw
    lista = map(list, zip(comandos, parametros, iteraciones))
    runNow()


def runNow():
    if (len(lista) == 0):
        return
    sublist = lista[0]
    if int(sublist[2]) == 0:
        del lista[0]
        runNow()
    else:
        sublist[2] = str(int(sublist[2]) - 1)
        if not sublist[1]:
            nProcess.start(sublist[0])
        else:
            nProcess.start(sublist[0], sublist[1])


def hayParaEscribir():
    WINDOW_INSTANCE.showOutputInTerminal(nProcess.readAll().data())


def getPid():
    try:
        if sys.platform == 'win32':
            LPWinProcInfo = ctypes.POINTER(WinProcInfo)
            struct = ctypes.cast(int(nProcess.pid()), LPWinProcInfo)
            pid = struct.contents.dwProcessID
        else:
            pid = int(nProcess.pid())
        return pid
    except UserWarning:
        pass


def killCurrentProcess(mw):
    mw.showOutputInTerminal(str(getPid()))
    nProcess.kill()


nProcess.setProcessChannelMode(PyQt4.QtCore.QProcess.MergedChannels)
nProcess.setReadChannelMode(PyQt4.QtCore.QProcess.MergedChannels)
nProcess.finished.connect(runNow)
nProcess.readyRead.connect(hayParaEscribir)


class WinProcInfo(ctypes.Structure):
    '''windows only'''
    _fields_ = [
        ('hProcess', ctypes.wintypes.HANDLE),
        ('hThread', ctypes.wintypes.HANDLE),
        ('dwProcessID', ctypes.wintypes.DWORD),
        ('dwThreadID', ctypes.wintypes.DWORD),
    ]

# -*- coding: utf-8 -*-

# Default
import sys
from PyQt4 import QtCore
import os

if sys.platform == "win32":
    # Windows only
    from .winstructs import WinProcInfo
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

    def ejecutarSecuencia(self, comandos, iteraciones, mw):
        self.MainWindowInstance = mw
        for i, _ in enumerate(comandos):
            instruccion = dict(comando=comandos[i], iteraciones=iteraciones[i])
            # instruccion["parametro"] = [x for x in instruccion["parametro"]
            #                             if x.strip()]  # Elimino parámetros vacíos
            self.secuencia.append(instruccion)
        self.secuenciaList(mw)
        self.runNow()

    def runNow(self):
        filePathExists = True
        if not self.secuencia:
            return
        instruccion = self.secuencia[0]
        if int(instruccion['iteraciones']) == 0:  # Iteraciones restantes
            # Si no hay más iteraciones, la saco de la lista.
            del self.secuencia[0]
            self.runNow()
        else:  # Quedan iteraciones
            instruccion['iteraciones'] = str(int(instruccion['iteraciones']) - 1)  # Iteraciones -1
            self.current_process = instruccion['comando']
            if self.current_process[:6] == "python":
                soloRuta = self.current_process.split(
                    "python ")[1][:self.current_process.split("python ")[1].rfind("/") + 1]
                rutaAbsoluta = os.path.abspath(soloRuta) + "/"
                self.proc.setWorkingDirectory(rutaAbsoluta)
                self.current_process = self.current_process.replace(soloRuta, rutaAbsoluta)
                filePath = self.current_process.replace("python ", "")
                filePathExists = os.path.isfile(filePath)
            if filePathExists:
                self.MainWindowInstance.showOutputInTerminal(
                    "iniciando proceso: " + instruccion["comando"])
                # if not instruccion['parametro']:  # Si no hay parámetros
                self.proc.start(self.current_process)  # lanzo sin parámetros
                # else:  # ya no hay parámetros
                # lanzo con parámetros
                #   parametros = " ".join(instruccion['parametro'])
                #  self.proc.start(self.current_process + " " + parametros)
            else:
                print "no se encontro el archivo"

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

    def secuenciaList(self, window_instance):
        window_instance.indicadorSecuencia.clear()
        secuencia = self.secuencia
        for instruccion in secuencia:
            printable_instruccion = str(
                instruccion["comando"]) + " (" + str(instruccion["iteraciones"]) + ")"

            bold_instruccion = "<html><b>" + printable_instruccion + "</b></html>"
            prev_content = str(window_instance.indicadorSecuencia.document().toPlainText()).replace(
                "<html><b>", "")
            window_instance.indicadorSecuencia.setFontWeight(50)
            window_instance.indicadorSecuencia.append(prev_content)
            window_instance.indicadorSecuencia.append(bold_instruccion)

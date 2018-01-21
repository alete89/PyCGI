# -*- coding: utf-8 -*-

# Default
import multiprocessing as mp
# GUI
from PyQt4 import QtCore
# Forms


lock = mp.Lock()


class Process():
    def __init__(self):
        self.processRun = QtCore.QProcess()
        # El canal stdout y stderr juntos
        self.processRun.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.processRun.setReadChannelMode(QtCore.QProcess.MergedChannels)
        # Slot cuando haya algo para leer
        self.processRun.readyRead.connect(self.getOutput)

    def EjecutarComandos(self, comandos, parametros, iteraciones, instanciaVentanaPrincipal):
        for c, comando in enumerate(comandos):
            parametro = parametros[c]
            iteracion = iteraciones[c]
            for _ in range(int(iteracion)):
                print comando, parametro
                self.processRun.waitForFinished()
                # o mandarle el string? '>>> PROC ' + str(comando) + ' - LOOP:' + str(it)
                instanciaVentanaPrincipal.showOutputInTerminal()

        return

        '''
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
'''

    def getOutput(self):
        salida = 'OUT: ' + str(self.processRun.readAllStandardOutput()).strip()
        error = 'ERR: ' + str(self.processRun.readAllStandardError()).strip()
        if salida:
            return salida
        else:
            return error

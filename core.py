# -*- coding: utf-8 -*-

import sys
import os
import multiprocessing as mp
from stringFinderV2 import *
import csvdb

lock = mp.Lock()
default_path = os.getcwd() + r"/rs.csv"

# Startup
def fullDataSet(path=default_path):
    return csvdb.getDataFromCsv(path)

def menuList(dataSet=fullDataSet()):
    distinct = csvdb.distinct(dataSet,1)
    sortedList = csvdb.sortDataSet(distinct,4)
    return csvdb.getColumn(sortedList,1)


# Processes
def getOutput():
    salida='OUT: '+str(processRun.readAllStandardOutput()).strip()
    error='ERR: '+str(processRun.readAllStandardError()).strip()
    if salida:
        return salida
    else:
        return error

processRun = QtCore.QProcess()
processRun.setProcessChannelMode(QtCore.QProcess.MergedChannels)
processRun.setReadChannelMode(QtCore.QProcess.MergedChannels)        
processRun.readyRead.connect(getOutput)


class TerminalX(QtCore.QThread):
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)
          
    def run(self):
        self.emit(QtCore.SIGNAL("Activated( QString )"), self.getOutput)
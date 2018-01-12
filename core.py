# -*- coding: utf-8 -*-

import sys
import os
import multiprocessing as mp
import paramFinder
import csvdb
import re

lock = mp.Lock()
default_path = os.getcwd() + r"/rs.csv"

# Startup
def fullDataSet(path=default_path):
    return csvdb.getDataFromCsv(path)

def menuList(dataSet=fullDataSet()):
    distinct = csvdb.distinct(dataSet,1)
    sortedList = csvdb.sortDataSet(distinct,4)
    return csvdb.getColumn(sortedList,1)

def subMenuList(menu, dataSet=fullDataSet()):
    subMenuFilter = csvdb.dataFilter(dataSet,1,menu)
    return csvdb.getColumn(subMenuFilter,2)

def idList(menu, dataSet=fullDataSet()):
    subMenuFilter = csvdb.dataFilter(dataSet,1,menu)
    return csvdb.getColumn(subMenuFilter,0)

# Processes
def getOutput():
    salida='OUT: '+str(processRun.readAllStandardOutput()).strip()
    error='ERR: '+str(processRun.readAllStandardError()).strip()
    if salida:
        return salida
    else:
        return error

# esto?
processRun = QtCore.QProcess()
processRun.setProcessChannelMode(QtCore.QProcess.MergedChannels)
processRun.setReadChannelMode(QtCore.QProcess.MergedChannels)        
processRun.readyRead.connect(getOutput)
# /esto?

class TerminalX(QtCore.QThread):
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)
          
    def run(self):
        self.emit(QtCore.SIGNAL("Activated( QString )"), self.getOutput)

def PreEjecutarComandos(idFila):
    #global lock
    # Hasta aca lo unico que hice fue agarrar todos los datos de un 
    # proceso y cargarlos en una nueva tabla de secuencias pero temporal    
    # Ahora tengo que tomar todos los strings que contiene indicaciones 
    # entre del tipo '(tipee su comando)' y armar con todos ellos un formulario
    
    # acá había un ciclo y un if ComandoDeSistemaTem:
    # entiendo que agregaba a la tabladesecuenciatemp sólo lo que tenía un comando escrito 
    # ¿lo hacía para evitar un error más adelante? hace falta?
    
    print 'idFila: ' + str(idFila)
    findParameters(idFila,)

def findParameters(idfila, dataset):
    for comando in csvdb.getColumn(dataset,6):
        parentesisList = re.findall('\(.*?\)',comando)
        for char in parentesisList:
            char.replace(')','')
            char.replace('(','')
            # query.exec_("INSERT INTO Formulario (id, Menu, SubMenu, Command, Value) VALUES ('"+str(idCampoTemp)+"', '"+str(MenuTemp)+"','"+str(SubMenuTemp)+"','"+str(j)+"','');")
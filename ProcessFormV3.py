# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 11:23:29 2017
@author: manuel
"""
import sys
from PyQt4 import QtCore, QtGui, QtSql
import re
import string


class ProcessFormV3(QtGui.QDialog):
    
    def __init__(self,idFilaTemp):
        
        super(ProcessFormV3, self).__init__()
#        Tabla=sys.argv[1] # Tomo el valor de la linea de comandos

        Tabla="Formulario" #VariablesGlobales
        
#        with open('db', 'r') as f:
#            data = f.read()

        db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        db.setHostName('localhost')
        db.setDatabaseName('PyCGI')
        db.setUserName('root')
        db.setPassword('23101log') # esto no funciona con la variable 'data' ni con str(data)
#        db.setPort(3306)
        db.open()
        
        model = QtSql.QSqlTableModel()
        delrow = -1

        self.initializeModel(model, Tabla)
        
        view1 =self.createView("PyCGI - Configuracion de la Tabla " + str(Tabla), model)
        
        view1.clicked.connect(self.findrow)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(view1)
        
#        layoutH = QtGui.QHBoxLayout()
        
        btn1 = QtGui.QPushButton("Config process")
        btn1.clicked.connect(lambda: self.stringCompleto(idFilaTemp))
        layout.addWidget(btn1)
        
#        layout.addLayout(layoutH)
        
        self.setLayout(layout)
        self.setWindowTitle("PyCGI - Configuracion de la Tabla " + str(Tabla))
        self.show()
    
    def stringCompleto(self,idFilaTemp):
        
        query = QtSql.QSqlQuery()
        query.exec_("SELECT DISTINCT id FROM Formulario ORDER BY id;")
        idCampoForm=[]

        while(query.next()):
            idCampoFormTemp=query.value(0).toString()
            idCampoForm.append(idCampoFormTemp)

        for idCampoFormTemp in idCampoForm:
            query.exec_("SELECT ComandoDeSistema FROM TablaDeSecuencias WHERE id='"+str(idCampoFormTemp)+"';")

            
            while(query.next()):
                ComandoDeSistemaTemp=query.value(0).toString()

            query.exec_("SELECT Value FROM Formulario WHERE id='"+str(idCampoFormTemp)+"';")
            ValueForm=[]
    
            while(query.next()):
                ValueFormTemp=query.value(0).toString()
                ValueForm.append(ValueFormTemp)                        
      
            a=0   
            p=re.findall('\(.*?\)',ComandoDeSistemaTemp)  
            
            for i in p:
                ComandoDeSistemaTemp = string.replace(ComandoDeSistemaTemp, i, str(ValueForm[a]))
                a=a+1

            query.exec_("UPDATE TablaDeSecuenciasTemp SET ComandoDeSistema='"+str(ComandoDeSistemaTemp)+"' WHERE id='"+str(idCampoFormTemp)+"';")
            
            print ComandoDeSistemaTemp
            print 'idFilaTemp vale v3:'+str(idFilaTemp)

#        self.close()
        
        
    def initializeModel(self, model, Tabla):

#        print Tabla
#        with open('db', 'r') as f:
#            data = f.read()
        
        Campos=[]
#        db = MySQLdb.connect(host   ="localhost",   # host
#                             user   ="root",        # nombre de usuario
#                             passwd = "23101log",    # password
#                             db     ="PyCGI")       # Nombre de la base de datos     
#        cur = db.cursor()
#        cur.execute("show columns from " + str(Tabla))
#        db.commit()
        query = QtSql.QSqlQuery()
        
        query.exec_("show columns from " + str(Tabla))
        while(query.next()):  
            CamposTemp=query.value(0).toString()
            Campos.append(CamposTemp)
    #        print("Campo: "+ str(CamposTemp))
#        db.close()    
        
        model.setTable(Tabla)
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        model.select()
        j=0
        
        for CamposTemp in Campos:
            CampoTitulo = QtGui.QLabel(str(CamposTemp))
            model.setHeaderData(j, QtCore.Qt.Horizontal, str(CamposTemp))
            
            j=j+1
    	
    def createView(self, title, model):
        view = QtGui.QTableView()
        view.setModel(model)
        view.setWindowTitle(title)
        view.setMinimumHeight(250)
        view.setMinimumWidth(900)
        view.verticalScrollBar()
        view.resizeColumnsToContents()
        view.setSortingEnabled(True)
        return view
    	  	
    def findrow(self,i):
        delrow = i.row()    

if __name__ == '__main__':
    
    global Tabla
    global stringFinderV2
    app = QtGui.QApplication(sys.argv)
    foo=ProcessFormV3()
    foo.show()
    sys.exit(app.exec_())
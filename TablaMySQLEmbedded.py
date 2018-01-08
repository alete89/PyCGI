# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 11:23:29 2017
@author: manuel
"""
import sys
from PyQt4 import QtCore, QtGui, QtSql

class TablaMySQLEmbedded(QtGui.QDialog):
    
    def __init__(self):
        
        super(TablaMySQLEmbedded, self).__init__()
#        Tabla=sys.argv[1] # Tomo el valor de la linea de comandos

        Tabla="TablaDeSecuencias" #VariablesGlobales
        
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
        
        view1 =self.createView("PyCGI - Configuracion de la Tabla "+str(Tabla), model)
        view1.clicked.connect(self.findrow)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(view1)
        
        layoutH = QtGui.QHBoxLayout()
        
        btn0 = QtGui.QPushButton("Add a row")
        btn0.clicked.connect(lambda: model.insertRows(model.rowCount(), 1))
        layoutH.addWidget(btn0)
        	
        btn1 = QtGui.QPushButton("Del a row")
        btn1.clicked.connect(lambda: model.removeRow(view1.currentIndex().row()))
        layoutH.addWidget(btn1)
    
        layout.addLayout(layoutH)
        
        self.setLayout(layout)
        self.setWindowTitle("PyCGI - Configuracion de la Tabla "+str(Tabla))
        self.show()
       
        
    def initializeModel(self, model, Tabla):
        
#        print Tabla
#        with open('db', 'r') as f:
#            data = f.read()
        
        Campos=[]

        query = QtSql.QSqlQuery()
        
        query.exec_("show columns from " + str(Tabla))
        while(query.next()):  
            CamposTemp=query.value(0).toString()
            Campos.append(CamposTemp)
        
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
        view.setMinimumHeight(150)
        view.setMinimumWidth(300)
        view.verticalScrollBar()
        view.resizeColumnsToContents()
        view.setSortingEnabled(True)
        return view
   	
    def findrow(self,i):
        delrow = i.row()    
 
if __name__ == '__main__':
    
    global Tabla
    
    app = QtGui.QApplication(sys.argv)
    foo=TablaMySQLEmbedded()
    foo.show()
    sys.exit(app.exec_())
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 10:42:18 2017

@author: manuel
"""
import re
import string
from ProcessForm import *


class stringFinder(QtGui.QMainWindow):
    
    def __init__(self,cmd):
        
        super(stringFinder, self).__init__()

        db1 = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        db1.setHostName('localhost')
        db1.setDatabaseName('PyCGI')
        db1.setUserName('root')
        db1.setPassword('23101log')
        db1.open()
        
#        cmd = 'python (archivo1) par (archivo2) par1 (archivo3) par2 (archivo4) par3 par4 (archivo5) (archivo6)'
        #print cmd
        
        p=re.findall('\(.*?\)',cmd)
        
        query = QtSql.QSqlQuery()
        query.exec_("TRUNCATE TABLE Formulario;")
        
        query = QtSql.QSqlQuery()
        for i in p:
            query.exec_("INSERT INTO Formulario (id, Coordenada, Command, Value) VALUES ('', '','"+str(i)+"','');")
            
        db1.close()
        
        widget_central = QtGui.QWidget(self)
        self.setCentralWidget(widget_central)  
        
        layout = QtGui.QVBoxLayout(widget_central)
        self.form=ProcessForm(cmd)
        
        layout.addWidget(self.form)
        self.show()

if __name__ == '__main__':
    
    global Tabla
    
    app = QtGui.QApplication(sys.argv)
    foo=stringFinder()
    foo.show()
    sys.exit(app.exec_())
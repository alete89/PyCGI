# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 10:42:18 2017

@author: manuel
"""
import re
from ProcessFormV3 import *


class stringFinderV2(QtGui.QWidget):
    
    def __init__(self,idFilaTemp):
        
        super(stringFinderV2, self).__init__()

        db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        db.setHostName('localhost')
        db.setDatabaseName('PyCGI')
        db.setUserName('root')
        db.setPassword('23101log')
        db.open()
        
        query = QtSql.QSqlQuery()
        query.exec_("SELECT id, Menu, SubMenu, ComandoDeSistema FROM TablaDeSecuenciasTemp;")
        
        idCampo=[]
        Menu=[]
        SubMenu=[]        
        ComandoDeSistema=[]
#        Coordenada=[]
        
        while(query.next()):
            
            idCampoTemp=query.value(0).toString()            
            MenuTemp=query.value(1).toString()            
            SubMenuTemp=query.value(2).toString()            
            ComandoDeSistemaTemp=query.value(3).toString()
            
            idCampo.append(idCampoTemp)
            Menu.append(MenuTemp)
            SubMenu.append(SubMenuTemp)
            ComandoDeSistema.append(ComandoDeSistemaTemp)

        query.exec_("TRUNCATE TABLE Formulario;")
       
        i=0
        
        for cmd in ComandoDeSistema:
            
            p=re.findall('\(.*?\)',cmd)
            
            idCampoTemp=idCampo[i]
            MenuTemp=Menu[i]
            SubMenuTemp=SubMenu[i]
            
           
            for j in p:
                j=j.replace(')','')
                j=j.replace('(','')
                query.exec_("INSERT INTO Formulario (id, Menu, SubMenu, Command, Value) VALUES ('"+str(idCampoTemp)+"', '"+str(MenuTemp)+"','"+str(SubMenuTemp)+"','"+str(j)+"','');")
            i=i+1
            
        widgetFormulario = QtGui.QWidget(self)
        widgetFormulario.setGeometry(5,5,900,250)
        
        layout = QtGui.QVBoxLayout(widgetFormulario)
        
        print 'idFilaTemp vale: '+str(idFilaTemp)
        self.form=ProcessFormV3(idFilaTemp)
        
        layout.addWidget(self.form)
        self.show()
        
        
if __name__ == '__main__':
    
    global Tabla
    
    app = QtGui.QApplication(sys.argv)
    foo=stringFinderV2()
    foo.show()
    sys.exit(app.exec_())
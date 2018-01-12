# -*- coding: utf-8 -*-

import re
from ProcessFormV3 import *
import csvdb

def findParameters(idfila, dataset):
    for comando in csvdb.getColumn(dataset,6):
        parentesisList = re.findall('\(.*?\)',comando)
        for char in parentesisList:
            char.replace(')','')
            char.replace('(','')
            # query.exec_("INSERT INTO Formulario (id, Menu, SubMenu, Command, Value) VALUES ('"+str(idCampoTemp)+"', '"+str(MenuTemp)+"','"+str(SubMenuTemp)+"','"+str(j)+"','');")
            
# ESTO ES TODO GUI VER DÓNDE LO METEMOS:
#widgetFormulario = QtGui.QWidget(self)
#widgetFormulario.setGeometry(5,5,900,250)
#layout = QtGui.QVBoxLayout(widgetFormulario)
#print 'idFilaTemp vale: '+str(idFilaTemp)
#self.form=ProcessFormV3(idFilaTemp)
#layout.addWidget(self.form)
#self.show()
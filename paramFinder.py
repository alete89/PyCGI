# -*- coding: utf-8 -*-

import re
#import ProcessFormV3
import csvdb


def findParameters(dataset):
    for comando in csvdb.getColumn(dataset, 5):
        print comando  # Debug
        parentesisList = re.findall('(.*?)', comando)
        for char in parentesisList:
            char.replace(')', '')
            char.replace('(', '')
            # query.exec_("INSERT INTO Formulario (id, Menu, SubMenu, Command, Value) VALUES ('"+str(idCampoTemp)+"', '"+str(MenuTemp)+"','"+str(SubMenuTemp)+"','"+str(j)+"','');")

# ESTO ES todo GUI VER DÓNDE LO METEMOS:
#widgetFormulario = QtGui.QWidget(self)
# widgetFormulario.setGeometry(5,5,900,250)
#layout = QtGui.QVBoxLayout(widgetFormulario)
# print 'idFilaTemp vale: '+str(idFilaTemp)
# self.form=ProcessFormV3(idFilaTemp)
# layout.addWidget(self.form)
# self.show()

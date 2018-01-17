# -*- coding: utf-8 -*-

import re
#import ProcessFormV3
import csvdb
import enterParametersForm


def findParameters(dataset):
    parametro = None
    parametros = []
    for comando in csvdb.getColumn(dataset, 5):
        print "antes: " + comando  # Debug
        indicacionParametros = re.findall('\(.*?\)', comando)
        for parametro in indicacionParametros:
            parametro = parametro.replace("(", "")
            parametro = parametro.replace(")", "")
        if parametro:
            parametros.append(parametro)
    if len(parametros):
        enterParametersForm.enterParametersForm(parametros)


# ESTO ES todo GUI VER DÓNDE LO METEMOS:
#widgetFormulario = QtGui.QWidget(self)
# widgetFormulario.setGeometry(5,5,900,250)
#layout = QtGui.QVBoxLayout(widgetFormulario)
# print 'idFilaTemp vale: '+str(idFilaTemp)
# self.form=ProcessFormV3(idFilaTemp)
# layout.addWidget(self.form)
# self.show()

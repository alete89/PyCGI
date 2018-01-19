# -*- coding: utf-8 -*-

import re
# import ProcessFormV3
import csvdb


def findParameters(dataset):
    # dataset = [['6', 'ver', 'ping', '2', '1', 'ping (ingrese un sitio)', '1'], [
    #    '3', 'ver', 'ping', '1', '2', 'ping (ingrese una IP)', '1']]
    parametro = None
    lista_de_parametros = []
    lista_de_comandos = []
    for comando_completo in csvdb.getColumn(dataset, 5):
        parentesis_index = comando_completo.find("(")
        if parentesis_index >= 1:
            cmd_solo = comando_completo[0: parentesis_index - 1]
        else:
            cmd_solo = comando_completo
        lista_de_comandos.append(cmd_solo)

        indicacionParametros = re.findall('\(.*?\)', comando_completo)
        for parametro in indicacionParametros:
            parametro = parametro.replace("(", "")
            parametro = parametro.replace(")", "")
        if parametro:
            lista_de_parametros.append(parametro)
    return lista_de_comandos, lista_de_parametros


# ESTO ES todo GUI VER DÓNDE LO METEMOS:
# widgetFormulario = QtGui.QWidget(self)
# widgetFormulario.setGeometry(5,5,900,250)
# layout = QtGui.QVBoxLayout(widgetFormulario)
# print 'idFilaTemp vale: '+str(idFilaTemp)
# self.form=ProcessFormV3(idFilaTemp)
# layout.addWidget(self.form)
# self.show()

# if __name__ == "__main__":
#    findParameters()

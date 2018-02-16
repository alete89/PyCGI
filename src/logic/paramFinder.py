# -*- coding: utf-8 -*-

import re
from . import csvdb


def findParameters(dataset):
    parametro = None
    listas_de_parametros = []
    lista_de_comandos = []
    for comando_completo in csvdb.getColumn(dataset, 5):
        parametros_por_comando = []
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
                parametros_por_comando.append(parametro)
        listas_de_parametros.append(parametros_por_comando)
    return lista_de_comandos, listas_de_parametros

# -*- coding: utf-8 -*-

import re
from . import csvdb

DEL_ABRE = "<"
DEL_CIERRA = ">"
RE_BUSCA_DELIM = re.escape(DEL_ABRE) + ".*?" + re.escape(DEL_CIERRA)


def findParameters(dataset):
    parametro = None
    listas_de_parametros = []
    lista_de_comandos = []
    for comando_completo in csvdb.getColumn(dataset, 5):
        parametros_por_comando = []
        delimitador_index = comando_completo.find(DEL_ABRE)
        if delimitador_index >= 1:
            cmd_solo = comando_completo[0: delimitador_index - 1]
        else:
            cmd_solo = comando_completo

        lista_de_comandos.append(cmd_solo)
        indicacionParametros = re.findall(RE_BUSCA_DELIM, comando_completo)
        for parametro in indicacionParametros:
            parametro = parametro.replace(DEL_ABRE, "")
            parametro = parametro.replace(DEL_CIERRA, "")
            if parametro:
                parametros_por_comando.append(parametro)
        listas_de_parametros.append(parametros_por_comando)
    return lista_de_comandos, listas_de_parametros

# -*- coding: utf-8 -*-

import re
from . import csvdb

DEL_ABRE = r"<"
DEL_CIERRA = r">"
RE_ENTRE_DELIM = DEL_ABRE + r"(.+?)" + DEL_CIERRA


def getParameters(rows):
    for index, comando_completo in enumerate(csvdb.getColumn(rows, 5)):
        found = re.findall(RE_ENTRE_DELIM, comando_completo)
        rows[index].append(found)
    return rows

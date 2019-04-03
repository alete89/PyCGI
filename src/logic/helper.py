import core


def getValueFromCfg(clave):
    with open(core.CFG_PATH, 'r') as f:
        text = f.read()
    return text.split(clave)[1].split("\n")[0].replace("'", "").replace('"', '')


def getTreeViewInitialPath():
    initial = getValueFromCfg('treeViewInitialPath=')
    if initial == '':
        from PyQt4 import QtCore
        initial = QtCore.QDir.rootPath()
    return initial

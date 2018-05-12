from PyQt4 import QtGui, QtCore
from ..logic import core


class TreeView(QtGui.QTreeView):
    def __init__(self, window_instance):
        super(TreeView, self).__init__()
        self.window = window_instance

        self.fsmodel = QtGui.QFileSystemModel(self)
        self.fsmodel.setRootPath(core.getTreeViewRootPath())
        initialPath = self.fsmodel.index(core.getTreeViewInitialPath())
        self.setModel(self.fsmodel)
        self.expand(initialPath)
        while initialPath.parent().isValid():
            self.expand(initialPath.parent())
            initialPath = initialPath.parent()
        self.setAnimated(True)
        self.setIndentation(15)
        self.setSortingEnabled(True)
        self.setColumnWidth(0, 300)
        self.doubleClicked.connect(self.openFileFromTree)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openRightClickMenu)

    def openFileFromTree(self, index):
        indexItem = self.fsmodel.index(index.row(), 0, index.parent())
        filePath = self.fsmodel.filePath(indexItem)
        fname = str(filePath)
        self.window.openFile(fname)

    def openRightClickMenu(self, position):
        indexes = self.selectedIndexes()
        menu = QtGui.QMenu()
        filePath = str(self.fsmodel.filePath(indexes[0]))

        # Actions
        copyPath = menu.addAction(self.tr("Copy Full Path..."))
        # Resultado
        eleccion = menu.exec_(self.viewport().mapToGlobal(position))
        if eleccion == copyPath:
            self.setClipboard(filePath)

    def setClipboard(self, text):
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(text)

from PyQt4 import QtGui, QtCore
from ..logic import core
import shutil as shu
import os


class TreeView(QtGui.QTreeView):
    def __init__(self, window_instance):
        super(TreeView, self).__init__()
        self.window = window_instance
        self.fsmodel = QtGui.QFileSystemModel(self)
        self.fsmodel.setRootPath(core.getTreeViewRootPath())
        initialPath = self.fsmodel.index(core.getTreeViewInitialPath())
        self.setModel(self.fsmodel)
        self.setRootIndex(self.fsmodel.index(core.getTreeViewRootPath()))
        self.expand(initialPath)
        while initialPath.parent().isValid():
            self.expand(initialPath.parent())
            initialPath = initialPath.parent()
        self.setAnimated(True)
        self.setIndentation(15)
        self.setSortingEnabled(True)
        self.sortByColumn(0, 0)
        self.setColumnWidth(0, 300)
        self.doubleClicked.connect(self.openFileFromTree)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openRightClickMenu)

    def updateTreeView(self):
        self.collapseAll()
        self.setRootIndex(self.fsmodel.index(core.getTreeViewRootPath()))
        self.update()
        initialPath = self.fsmodel.index(core.getTreeViewInitialPath())
        self.expand(initialPath)
        while initialPath.parent().isValid():
            self.expand(initialPath.parent())
            initialPath = initialPath.parent()

    def openFileFromTree(self, index):
        indexItem = self.fsmodel.index(index.row(), 0, index.parent())
        filePath = self.fsmodel.filePath(indexItem)
        if os.path.isfile(filePath):
            fname = str(filePath)
            self.window.tabWidget.setCurrentIndex(1)
            self.window.tabEditor.openFile(fname)

    def openRightClickMenu(self, position):
        indexes = self.selectedIndexes()
        menu = QtGui.QMenu()
        clipboard = QtGui.QApplication.clipboard()
        filePath = str(self.fsmodel.filePath(indexes[0]))

        # Actions
        createDirFunction = menu.addAction(self.tr("Create directory"))
        renameFunction = menu.addAction(self.tr("Rename"))
        separator = menu.addSeparator()
        copyFileFunction = menu.addAction(self.tr("Copy"))
        moveFileFunction = menu.addAction(self.tr("Move"))
        pasteFileFunction = menu.addAction(self.tr("Paste"))
        separator = menu.addSeparator()
        removeFileFunction = menu.addAction(self.tr("Remove"))
        separator = menu.addSeparator()
        copyPath = menu.addAction(self.tr("Get Full Path..."))

        # Resultado
        eleccion = menu.exec_(self.viewport().mapToGlobal(position))

        if eleccion == copyPath:
            self.setClipboard(filePath, copyOrMove="")

        elif eleccion == renameFunction:
            self.showDialogRename(filePath)

        elif eleccion == createDirFunction:
            self.showDialogMkDir(filePath)

        elif eleccion == copyFileFunction:
            copyOrMove = 1
            self.setClipboard(filePath, copyOrMove)

        elif eleccion == moveFileFunction:
            copyOrMove = 0
            self.setClipboard(filePath, copyOrMove)

        elif eleccion == removeFileFunction:
            res = QtGui.QMessageBox.information(None, "Warning", "<b>Remove this</b>?\n"+str(
                filePath), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

            if res == QtGui.QMessageBox.Cancel:
                return
            else:
                if os.path.isfile(filePath):
                    os.remove(filePath)
                elif os.path.isdir(filePath):
                    delDir = QtGui.QMessageBox.information(None, "Warning", "This is a directory. All files inside will be deleted.\n"+str(
                        filePath), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
                    if delDir == QtGui.QMessageBox.Cancel:
                        return
                    else:
                        shu.rmtree(filePath)
                else:
                    QtGui.QMessageBox.information(None, "Message", "Error on remove")

        elif eleccion == pasteFileFunction:
            filePath = str(self.fsmodel.filePath(indexes[0]))
            oldFilePath = str(clipboard.text())
            copyOrMove = oldFilePath[0]
            oldFilePath = oldFilePath[1:]
            newPath, newFile = os.path.split(oldFilePath)
            fileToPaste = filePath+"/"+newFile
            try:
                if copyOrMove == "1":
                    shu.copyfile(oldFilePath, fileToPaste)
                else:
                    shu.move(oldFilePath, fileToPaste)
            except:
                QtGui.QMessageBox.information(None, "Message", "Error on paste")

    def setClipboard(self, text, copyOrMove):
        # Necesito indicar en el clipboard si el usuario
        # quiere copiar o cortar (mover) el archivo
        # para eso agrego un indicador al inicio del path
        # en el clipboard
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(str(copyOrMove)+str(text))

    def showDialogMkDir(self, filePath):
        newPath, newFile = os.path.split(filePath)
        myDir, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
                                               'Create a directory in <b>'+str(newPath)+'</b>')
        if ok:
            try:
                if os.path.exists(newPath):
                    os.mkdir(newPath+"/"+myDir)
            except:
                QtGui.QMessageBox.information(None, "Message", "Error on create directory")

    def showDialogRename(self, filePath):
        newPath, oldFileName = os.path.split(filePath)
        myNewName, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
                                                   'Rename <b>'+str(oldFileName)+'</b>', text=oldFileName)

        fileToRename = newPath+"/"+myNewName

        if ok:
            try:
                if os.path.exists(newPath):
                    shu.move(filePath, fileToRename)
            except:
                QtGui.QMessageBox.information(None, "Message", "Error on rename")

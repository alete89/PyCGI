# -*- coding: utf-8 -*-

import sys
# import os
from PyQt4 import QtGui, QtCore
import Highlighter
import CodeEditor
import TablaMySQLEmbedded
#from stringFinderV2 import *
import core


class PyCGI(QtGui.QMainWindow):

    def __init__(self):
        super(PyCGI, self).__init__()
        self.is_new = True  # Flag para el archivo del editor
        self.file_name = ''  # Nombre del archivo del editor
        self.VentanaPrincipal()
        self.statusBar()
        self.setWindowTitle(
            'PyCGI - Instituto de Tecnologia Nuclear Dan Beninson')
        self.show()
        for menu in core.menuList():
            self.menuPrincipal(menu)

    def menuPrincipal(self, menu):
        menubar = self.menuBar()
        thisMenu = menubar.addMenu('&' + str(menu))
        for subMenu, idFila in zip(core.subMenuList(menu), core.idList(menu)):
            action = QtGui.QAction('&' + str(subMenu), self)
            action.setStatusTip(str(idFila) + " - " + str(subMenu))
            action.triggered.connect(
                lambda ignore, idt=idFila: self.PreEjecutarComandos(idt))
            thisMenu.addAction(action)

    def VentanaPrincipal(self):
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.currentPath())
        tree = QtGui.QTreeView()
        tree.setModel(self.model)
        tree.setAnimated(True)
        tree.setIndentation(15)
        tree.setSortingEnabled(True)
        tree.setColumnWidth(0, 300)

        # tree.doubleClicked.connect(self.OpenFileNow)

        self.toolbar = self.addToolBar('Editor de texto')

        OpenIcon = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        OpenIcon.setShortcut('Ctrl+o')
        OpenIcon.triggered.connect(self.OpenDialog)
        self.toolbar.addAction(OpenIcon)

        SaveIcon = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        SaveIcon.setShortcut('Ctrl+s')
        SaveIcon.triggered.connect(self.saveDialog)
        self.toolbar.addAction(SaveIcon)

        SaveAsIcon = QtGui.QAction(QtGui.QIcon(
            'icons/saveAs.png'), 'Save as', self)
        SaveAsIcon.setShortcut('Ctrl+g')
        SaveAsIcon.triggered.connect(self.saveAsDialog)
        self.toolbar.addAction(SaveAsIcon)

        CloseIcon = QtGui.QAction(QtGui.QIcon(
            'icons/closeFile.png'), 'Close', self)
        CloseIcon.setShortcut('Ctrl+x')
        CloseIcon.triggered.connect(self.CloseDialog)
        self.toolbar.addAction(CloseIcon)

        self.setWindowTitle('Toolbar')
        self.setMinimumWidth(650)
        self.setMinimumHeight(600)

        font = QtGui.QFont()
        font.setFamily('Monospace')
        font.setPointSize(11)

        self.killButton = QtGui.QPushButton("kill process")
        self.killButton.clicked.connect(self.KillingProcess)

        self.CleanTerminal = QtGui.QPushButton("clean")
        self.CleanTerminal.clicked.connect(self.CleaningTerminal)

        self.killGo = QtGui.QPushButton("kill and Go")
        self.killGo.clicked.connect(self.KillAndGo)

        self.Exe = QtGui.QPushButton("Exe")
        self.Exe.clicked.connect(core.EjecutarComandos)

        self.Update = QtGui.QPushButton("Update PyCGI")
        self.Update.clicked.connect(self.updateFunc)  # restartea la app

        self.terminalDeTexto = QtGui.QTextEdit(self)
        self.terminalDeTexto.setReadOnly(True)
        self.terminalDeTexto.setFont(font)
        self.terminalDeTexto.setStyleSheet(
            "background-color: #585858; color: #fff")

        self.terminalDeProceso = QtGui.QTextEdit(self)

        self.terminalDeProceso.setReadOnly(True)
        self.terminalDeProceso.setFont(font)
        self.terminalDeProceso.setStyleSheet(
            "background-color: #595999; color: #fff")

        self.cursor = self.terminalDeTexto.textCursor()

        self.EditorDeTexto = QtGui.QPlainTextEdit()
        self.EditorDeTexto = CodeEditor.CodeEditor()
        self.highlighter = Highlighter.Highlighter(
            self.EditorDeTexto.document())

        self.EditorDeTexto.setFont(font)
        self.EditorDeTexto.setStyleSheet("background-color: #f1f1f1;")
        self.EditorDeTexto.setMinimumHeight(100)

        self.terminalDeTexto.setMinimumHeight(100)
        self.cursor = QtGui.QTextCursor(self.terminalDeTexto.document())

        widget_central = QtGui.QWidget(self)
        self.setCentralWidget(widget_central)

        layout = QtGui.QVBoxLayout(widget_central)

        tabs = QtGui.QTabWidget()
        tab1 = QtGui.QWidget()
        tab2 = QtGui.QWidget()
        tab3 = QtGui.QWidget()
#        tab4=QWidget()

        BotoneraInferior = QtGui.QHBoxLayout(widget_central)
        BotoneraInferior.addWidget(self.killButton)
        BotoneraInferior.addWidget(self.CleanTerminal)
        BotoneraInferior.addWidget(self.Update)
        BotoneraInferior.addWidget(self.killGo)
        BotoneraInferior.addWidget(self.Exe)

        splitterVert = QtGui.QSplitter(QtCore.Qt.Vertical)

        splitterVert.addWidget(self.terminalDeTexto)
        splitterVert.addWidget(self.terminalDeProceso)
        splitterVert.setSizes([200, 200])

        tabs.addTab(tab1, "Proceso")
        tabs.addTab(tab2, "Editor")
        tabs.addTab(tab3, "Tabla de secuencias")

        layoutTabs1 = QtGui.QVBoxLayout(tabs)
        layoutTabs1.addWidget(splitterVert)
        tab1.setLayout(layoutTabs1)

        layoutTabs2 = QtGui.QVBoxLayout(tabs)
        layoutTabs2.addWidget(self.EditorDeTexto)
        tab2.setLayout(layoutTabs2)

        layoutTabs3 = QtGui.QVBoxLayout(tabs)

        self.form = TablaMySQLEmbedded.TablaMySQLEmbedded()
        layoutTabs3.addWidget(self.form)
        tab3.setLayout(layoutTabs3)

        splitterHoriz = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitterHoriz.addWidget(tree)
        splitterHoriz.addWidget(tabs)
        splitterHoriz.setSizes([100, 500])

        layout.addWidget(splitterHoriz)

        layout.addLayout(BotoneraInferior)

        self.processRun = QtCore.QProcess(self)
        self.processRun.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.processRun.setReadChannelMode(QtCore.QProcess.MergedChannels)

        # dataready debería venir de core
        self.processRun.readyRead.connect(self.showOutputInTerminal)
        self.TermX = core.TerminalX(self)

        self.setLayout(BotoneraInferior)
        self.show()

    def showOutputInTerminal(self):
        self.terminalDeTexto.append(core.getOutput())

    def KillingProcess(self):
        self.cursor.insertText('\n --- Process stopped by user --- ')
        self.cursor.movePosition(self.cursor.End)
        self.processRun.close()

    def CleaningTerminal(self):
        self.terminalDeTexto.setText(" ")
        self.terminalDeProceso.setText(" ")

    def KillAndGo(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.cursor.insertText('\n--- Process stopped by user ---')
            self.processRun.close()
            exit()
        else:
            pass

    def OpenDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname:
            with open(fname, 'r') as f:
                data = f.read()
                self.EditorDeTexto.setPlainText(data)
                self.is_new = False
                self.file_name = fname
            print 'OpenDialog - fname: ' + str(fname)
            return fname
        return ''


    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def OpenFileNow(self, index):

        indexItem = self.model.index(index.row(), 0, index.parent())
        filePath = self.model.filePath(indexItem)
        fname = str(filePath)
        print 'fname vale: ' + str(fname)
        if fname:
            with open(fname, 'r') as f:
                data = f.read()
                self.EditorDeTexto.setPlainText(data)
                self.is_new = False
                self.file_name = fname
            print 'OpenDialog - fname: ' + str(fname)
            return fname
        return ''

    def saveAsDialog(self):
        name = QtGui.QFileDialog.getSaveFileName(
            self, 'Save File', str(self.file_name))
        if name:
            textoParaGuardar = self.EditorDeTexto.toPlainText()
            with open(name, "w") as nFile:
                nFile.write(textoParaGuardar)
                self.is_new = False
                self.file_name = name

    def saveDialog(self):
        if self.is_new:
            self.saveAsDialog()
        else:
            textoParaGuardar = self.EditorDeTexto.toPlainText()
            with open(self.file_name, "w") as nFile:
                nFile.write(textoParaGuardar)

    def CloseDialog(self):
        # TO DO preguntar si desea guardar antes de borrar.
        if self.is_new:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText(
                u"Se modificó el documento desde la última vez que se guardó")
            msg.setInformativeText("desea guardar los cambios?")
            msg.setStandardButtons(
                QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            resultado = msg.exec_()
            print resultado
            if resultado == QtGui.QMessageBox.Save:
                self.saveDialog()
            elif resultado == QtGui.QMessageBox.Discard:
                pass
            elif resultado == QtGui.QMessageBox.Cancel:
                return

        self.EditorDeTexto.clear()
        self.is_new = True
        self.file_name = "NewFile"

    def updateFunc(self):
        pass


def mainLoop():
    app = QtGui.QApplication(sys.argv)
    ex = PyCGI()
    ex.show()

    # proceso1=mp.Pool(4)
    # proceso1.map(PyCGI.EjecutarComandos,idFilaTemp)
    # proceso1.close()
    # proceso1.join()
    sys.exit(app.exec_())


if __name__ == '__main__':
    mainLoop()

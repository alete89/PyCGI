# -*- coding: utf-8 -*-
import sys
import os
from PyQt4 import QtGui, QtCore
from ..logic import core
from . import Highlighter
from . import CodeEditor
from . import tabla


class PyCGI(QtGui.QMainWindow):
    def __init__(self):
        super(PyCGI, self).__init__()
        self.is_new = True  # Flag para el archivo del editor
        self.file_name = ''  # Nombre del archivo del editor
        self.setWindowTitle('PyCGI - Instituto de Tecnologia Nuclear Dan Beninson')
        self.treeWidget()
        self.crearIndicadorSecuencia()
        self.crearTerminal()
        self.crearEditorDeTexto()
        self.ventanaPrincipal()
        self.crearMenu()
        self.statusBar()
        self.show()

    def treeWidget(self):
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.currentPath())
        self.tree = QtGui.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setAnimated(True)
        self.tree.setIndentation(15)
        self.tree.setSortingEnabled(True)
        self.tree.setColumnWidth(0, 300)
        self.tree.doubleClicked.connect(self.openFileFromTree)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openRightClickMenu)

    def openRightClickMenu(self, position):
        indexes = self.tree.selectedIndexes()
        menu = QtGui.QMenu()
        filePath = str(self.model.filePath(indexes[0]))

        # Actions
        copyPath = menu.addAction(self.tr("Copy Full Path..."))
        # Resultado
        eleccion = menu.exec_(self.tree.viewport().mapToGlobal(position))
        if eleccion == copyPath:
            self.setClipboard(filePath)

    def setClipboard(self, text):
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(text)

    def crearIndicadorSecuencia(self):
        self.font = QtGui.QFont()
        self.font.setFamily("Consolas, 'Courier New', monospace")
        self.font.setPointSize(11)  # font size in points
        self.indicadorSecuencia = QtGui.QTextEdit(self)
        self.indicadorSecuencia.setReadOnly(True)
        self.indicadorSecuencia.setFont(self.font)
        self.indicadorSecuencia.setMaximumHeight(50)
        self.indicadorSecuencia.setFontWeight(75)  # BOLD sólo para la instrucción actual!

    def crearTerminal(self):
        self.terminalOutput = QtGui.QTextEdit(self)
        self.terminalOutput.setReadOnly(True)
        self.terminalOutput.setFont(self.font)
        self.terminalOutput.setStyleSheet("background-color: #585858; color: #fff")
        self.cursor = self.terminalOutput.textCursor()

    def crearEditorDeTexto(self):
        self.EditorDeTexto = CodeEditor.CodeEditor()
        self.EditorDeTexto.setFont(self.font)
        self.EditorDeTexto.setStyleSheet("background-color: #f1f1f1;")
        self.EditorDeTexto.setMinimumHeight(100)
        self.highlighter = Highlighter.Highlighter(self.EditorDeTexto.document())
        self.highlighter.setDocument(None)

    def crearToolbar(self):
        toolbar = self.addToolBar("Editor de texto Toolbar")
        NewOne = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New', self)
        NewOne.setShortcut('Ctrl+n')
        NewOne.triggered.connect(self.newEditorTab)
        toolbar.addAction(NewOne)
        OpenIcon = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        OpenIcon.setShortcut('Ctrl+o')
        OpenIcon.triggered.connect(self.openFile)
        toolbar.addAction(OpenIcon)
        SaveIcon = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        SaveIcon.setShortcut('Ctrl+s')
        SaveIcon.triggered.connect(self.saveDialog)
        toolbar.addAction(SaveIcon)
        SaveAsIcon = QtGui.QAction(QtGui.QIcon('icons/saveAs.png'), 'Save as', self)
        SaveAsIcon.setShortcut('Ctrl+g')
        SaveAsIcon.triggered.connect(self.saveAsDialog)
        toolbar.addAction(SaveAsIcon)
        CloseIcon = QtGui.QAction(QtGui.QIcon('icons/closeFile.png'), 'Close', self)
        CloseIcon.setShortcut('Ctrl+x')
        CloseIcon.triggered.connect(self.CloseDialog)
        toolbar.addAction(CloseIcon)
        return toolbar

    def ventanaPrincipal(self):
        self.setMinimumWidth(650)
        self.setMinimumHeight(600)
        self.killButton = QtGui.QPushButton("Kill process")
        self.killButton.clicked.connect(self.KillingProcess)
        self.cleanTerminalButton = QtGui.QPushButton("Clean terminal")
        self.cleanTerminalButton.clicked.connect(self.cleanTerminal)
        self.killGo = QtGui.QPushButton("Exit app")
        self.killGo.clicked.connect(self.quitApp)
        self.terminalOutput.setMinimumHeight(100)
        self.cursor = QtGui.QTextCursor(self.terminalOutput.document())
        widget_central = QtGui.QWidget(self)
        self.setCentralWidget(widget_central)
        layout = QtGui.QVBoxLayout(widget_central)
        self.tabs = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        self.tabsInternas = QtGui.QTabWidget()
        self.tabsConfiguracion = QtGui.QTabWidget()
        self.configTab1 = QtGui.QWidget()
        self.configTab2 = QtGui.QWidget()
        self.configTab3 = QtGui.QWidget()
        BotoneraInferior = QtGui.QHBoxLayout(widget_central)
        BotoneraInferior.addWidget(self.killGo)
        self.tabs.addTab(self.tab1, "Proceso")
        self.tabs.addTab(self.tab2, "Editor")
        layoutTab1 = QtGui.QVBoxLayout(self.tabs)
        layoutTab1.addWidget(self.indicadorSecuencia)
        layoutTab1.addWidget(self.terminalOutput)
        layoutTab1.addWidget(self.killButton)
        layoutTab1.addWidget(self.cleanTerminalButton)
        self.tab1.setLayout(layoutTab1)
        layoutTab2 = QtGui.QVBoxLayout(self.tabs)
        layoutTab2.addWidget(self.crearToolbar())
        self.tab2.setLayout(layoutTab2)
        self.tabs.addTab(self.tab3, "Configuracion")
        layoutTabsConfig = QtGui.QVBoxLayout(self.tab3)
        layoutTabsConfig.addWidget(self.tabsConfiguracion)
        self.tab3.setLayout(layoutTabsConfig)
        self.tabsConfiguracion.addTab(self.configTab1, "Tabla de Secuencias")
        self.tabsConfiguracion.addTab(self.configTab2, "Variables Globales")
        self.tabsConfiguracion.addTab(self.configTab3, "Configuracion automatica")
        layoutTab2.addWidget(self.tabsInternas)
        layoutTab3 = QtGui.QVBoxLayout(self.tabs)
        self.tabla = tabla.Tabla()
        self.tabla.ShowDataSet(core.fullDataSet(), core.getHeaders())
        self.addRowButton = QtGui.QPushButton("Agregar fila")
        self.addRowButton.clicked.connect(self.tabla.addRow)
        self.delRowButton = QtGui.QPushButton("Borrar fila")
        self.delRowButton.clicked.connect(self.tabla.delRow)
        self.saveTableButton = QtGui.QPushButton("Guardar cambios")
        self.saveTableButton.clicked.connect(self.guardarCambiosClicked)
        layoutTab3.addWidget(self.tabla)
        layoutTab3.addWidget(self.addRowButton)
        layoutTab3.addWidget(self.delRowButton)
        layoutTab3.addWidget(self.saveTableButton)
        self.configTab1.setLayout(layoutTab3)
        splitterHoriz = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitterHoriz.addWidget(self.tree)
        splitterHoriz.addWidget(self.tabs)
        splitterHoriz.setSizes([100, 500])
        layout.addWidget(splitterHoriz)
        layout.addLayout(BotoneraInferior)
        self.show()

    def crearMenu(self):
        self.menuBar().clear()
        menubar = self.menuBar()
        for menu in core.menuList(core.fullDataSet()):
            thisMenu = menubar.addMenu('&' + str(menu))
            for subMenu, idFila in zip(core.subMenuList(menu, core.fullDataSet()), core.idList(menu, core.fullDataSet())):
                action = QtGui.QAction('&' + str(subMenu), self)
                action.setStatusTip(str(idFila) + " - " + str(subMenu))
                action.triggered.connect(lambda ignore, idt=subMenu: self.subMenuOptionClicked(idt))
                thisMenu.addAction(action)

    def subMenuOptionClicked(self, subMenu):
        core.PreEjecutarComandos(subMenu, self)

    def showOutputInTerminal(self, text):
        self.terminalOutput.append(text)

    def KillingProcess(self):
        self.terminalOutput.append("Matando proceso:")
        core.matarProceso(self)

    def cleanTerminal(self):
        self.terminalOutput.clear()
        self.indicadorSecuencia.clear()

    def guardarCambiosClicked(self):
        core.saveTable(self.tabla)
        self.crearMenu()

    def quitApp(self):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure you want to quit?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            sys.exit()

    def newEditorTab(self, fname):
        if not fname:
            newTabName = 'Temp'
        else:
            if os.path.isfile(fname):
                newTabName = str(fname)

        newTab = QtGui.QWidget()
        self.tabsInternas.addTab(newTab, str(newTabName))
        newTabLayout = QtGui.QVBoxLayout(newTab)
        self.crearEditorDeTexto()
        newTabLayout.addWidget(self.EditorDeTexto)
        newTab.setLayout(newTabLayout)
        self.tabsInternas.setCurrentWidget(newTab)

    def openFile(self, fname):
        if not fname:
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname:
            with open(fname, 'r') as f:
                self.newEditorTab(fname)
                data = f.read()
                self.EditorDeTexto.setPlainText(data)
                self.is_new = False
                self.file_name = fname
        if fname[-3:] == ".py":
            self.highlighter.setDocument(self.EditorDeTexto.document())

    def openFileFromTree(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        filePath = self.model.filePath(indexItem)
        fname = str(filePath)
        self.openFile(fname)

    def saveAsDialog(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', str(self.file_name))
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

    def removeTabFile(self):
        self.tabsInternas.removeTab(self.tabsInternas.currentIndex())

    def CloseDialog(self):
        if self.is_new:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText(u"Se modificó el documento desde la última vez que se guardó")
            msg.setInformativeText("desea guardar los cambios?")
            msg.setStandardButtons(QtGui.QMessageBox.Save |
                                   QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            resultado = msg.exec_()
            if resultado == QtGui.QMessageBox.Save:
                self.saveDialog()
            elif resultado == QtGui.QMessageBox.Discard:
                self.removeTabFile()
            elif resultado == QtGui.QMessageBox.Cancel:
                return
        else:
            self.removeTabFile()

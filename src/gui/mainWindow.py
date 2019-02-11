# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from ..logic import core
from . import Editor
from . import tabla
from . import treeView


class PyCGI(QtGui.QMainWindow):
    def __init__(self):
        super(PyCGI, self).__init__()
        self.setWindowTitle('Nuclear Py - Instituto de Tecnologia Nuclear Dan Beninson')
        self.treeWidget = treeView.TreeView(self)
        self.crearIndicadorSecuencia()
        self.crearTerminal()
        self.ventanaPrincipal()
        self.crearMenu()
        self.statusBar()
        self.show()

    def crearIndicadorSecuencia(self):
        self.font = QtGui.QFont()
        self.font.setFamily("Consolas, 'Courier New', monospace")
        self.font.setPointSize(11)  # font size in points
        self.indicadorSecuencia = QtGui.QTextEdit(self)
        self.indicadorSecuencia.setReadOnly(True)
        self.indicadorSecuencia.setFont(self.font)
        self.indicadorSecuencia.setMaximumHeight(800)
        self.indicadorSecuencia.setFontWeight(75)  # 50 normal, 75 BOLD

    def crearTerminal(self):
        self.terminalOutput = QtGui.QTextEdit(self)
        self.terminalOutput.setReadOnly(True)
        self.terminalOutput.setFont(self.font)
        self.terminalOutput.setStyleSheet("background-color: #585858; color: #fff")
        self.terminalOutput.setMaximumHeight(1000)
        self.cursor = self.terminalOutput.textCursor()

    def ventanaPrincipal(self):
        self.setMinimumWidth(800)
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
        self.tabWidget = QtGui.QTabWidget()
        self.tabOutputs = QtGui.QWidget()
        self.tabEditor = Editor.Editor()
        self.tabApplication = QtGui.QWidget()
        self.tabConfiguracion = QtGui.QTabWidget()

        self.configTab1 = QtGui.QWidget()
        self.configTab2 = QtGui.QWidget()
        self.configTab3 = QtGui.QWidget()
        self.configTab4 = QtGui.QWidget()

        BotoneraInferior = QtGui.QHBoxLayout(widget_central)
        BotoneraInferior.addWidget(self.killGo)
        self.tabWidget.addTab(self.tabOutputs, "Process")
        self.tabWidget.addTab(self.tabEditor, "Text Editor")
        layoutTab1 = QtGui.QVBoxLayout(self.tabWidget)
        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.indicadorSecuenciaNombre = QtGui.QLabel('Current process')
        self.terminalOutputNombre = QtGui.QLabel('Standard output')
        layoutSecuencia = QtGui.QVBoxLayout()
        layoutSecuencia.addWidget(self.indicadorSecuenciaNombre)
        layoutSecuencia.addWidget(self.indicadorSecuencia)
        unWidget = QtGui.QWidget()
        unWidget.setLayout(layoutSecuencia)
        splitter.addWidget(unWidget)
        otroWidget = QtGui.QWidget()
        layoutTerminal = QtGui.QVBoxLayout()
        layoutTerminal.addWidget(self.terminalOutputNombre)
        layoutTerminal.addWidget(self.terminalOutput)
        otroWidget.setLayout(layoutTerminal)
        splitter.addWidget(otroWidget)
        layoutTab1.addWidget(splitter)
        layoutTab1.addWidget(self.killButton)
        layoutTab1.addWidget(self.cleanTerminalButton)
        self.tabOutputs.setLayout(layoutTab1)

        self.tabWidget.addTab(self.tabApplication, "Application")
        layoutTabsConfig = QtGui.QVBoxLayout(self.tabApplication)
        layoutTabsConfig.addWidget(self.tabConfiguracion)
        self.tabApplication.setLayout(layoutTabsConfig)
        self.tabConfiguracion.addTab(self.configTab1, "Sequence Table")
        self.tabConfiguracion.addTab(self.configTab4, "Environment")

        self.dirRoot = QtGui.QLabel('Root path')
        self.dirInitial = QtGui.QLabel('Initial path')
        self.dirButtonRoot = QtGui.QPushButton("Update directory")
        self.dirButtonInitial = QtGui.QPushButton("Update directory")
        viewInitialPath=core.getTreeViewInitialPath()
        viewRootPath=core.getTreeViewRootPath()

        print "Path 1 vale: " + str(viewInitialPath)

        self.dirRootEdit = QtGui.QLineEdit(str(viewRootPath))
        self.dirInitialEdit = QtGui.QLineEdit(str(viewInitialPath))
        
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.dirRoot, 1, 0)
        self.grid.addWidget(self.dirRootEdit, 1, 1)
        self.grid.addWidget(self.dirButtonRoot, 1, 2)
        self.grid.addWidget(self.dirInitial, 2, 0)
        self.grid.addWidget(self.dirInitialEdit, 2, 1)
        self.grid.addWidget(self.dirButtonInitial, 2, 2)
        
        dirInitialText=self.dirInitialEdit.text()
        dirRootText=self.dirRootEdit.text()
        
        print "Path 2 vale: " + str(dirInitialText)
        # estas dos lineas no funcionan bien
        # pretendo llevar a la funcion updateCfgPath el texto del campo QlineEdit
        # pero devuelve '<built-in function dir>' en el archivo cfg

        self.dirButtonInitial.clicked.connect(lambda: core.updateCfgPath(self.dirInitialEdit.text(),0))
        self.dirButtonRoot.clicked.connect(lambda: core.updateCfgPath(self.dirRootEdit.text(),1))

        self.configTab4.setLayout(self.grid)

        layoutTab3 = QtGui.QVBoxLayout(self.tabWidget)
        self.tabla = tabla.Tabla()
        self.tabla.ShowDataSet(core.fullDataSet(), core.getHeaders())
        self.addRowButton = QtGui.QPushButton("Add row")
        self.addRowButton.clicked.connect(self.tabla.addRow)
        self.delRowButton = QtGui.QPushButton("Delete current row")
        self.delRowButton.clicked.connect(self.tabla.delRow)
        self.saveTableButton = QtGui.QPushButton("Save changes")
        self.saveTableButton.clicked.connect(self.guardarCambiosClicked)
        layoutTab3.addWidget(self.tabla)
        layoutTab3.addWidget(self.addRowButton)
        layoutTab3.addWidget(self.delRowButton)
        layoutTab3.addWidget(self.saveTableButton)
        self.configTab1.setLayout(layoutTab3)
        splitterHoriz = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitterHoriz.addWidget(self.treeWidget)
        splitterHoriz.addWidget(self.tabWidget)
        layout.addWidget(splitterHoriz)
        layout.addLayout(BotoneraInferior)
        self.show()
        sizes = splitterHoriz.sizes()
        splitterHoriz.setSizes([sizes[0] * 0.7, sizes[1]])

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
        self.terminalOutput.append("Killing process:")
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

# -*- coding: utf-8 -*-
import sys
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

        self.setWindowTitle(
            'PyCGI - Instituto de Tecnologia Nuclear Dan Beninson')

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
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openContextMenu)

        self.tree.setModel(self.model)
        self.tree.setAnimated(True)
        self.tree.setIndentation(15)
        self.tree.setSortingEnabled(True)
        self.tree.setColumnWidth(0, 300)
        self.tree.doubleClicked.connect(self.openFileFromTree)

    def openContextMenu(self, position):
        indexes = self.tree.selectedIndexes()
        # El if a continuación obtiene el nivel de profundidad del elemento

        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            selected = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        rightClickMenu = QtGui.QMenu()
        # print self.model.fileName(selected)
        # print self.model.filePath(selected)
        if self.model.fileName(selected)[-3:] == '.py':
            rightClickMenu.addAction(self.tr("Agregar a Menu"))
        rightClickMenu.addAction(
            self.tr("Copy Path" + str(self.model.filePath(selected))))

        rightClickMenu.exec_(self.tree.viewport().mapToGlobal(position))

    def crearIndicadorSecuencia(self):
        self.font = QtGui.QFont()
        self.font.setFamily("Consolas, 'Courier New', monospace")
        self.font.setPointSize(11)  # font size in points
        self.indicadorSecuencia = QtGui.QTextEdit(self)
        self.indicadorSecuencia.setReadOnly(True)
        self.indicadorSecuencia.setFont(self.font)
        self.indicadorSecuencia.setMaximumHeight(50)
        # BOLD sólo para la instrucción actual!
        self.indicadorSecuencia.setFontWeight(75)

    def crearTerminal(self):
        self.terminalOutput = QtGui.QTextEdit(self)
        self.terminalOutput.setReadOnly(True)
        self.terminalOutput.setFont(self.font)
        self.terminalOutput.setStyleSheet(
            "background-color: #585858; color: #fff")

        self.cursor = self.terminalOutput.textCursor()

    def crearEditorDeTexto(self):
        self.EditorDeTexto = CodeEditor.CodeEditor()

        self.EditorDeTexto.setFont(self.font)
        self.EditorDeTexto.setStyleSheet("background-color: #f1f1f1;")
        self.EditorDeTexto.setMinimumHeight(100)

        self.pythonHighlighter = Highlighter.Highlighter(
            self.EditorDeTexto.document())

    def crearToolbar(self):
        toolbar = self.addToolBar("Editor de texto Toolbar")

        OpenIcon = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        OpenIcon.setShortcut('Ctrl+o')
        OpenIcon.triggered.connect(self.openFile)
        toolbar.addAction(OpenIcon)

        SaveIcon = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        SaveIcon.setShortcut('Ctrl+s')
        SaveIcon.triggered.connect(self.saveDialog)
        toolbar.addAction(SaveIcon)

        SaveAsIcon = QtGui.QAction(QtGui.QIcon(
            'icons/saveAs.png'), 'Save as', self)
        SaveAsIcon.setShortcut('Ctrl+g')
        SaveAsIcon.triggered.connect(self.saveAsDialog)
        toolbar.addAction(SaveAsIcon)

        CloseIcon = QtGui.QAction(QtGui.QIcon(
            'icons/closeFile.png'), 'Close', self)
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

        BotoneraInferior = QtGui.QHBoxLayout(widget_central)
        BotoneraInferior.addWidget(self.killGo)

        self.tabs.addTab(self.tab1, "Proceso")
        self.tabs.addTab(self.tab2, "Editor")
        self.tabs.addTab(self.tab3, "Tabla de secuencias")

        layoutTab1 = QtGui.QVBoxLayout(self.tabs)
        layoutTab1.addWidget(self.indicadorSecuencia)
        layoutTab1.addWidget(self.terminalOutput)
        layoutTab1.addWidget(self.killButton)
        layoutTab1.addWidget(self.cleanTerminalButton)
        self.tab1.setLayout(layoutTab1)

        layoutTab2 = QtGui.QVBoxLayout(self.tabs)
        layoutTab2.addWidget(self.crearToolbar())
        layoutTab2.addWidget(self.EditorDeTexto)
        self.tab2.setLayout(layoutTab2)

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
        self.tab3.setLayout(layoutTab3)

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
                action.triggered.connect(
                    lambda ignore, idt=subMenu: self.subMenuOptionClicked(idt))
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
        else:
            pass

    def openFile(self, fname):
        if not fname:
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname:
            with open(fname, 'r') as f:
                data = f.read()
                self.EditorDeTexto.setPlainText(data)
                self.is_new = False
                self.file_name = fname
        if fname[-3:] == ".py":
            self.pythonHighlighter.setDocument(self.EditorDeTexto.document())
        else:
            self.pythonHighlighter.setDocument(None)  # quitar higlight

    def openFileFromTree(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        filePath = self.model.filePath(indexItem)
        fname = str(filePath)
        self.openFile(fname)
        self.tabs.setCurrentWidget(self.tab2)

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
        if self.is_new:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText(
                u"Se modificó el documento desde la última vez que se guardó")
            msg.setInformativeText("desea guardar los cambios?")
            msg.setStandardButtons(QtGui.QMessageBox.Save |
                                   QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
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

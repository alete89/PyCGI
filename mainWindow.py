# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import Highlighter
import CodeEditor
import core
import tabla


class PyCGI(QtGui.QMainWindow):
    def __init__(self):
        super(PyCGI, self).__init__()
        self.is_new = True  # Flag para el archivo del editor
        self.file_name = ''  # Nombre del archivo del editor

        self.setWindowTitle(
            'PyCGI - Instituto de Tecnologia Nuclear Dan Beninson')
        self.treeWidget()
        self.crearTerminal()
        self.crearEditorDeTexto()
        self.VentanaPrincipal()
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

    def crearTerminal(self):
        self.font = QtGui.QFont()
        self.font.setFamily("Consolas, 'Courier New', monospace")
        self.font.setPointSize(11)  # size in points
        self.terminalDeTexto = QtGui.QTextEdit(self)
        self.terminalDeTexto.setReadOnly(True)
        self.terminalDeTexto.setFont(self.font)
        self.terminalDeTexto.setStyleSheet(
            "background-color: #585858; color: #fff")

        self.cursor = self.terminalDeTexto.textCursor()

    def crearEditorDeTexto(self):
        self.EditorDeTexto = CodeEditor.CodeEditor()
        self.highlighter = Highlighter.Highlighter(
            self.EditorDeTexto.document())

        self.EditorDeTexto.setFont(self.font)
        self.EditorDeTexto.setStyleSheet("background-color: #f1f1f1;")
        self.EditorDeTexto.setMinimumHeight(100)

    def VentanaPrincipal(self):

        self.setMinimumWidth(650)
        self.setMinimumHeight(600)

        self.killButton = QtGui.QPushButton("Kill process")
        self.killButton.clicked.connect(self.KillingProcess)

        self.cleanTerminalButton = QtGui.QPushButton("Clean terminal")
        self.cleanTerminalButton.clicked.connect(self.cleanTerminal)

        self.killGo = QtGui.QPushButton("Quit")
        self.killGo.clicked.connect(self.KillAndGo)

        self.terminalDeTexto.setMinimumHeight(100)
        self.cursor = QtGui.QTextCursor(self.terminalDeTexto.document())

        widget_central = QtGui.QWidget(self)
        self.setCentralWidget(widget_central)

        layout = QtGui.QVBoxLayout(widget_central)

        # No tendríamos que cargar las tabs dinamicamente también?
        self.tabs = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()

        BotoneraInferior = QtGui.QHBoxLayout(widget_central)
        BotoneraInferior.addWidget(self.killButton)
        BotoneraInferior.addWidget(self.cleanTerminalButton)
        BotoneraInferior.addWidget(self.killGo)

        self.tabs.addTab(self.tab1, "Proceso")
        self.tabs.addTab(self.tab2, "Editor")
        self.tabs.addTab(self.tab3, "Tabla de secuencias")

        layoutTabs1 = QtGui.QVBoxLayout(self.tabs)
        layoutTabs1.addWidget(self.terminalDeTexto)
        self.tab1.setLayout(layoutTabs1)

        layoutTabs2 = QtGui.QVBoxLayout(self.tabs)
        layoutTabs2.addWidget(self.theToolbar())
        layoutTabs2.addWidget(self.EditorDeTexto)
        self.tab2.setLayout(layoutTabs2)

        layoutTabs3 = QtGui.QVBoxLayout(self.tabs)

        self.tabla = tabla.Tabla()
        self.tabla.ShowDataSet(core.fullDataSet(), core.getHeaders())
        self.addRowButton = QtGui.QPushButton("Agregar fila")
        self.addRowButton.clicked.connect(self.tabla.addRow)
        self.saveTableButton = QtGui.QPushButton("Guardar cambios")
        self.saveTableButton.clicked.connect(
            lambda ignore, tabl=self.tabla: core.saveTable(tabl))

        self.updateMenuBarButton = QtGui.QPushButton("actualizar menu")
        self.updateMenuBarButton.clicked.connect(self.crearMenu)

        layoutTabs3.addWidget(self.tabla)
        layoutTabs3.addWidget(self.addRowButton)
        layoutTabs3.addWidget(self.saveTableButton)
        layoutTabs3.addWidget(self.updateMenuBarButton)
        self.tab3.setLayout(layoutTabs3)

        splitterHoriz = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitterHoriz.addWidget(self.tree)
        splitterHoriz.addWidget(self.tabs)
        splitterHoriz.setSizes([100, 500])

        layout.addWidget(splitterHoriz)

        layout.addLayout(BotoneraInferior)

        self.setLayout(BotoneraInferior)
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
        self.terminalDeTexto.append(text)

    def theToolbar(self):
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

    def KillingProcess(self):
        self.terminalDeTexto.append("Matando proceso")
        core.matarProceso(self)

    def cleanTerminal(self):
        self.terminalDeTexto.setText("")

    def KillAndGo(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            # core.matarProceso(self)
            exit()
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
            return fname
        return ''

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

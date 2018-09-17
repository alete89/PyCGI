# -*- coding: utf-8 -*-
import sys
import os
from PyQt4 import QtGui, QtCore
from ..logic import core
from . import Highlighter
from . import CodeEditor
from . import tabla
from . import treeView





class PyCGI(QtGui.QMainWindow):
    def __init__(self):
        super(PyCGI, self).__init__()
        self.setWindowTitle('PyCGI - Instituto de Tecnologia Nuclear Dan Beninson')
        self.treeWidget = treeView.TreeView(self)
        self.crearIndicadorSecuencia()
        self.crearTerminal()
        self.crearEditorDeTexto()
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
        self.indicadorSecuencia.setMaximumHeight(50)
        self.indicadorSecuencia.setFontWeight(75)  # 50 normal, 75 BOLD

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
        toolbar = self.addToolBar("Text editor - Toolbar")
        
        NewOne = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New', self)
        NewOne.setShortcut('Ctrl+n')
        NewOne.setStatusTip("New file")
        NewOne.triggered.connect(self.newEditorTab)
        toolbar.addAction(NewOne)
        
        OpenIcon = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        OpenIcon.setShortcut('Ctrl+o')
        OpenIcon.setStatusTip("Open file")
        OpenIcon.triggered.connect(self.openFile)
        toolbar.addAction(OpenIcon)
        
        SaveIcon = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        SaveIcon.setShortcut('Ctrl+s')
        SaveIcon.setStatusTip("Save file")
        SaveIcon.triggered.connect(self.saveDialog)
        toolbar.addAction(SaveIcon)
        
        SaveAsIcon = QtGui.QAction(QtGui.QIcon('icons/saveAs.png'), 'Save as', self)
        SaveAsIcon.setShortcut('Ctrl+g')
        SaveAsIcon.setStatusTip("Save as")
        SaveAsIcon.triggered.connect(self.saveAsDialog)
        toolbar.addAction(SaveAsIcon)
        
        CloseIcon = QtGui.QAction(QtGui.QIcon('icons/closeFile.png'), 'Close', self)
        CloseIcon.setShortcut('Ctrl+f4')
        CloseIcon.setStatusTip("Close file")
        CloseIcon.triggered.connect(self.CloseDialog)
        toolbar.addAction(CloseIcon)
        
        printAction = QtGui.QAction(QtGui.QIcon("icons/print.png"),"Print document",self)
        printAction.setStatusTip("Print document")
        printAction.setShortcut("Ctrl+P")
        printAction.triggered.connect(self.Print)        
        toolbar.addAction(printAction)
        
        previewAction = QtGui.QAction(QtGui.QIcon("icons/preview.png"),"Page view",self)
        previewAction.setStatusTip("Preview page before printing")
        previewAction.setShortcut("Ctrl+Shift+P")
        previewAction.triggered.connect(self.PageView)    
        toolbar.addAction(previewAction)

        findAction = QtGui.QAction(QtGui.QIcon("icons/find.png"),"Find",self)
        findAction.setStatusTip("Find words in your document")
        findAction.setShortcut("Ctrl+F")
        findAction.triggered.connect(self.EditorDeTexto.find_dialog)
        toolbar.addAction(findAction)
        
        cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"),"Cut to clipboard",self)
        cutAction.setStatusTip("Delete and copy text to clipboard")
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.Cut)
        toolbar.addAction(cutAction)

        copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
        copyAction.setStatusTip("Copy text to clipboard")
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.Copy)        
        toolbar.addAction(copyAction)
        
        pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste from clipboard",self)
        pasteAction.setStatusTip("Paste text from clipboard")
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.Paste)
        toolbar.addAction(pasteAction)

        undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
        undoAction.setStatusTip("Undo last action")
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.Undo)
        toolbar.addAction(undoAction)

        redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        redoAction.setStatusTip("Redo last undone thing")
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(self.Redo)
        toolbar.addAction(redoAction)
        
        indentAction = QtGui.QAction(QtGui.QIcon("icons/indent.png"),"Indent Area",self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.Indent)
        toolbar.addAction(indentAction)
        
        dedentAction = QtGui.QAction(QtGui.QIcon("icons/dedent.png"),"Dedent Area",self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.Dedent)
        toolbar.addAction(dedentAction)
        
        self.fontFamily = QtGui.QFontComboBox(self)
        self.fontFamily.currentFontChanged.connect(self.FontFamily)
        toolbar.addWidget(self.fontFamily)
        
        fontSize = QtGui.QComboBox(self)
        fontSize.setEditable(True)
        fontSize.setMinimumContentsLength(3)
        fontSize.activated.connect(self.FontSize)
        flist = [6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28]
        
        for i in flist:
            fontSize.addItem(str(i))
            
        toolbar.addWidget(fontSize)    
            
        return toolbar
        
        
    def FontSize(self, fsize):
        size = (int(fsize))
        font = QtGui.QFont()
        font.setFamily("Consolas, 'Courier New', monospace")
        font.setPointSize(size)
        self.EditorDeTexto.setFont(font)
        
    def FontFamily(self,fontF):
        font = QtGui.QFont()
        font.setFamily("Consolas, '"+str(fontF)+"', monospace")
        self.setFont(font)
        self.EditorDeTexto.setFont(font)        
        
    def Undo(self):
        self.EditorDeTexto.undo()

    def Redo(self):
        self.EditorDeTexto.redo()

    def Cut(self):
        self.EditorDeTexto.cut()

    def Copy(self):
        self.EditorDeTexto.copy()

    def Paste(self):
        self.EditorDeTexto.paste()

    def Indent(self):
        tab = "\t"
        cursor = self.EditorDeTexto.textCursor()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(end)
        cursor.movePosition(cursor.EndOfLine)
        end = cursor.position()

        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()


        while cursor.position() < end:
            global var

            print(cursor.position(),end)
            
            cursor.movePosition(cursor.StartOfLine)
            cursor.insertText(tab)
            cursor.movePosition(cursor.Down)
            end += len(tab)

            '''if cursor.position() == end:
                var +=1

            if var == 2:
                break'''

    def Dedent(self):
        tab = "\t"
        cursor = self.EditorDeTexto.textCursor()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(end)
        cursor.movePosition(cursor.EndOfLine)
        end = cursor.position()

        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()


        while cursor.position() < end:
            global var
            
            cursor.movePosition(cursor.StartOfLine)
            cursor.deleteChar()
            cursor.movePosition(cursor.EndOfLine)
            cursor.movePosition(cursor.Down)
            end -= len(tab)

            '''if cursor.position() == end:
                var +=1

            if var == 2:
                break'''

    def CursorPosition(self):
        line = self.EditorDeTexto.textCursor().blockNumber()
        col = self.EditorDeTexto.textCursor().columnNumber()
        linecol = ("Line: "+str(line)+" | "+"Column: "+str(col))
        self.status.showMessage(linecol)

    
        
    def PageView(self):
        preview = QtGui.QPrintPreviewDialog()
        preview.paintRequested.connect(self.PaintPageView)
        preview.exec_()

    def PaintPageView(self, printer):
        self.EditorDeTexto.print_(printer)
        
    def Print(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.EditorDeTexto.document().print_(dialog.printer())

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
        self.tabs = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        self.tabsInternas = QtGui.QTabWidget()
        
        #self.tabsInternas.tabCloseRequested.connect(self._closeTab())
        self.tabsInternas.setTabsClosable(True)

        self.tabsConfiguracion = QtGui.QTabWidget()
        self.configTab1 = QtGui.QWidget()
        self.configTab2 = QtGui.QWidget()
        self.configTab3 = QtGui.QWidget()
        BotoneraInferior = QtGui.QHBoxLayout(widget_central)
        BotoneraInferior.addWidget(self.killGo)
        self.tabs.addTab(self.tab1, "Process")
        self.tabs.addTab(self.tab2, "Text Editor")
        layoutTab1 = QtGui.QVBoxLayout(self.tabs)
        layoutTab1.addWidget(self.indicadorSecuencia)
        layoutTab1.addWidget(self.terminalOutput)
        layoutTab1.addWidget(self.killButton)
        layoutTab1.addWidget(self.cleanTerminalButton)
        self.tab1.setLayout(layoutTab1)
        layoutTab2 = QtGui.QVBoxLayout(self.tabs)
        layoutTab2.addWidget(self.crearToolbar())
        self.tab2.setLayout(layoutTab2)
        self.tabs.addTab(self.tab3, "Configuration")
        layoutTabsConfig = QtGui.QVBoxLayout(self.tab3)
        layoutTabsConfig.addWidget(self.tabsConfiguracion)
        self.tab3.setLayout(layoutTabsConfig)
        self.tabsConfiguracion.addTab(self.configTab1, "Sequence Table")
        self.tabsConfiguracion.addTab(self.configTab2, "Global Variables")
        self.tabsConfiguracion.addTab(self.configTab3, "Import")
        layoutTab2.addWidget(self.tabsInternas)
        layoutTab3 = QtGui.QVBoxLayout(self.tabs)
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
        splitterHoriz.addWidget(self.tabs)
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

    def newEditorTab(self, fname):
        if not fname:
            newTabName = 'New'
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
            msg.setText(u"The file has been modified.")
            msg.setInformativeText("Save the changes?")
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
        
    def _closeTab(self):
        #self.tabsInternas.setCurrentIndex(index)
        self.CloseDialog()
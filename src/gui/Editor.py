from PyQt4 import QtGui, QtCore
import CodeBox
import sys
import os
import findStringDialog

class Editor(QtGui.QWidget):
    def __init__(self):
        super(Editor, self).__init__()
        self.EditorDeTexto = CodeBox.CodeBox()
        self.layout = QtGui.QVBoxLayout(self)
        self.crearToolbar()
        self.layout.addWidget(CodeBox.CodeBox())
    
    def crearToolbar(self):
        toolbar = QtGui.QToolBar(self)
                
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
        findAction.triggered.connect(self.find_dialog)
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
        self.layout.addWidget(toolbar)
            
            
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


    def find_dialog(self):
        find = findStringDialog.Find(self)
        find.show()

        def handleFind():

            texto_buscado = find.buscar_textbox.toPlainText()
            print(texto_buscado)

            if find.is_case_sensitive == True and find.is_solo_palabras_completas == False:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively

            elif find.is_case_sensitive == False and find.is_solo_palabras_completas == False:
                flag = QtGui.QTextDocument.FindBackward

            elif find.is_case_sensitive == False and find.is_solo_palabras_completas == True:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindWholeWords

            elif find.is_case_sensitive == True and find.is_solo_palabras_completas == True:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively and QtGui.QTextDocument.FindWholeWords

            self.find(texto_buscado, flag)

        def handleReplace():
            texto_buscado = find.buscar_textbox.toPlainText()
            texto_reemplaza = find.reemplazar_textbox.toPlainText()

            text = self.toPlainText()

            newText = text.replace(texto_buscado, texto_reemplaza)

            self.clear()
            self.setPlainText(newText)

        find.find_button.clicked.connect(handleFind)
        find.replace_button.clicked.connect(handleReplace)

    def newEditorTab(self, fname):
        if not fname:
            newTabName = 'New'
        else:
            if os.path.isfile(fname):
                newTabName = str(fname)

        newTab = QtGui.QWidget()
        self.tabsInternas.addTab(newTab, str(newTabName))

        newTabLayout = QtGui.QVBoxLayout(newTab)
        newTabLayout.addWidget(CodeBox.CodeBox())
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
        # self.tabsInternas.setCurrentIndex(index)
        self.CloseDialog()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    txt = Editor()
    txt.show()
    sys.exit(app.exec_())
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import CodeBox
import sys
import os
import findStringDialog
import Highlighter

class Editor(QtGui.QWidget):
    def __init__(self):
        super(Editor, self).__init__()
        self.layout = QtGui.QVBoxLayout(self)
        self.currentFontSize = 11

        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeDialog)
        self.crearToolbar()
        self.layout.addWidget(self.tabWidget)
        
        self.newEditorTab()
        self.highlighter = Highlighter.Highlighter(self)

        
    
    def crearToolbar(self):
        toolbar = QtGui.QToolBar(self)

        newTab = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New', self)
        newTab.setShortcut('Ctrl+n')
        newTab.setStatusTip("New file")
        newTab.triggered.connect(self.newEditorTab)
        toolbar.addAction(newTab)
                
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
        CloseIcon.triggered.connect(self.closeDialog)
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
        
        fontSizeCombo = QtGui.QComboBox(self)
        fontSizeCombo.setEditable(False)
        fontSizeCombo.setMinimumContentsLength(3)
        flist = [6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28]
        
        for i in flist:
            fontSizeCombo.addItem(str(i))

        fontSizeCombo.activated[str].connect(self._changeFontSize)
        toolbar.addWidget(fontSizeCombo)    
        self.layout.addWidget(toolbar)

            
    def _changeFontSize(self, selectedSize):
        self.currentFontSize = int(selectedSize)
        for index in range(self.tabWidget.count()):
            self.tabWidget.widget(index).changeFontSize(int(selectedSize))




    def FontSize(self, fsize):
        size = (int(fsize))
        font = QtGui.QFont()
        font.setFamily("Consolas, 'Courier New', monospace")
        font.setPointSize(size)
        self.tabWidget.currentWidget().setFont(font)
        
    def FontFamily(self,fontF):
        font = QtGui.QFont()
        font.setFamily("Consolas, '"+str(fontF)+"', monospace")
        self.setFont(font)
        self.tabWidget.currentWidget().setFont(font)        
        
    def Undo(self):
        self.tabWidget.currentWidget().undo()

    def Redo(self):
        self.tabWidget.currentWidget().redo()

    def Cut(self):
        self.tabWidget.currentWidget().cut()

    def Copy(self):
        self.tabWidget.currentWidget().copy()

    def Paste(self):
        self.tabWidget.currentWidget().paste()

    def Indent(self):
        print ("indent unimplemented")

    def Dedent(self):
        print ("indent unimplemented")

    def CursorPosition(self):
        line = self.tabWidget.currentWidget().textCursor().blockNumber()
        col = self.tabWidget.currentWidget().textCursor().columnNumber()
        linecol = ("Line: "+str(line)+" | "+"Column: "+str(col))
        self.status.showMessage(linecol)
        
    def PageView(self):
        preview = QtGui.QPrintPreviewDialog()
        preview.paintRequested.connect(self.PaintPageView)
        preview.exec_()

    def PaintPageView(self, printer):
        self.tabWidget.currentWidget().print_(printer)
        
    def Print(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.tabWidget.currentWidget().document().print_(dialog.printer())

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

    def newEditorTab(self, fname=None):
        if not fname:
            newTabName = 'Untitled'
        else:
            if os.path.isfile(fname):
                newTabName = str(fname)

        newTab = CodeBox.CodeBox()
        newTab.changeFontSize(self.currentFontSize)
        index = self.tabWidget.addTab(newTab, str(newTabName))
        self.tabWidget.setCurrentIndex(index)
        return index


    def openFile(self, fname):
        if not fname:
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname:
            with open(fname, 'r') as f:
                tabIndex = self.newEditorTab(fname)
                tab = self.tabWidget.widget(tabIndex)
                data = f.read()
                tab.setPlainText(data)
                tab.is_dirty = False
                tab.file_name = fname
                self.tabWidget.setCurrentIndex(tabIndex)
        if fname[-3:] == ".py":
            self.highlighter.setDocument(tab.document())

    def saveAsDialog(self, tabIndex):
        tab_to_save = self.tabWidget.widget(tabIndex)
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        if name:
            textoParaGuardar = tab_to_save.toPlainText()
            with open(name, "w") as nFile:
                nFile.write(textoParaGuardar)
                tab_to_save.is_dirty = False
                tab_to_save.file_name = name
                self.tabWidget.setTabText(tabIndex,name)

    def saveDialog(self, tabIndex):
        tab_to_save = self.tabWidget.widget(tabIndex)
        if tab_to_save.is_dirty:
            self.saveAsDialog(tabIndex)
        else:
            textoParaGuardar = tab_to_save.toPlainText()
            with open(tab_to_save.file_name, "w") as nFile:
                nFile.write(textoParaGuardar)

    def removeTabFile(self):
        self.tabsInternas.removeTab(self.tabsInternas.currentIndex())

    def closeDialog(self, closeIndex):
        tab_to_close = self.tabWidget.widget(closeIndex)
        if tab_to_close.is_dirty:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText(u"The file has been modified.")
            msg.setInformativeText("Save the changes?")
            msg.setStandardButtons(QtGui.QMessageBox.Save |
                                   QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            resultado = msg.exec_()
            if resultado == QtGui.QMessageBox.Save:
                self.saveDialog(closeIndex)
            elif resultado == QtGui.QMessageBox.Discard:
                tab_to_close.deleteLater()
                self.tabWidget.removeTab(closeIndex)
            elif resultado == QtGui.QMessageBox.Cancel:
                return
        else:
            tab_to_close.deleteLater()
            self.tabWidget.removeTab(closeIndex)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    txt = Editor()
    txt.show()
    sys.exit(app.exec_())
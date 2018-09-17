# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from . import findStringDialog


class LineNumberArea(QtGui.QWidget):
    def __init__(self, editor):
        super(LineNumberArea, self).__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QtGui.QPlainTextEdit):
    def __init__(self):
        super(CodeEditor, self).__init__()
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.setTabStopWidth(32)

        font = QtGui.QFont()
        font.setFamily("Consolas, 'Courier New', monospace")
        font.setPointSize(11)
        self.setFont(font)
        self.setMinimumHeight(100)
        self.is_new = True
        self.file_name = ''

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(
                0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QtCore.QRect(
            cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        mypainter = QtGui.QPainter(self.lineNumberArea)
        mypainter.fillRect(event.rect(), QtCore.Qt.lightGray)
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(
            block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                mypainter.setPen(QtCore.Qt.black)
                mypainter.drawText(0, top, self.lineNumberArea.width(
                ), height, QtCore.Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QtGui.QTextEdit.ExtraSelection()
            lineColor = QtGui.QColor(QtCore.Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(
                QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    txt = CodeEditor()
    txt.show()
    sys.exit(app.exec_())

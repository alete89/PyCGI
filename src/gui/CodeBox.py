# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class LineNumberArea(QtGui.QWidget):
    def __init__(self, editor):
        super(LineNumberArea, self).__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)


class CodeBox(QtGui.QPlainTextEdit):
    def __init__(self):
        super(CodeBox, self).__init__()
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.setTabStopWidth(32)

        self.font = QtGui.QFont()
        self.font.setFamily("Consolas, 'Courier New', monospace")
        self.font.setPointSize(11)
        self.setFont(self.font)
        self.setMinimumHeight(100)
        self.is_dirty = False
        self.file_name = ""
        self.textChanged.connect(self._huboCambios)

    def _huboCambios(self):
        self.is_dirty = True

    def changeFontSize(self, size):
        self.font.setPointSize(size)
        self.setFont(self.font)

    def FontSize(self, fsize):
        size = (int(fsize))
        font = QtGui.QFont()
        font.setFamily("Consolas, 'Courier New', monospace")
        font.setPointSize(size)
        self.EditorDeTexto.setFont(font)

    def FontFamily(self, fontF):
        font = QtGui.QFont()
        font.setFamily("Consolas, '"+str(fontF)+"', monospace")
        self.setFont(font)
        self.EditorDeTexto.setFont(font)

    def CursorPosition(self):
        line = self.EditorDeTexto.textCursor().blockNumber()
        col = self.EditorDeTexto.textCursor().columnNumber()
        linecol = ("Line: "+str(line)+" | "+"Column: "+str(col))
        self.status.showMessage(linecol)

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


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    txt = CodeBox()
    txt.show()
    sys.exit(app.exec_())

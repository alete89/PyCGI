# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 14:06:45 2017

@author: manuel
"""

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#import numpy as np

class LineNumberArea(QWidget):

    def __init__(self, editor):
        super(LineNumberArea,self).__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return Qsize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super(CodeEditor, self).__init__()
        self.lineNumberArea = LineNumberArea(self)
        
        self.connect(self, SIGNAL('blockCountChanged(int)'), self.updateLineNumberAreaWidth)
        self.connect(self, SIGNAL('updateRequest(QRect,int)'), self.updateLineNumberArea)
        self.connect(self, SIGNAL('cursorPositionChanged()'), self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)


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
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

        cr = self.contentsRect();
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                    self.lineNumberAreaWidth(), cr.height()))


    def lineNumberAreaPaintEvent(self, event):
        mypainter = QPainter(self.lineNumberArea)

        mypainter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                mypainter.setPen(Qt.black)
                mypainter.drawText(0, top, self.lineNumberArea.width(), height,
                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(Qt.yellow).lighter(160)
            
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    txt = CodeEditor()
    txt.show()
    sys.exit(app.exec_())
# -*- encoding:utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
import collections
import copy
import sys


class paramForm(QtGui.QDialog):
    def __init__(self, param_list):
        super(paramForm, self).__init__()

        self.labels = {}
        self.texts = {}
        self.buttons = {}

        layout = QtGui.QGridLayout(self)
        counter = 0
        for row in param_list:
            for parametro in row:
                self.labels[counter] = QtGui.QLabel(parametro, self)
                print "el parametro es: " + parametro[:1]
                if parametro[:1] == "#":
                    self.texts[counter] = QtGui.QLineEdit(self)
                    self.buttons[counter] = QtGui.QPushButton("examinar")
                    self.buttons[counter].clicked.connect(lambda ignore, co=counter: self.getFileName(co))
                else:
                    self.texts[counter] = QtGui.QLineEdit(self)
                layout.addWidget(self.labels[counter], counter, 0)
                layout.addWidget(self.texts[counter], counter, 1)
                layout.addWidget(self.buttons[counter], counter, 2)
                counter += 1

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        layout.addWidget(buttons)
        self.setLayout(layout)
        self.setModal(True)

    @staticmethod
    def getNewParams(old_param_list):
        if not any(old_param_list):
            return (old_param_list, 1)  # 1 = Accept
        new_list = copy.deepcopy(old_param_list)
        dialog = paramForm(old_param_list)
        result = dialog.exec_()

        newCount = 0
        for listIndex, sublist in enumerate(old_param_list):
            if isinstance(sublist, collections.Iterable):
                for sublistIndex, _ in enumerate(sublist):
                    new_list[listIndex][sublistIndex] = str(dialog.texts[newCount].text())
                    newCount += 1
            else:
                new_list[listIndex] = str(dialog.texts[newCount].text())
                newCount += 1

        return (new_list, result == QDialog.Accepted)

    def getFileName(self, counter):
        filename = QtGui.QFileDialog.getOpenFileName()
        self.texts[counter].setText(filename)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    gui = paramForm.getNewParams(
        [['param1 de a', 'param2 de a'], ['param1 de b']])
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class Find(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.is_case_sensitive = False
        self.is_solo_palabras_completas = False

        self.initUI()

    def initUI(self):

        self.label_buscar = QtGui.QLabel("Search for: ", self)
        self.label_buscar.setStyleSheet("font-size: 15px; ")
        self.label_buscar.move(10, 10)

        self.buscar_textbox = QtGui.QTextEdit(self)
        self.buscar_textbox.move(10, 40)
        self.buscar_textbox.resize(250, 25)

        self.find_button = QtGui.QPushButton("Find", self)
        self.find_button.move(270, 40)

        self.label_reemplazar = QtGui.QLabel("Replace all by: ", self)
        self.label_reemplazar.setStyleSheet("font-size: 15px; ")
        self.label_reemplazar.move(10, 80)

        self.reemplazar_textbox = QtGui.QTextEdit(self)
        self.reemplazar_textbox.move(10, 110)
        self.reemplazar_textbox.resize(250, 25)

        self.replace_button = QtGui.QPushButton("Replace", self)
        self.replace_button.move(270, 110)

        self.case_sensitive_check = QtGui.QCheckBox("Case sensitive", self)
        self.case_sensitive_check.move(10, 160)
        self.case_sensitive_check.stateChanged.connect(self.case_sensitive)

        self.palabras_completas_check = QtGui.QCheckBox("Whole words only", self)
        self.palabras_completas_check.move(10, 190)
        self.palabras_completas_check.stateChanged.connect(self.solo_palabras_completas)

        self.close = QtGui.QPushButton("Close", self)
        self.close.move(270, 220)
        self.close.clicked.connect(self.hide)

        self.setGeometry(300, 300, 360, 250)

    def case_sensitive(self, state):
        if state == QtCore.Qt.Checked:
            self.is_case_sensitive = True
        else:
            self.is_case_sensitive = False

    def solo_palabras_completas(self, state):
        if state == QtCore.Qt.Checked:
            self.is_solo_palabras_completas = True
        else:
            self.is_solo_palabras_completas = False

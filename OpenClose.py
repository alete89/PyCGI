# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 12:54:12 2017

@author: manuel
"""

import sys
from PyQt4 import QtGui  
import subprocess

class OpenClose(QtGui.QMainWindow):
    def __init__(self):
        super(QtGui.QMainWindow,self).__init__()
        
        myQWidget = QtGui.QWidget()
        myBoxLayout = QtGui.QVBoxLayout()       
        
        Button_01 = QtGui.QPushButton("Actualizar PyCGI")
        Button_01.clicked.connect(self.callAnotherQMainWindow)
        myBoxLayout.addWidget(Button_01)        
        
        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)
        self.setWindowTitle('Actualizar PyCGI')
        
    def callAnotherQMainWindow(self):
        self.close()
        OpenPyCGI=subprocess.Popen(['python', 'PyCGI.py'], stdout=subprocess.PIPE)
        print OpenPyCGI.communicate()
            
    def Cancel(self):
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog_1 = OpenClose()
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_())
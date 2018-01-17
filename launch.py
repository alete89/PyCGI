import sys
from PyQt4 import QtGui
import mainWindow


def mainLoop():
    app = QtGui.QApplication(sys.argv)
    gui = mainWindow.PyCGI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    mainLoop()

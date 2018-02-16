import sys


if __name__ == '__main__':
    import src.gui.mainWindow as mainWindow
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    vp = mainWindow.PyCGI()
    vp.show()
    sys.exit(app.exec_())

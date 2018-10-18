from PyQt4 import QtGui


class MyTabBar(QtGui.QTabBar):
    def mouseReleaseEvent(self, event):
        if event.button() == 4:  # 4 = middleButtonMouse
            self.tabCloseRequested.emit(self.tabAt(event.pos()))
        #super(MyTabBar, self).mouseReleaseEvent(event)

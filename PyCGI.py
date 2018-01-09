# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 11:23:29 2017
@author: manuel
"""
import sys
import os
from PyQt4 import QtGui, QtCore, QtSql
import multiprocessing as mp
from Highlighter import *
from CodeEditor import *
from TablaMySQLEmbedded import *
from stringFinderV2 import *

import csvdb

idFilaTemp=''
lock=mp.Lock()

ds = csvdb.getDataFromCsv(os.getcwd() + r"\PyCGI\rs.csv")

class PyCGI(QtGui.QMainWindow):
    
    def __init__(self):
        Menu=[]
        super(PyCGI, self).__init__()
        self.VentanaPrincipal()
        # CSV
        # ds = csvdb.getDataFromCsv(os.getcwd() + r"\PyCGI\rs.csv")
        distinct = csvdb.distinct(ds,1)
        sortedList = csvdb.sortDataSet(distinct,4)
        menuList = csvdb.getColumn(sortedList,1)
        
		#CSV
        '''
        conexionMySQL(self)
        query.exec_("SELECT DISTINCT Menu FROM TablaDeSecuencias order by Coordenada")
        
        while(query.next()):
            MenuTemp=query.value(0).toString()
            Menu.append(MenuTemp)
        '''
        for menu in menuList:
            self.MenuPrincipal(menu)
        
    def MenuPrincipal(self, MenuTemp):
        # query = QtSql.QSqlQuery()
        idFila=[]
        SubMenu=[]
        Coordenada=[]
        '''
        query.exec_("SELECT DISTINCT SubMenu,Coordenada FROM TablaDeSecuencias where Menu='"+ str(MenuTemp) +"' and SubMenu is not null order by Coordenada")
#        db.commit()
        '''
        distinct = csvdb.distinct(ds,2)
        sortedList = csvdb.sortDataSet(distinct,4)
        subMenuFiltered = csvdb.dataFilter(sortedList,1,MenuTemp)
        subMenuList = csvdb.getColumn(subMenuFiltered,2)


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&'+str(MenuTemp))

        while(query.next()):
            SubMenuTemp=query.value(0).toString()
            idFilaTemp =query.value(1).toString()
            SubMenu.append(SubMenuTemp)
            idFila.append(idFilaTemp)
        i=0
        
        for SubMenuTemp in SubMenu:
            idFilaTemp = idFila[i]
            i = i + 1
            Action = QtGui.QAction(QtGui.QIcon(
                'exit.png'), '&' + str(SubMenuTemp), self)
            Action.setStatusTip(str(idFilaTemp) + " - " +
                                str(SubMenuTemp) + " - " + str(SubMenuTemp))
            
            # idFilaTemp siempre tendrá el último valor que tomó.
            Action.triggered.connect(lambda ignore, idt=idFilaTemp: self.PreEjecutarComandos(idt))
            self.statusBar()
            fileMenu.addAction(Action)
        
        self.setWindowTitle('PyCGI - Instituto de Tecnologia Nuclear Dan Beninson')    
        self.show()
        
    def VentanaPrincipal(self):
        
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.currentPath())
        tree = QtGui.QTreeView()
        tree.setModel(self.model)
        tree.setAnimated(True)
        tree.setIndentation(15)
        tree.setSortingEnabled(True)
        tree.setColumnWidth(0, 300)
        
        tree.doubleClicked.connect(self.OpenFileNow)
        
        self.toolbar = self.addToolBar('Editor de texto')

        OpenIcon=QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        OpenIcon.setShortcut('Ctrl+o')
        OpenIcon.triggered.connect(lambda: self.OpenDialog())
        self.toolbar.addAction(OpenIcon)
        
        SaveIcon=QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        SaveIcon.setShortcut('Ctrl+s')
        SaveIcon.triggered.connect(lambda: self.saveDialog())
        self.toolbar.addAction(SaveIcon) 
        
        SaveAsIcon=QtGui.QAction(QtGui.QIcon('icons/saveAs.png'), 'Save as', self)
        SaveAsIcon.setShortcut('Ctrl+g')
        SaveAsIcon.triggered.connect(lambda: self.saveAsDialog())
        self.toolbar.addAction(SaveAsIcon)
        
        CloseIcon=QtGui.QAction(QtGui.QIcon('icons/closeFile.png'), 'Close', self)
        CloseIcon.setShortcut('Ctrl+x')
        CloseIcon.triggered.connect(lambda: self.CloseDialog())
        self.toolbar.addAction(CloseIcon)        
        
        self.setWindowTitle('Toolbar')
        self.setMinimumWidth(650)
        self.setMinimumHeight(600)
        
        font = QtGui.QFont()
        font.setFamily('Monospace')
        font.setPointSize(11)
        
        self.killButton=QtGui.QPushButton("kill process")
        self.killButton.clicked.connect(lambda: self.KillingProcess())
        
        self.CleanTerminal=QtGui.QPushButton("clean")
        self.CleanTerminal.clicked.connect(lambda: self.CleaningTerminal())
        
        self.killGo=QtGui.QPushButton("kill and Go")
        self.killGo.clicked.connect(lambda: self.KillAndGo())

        self.Exe=QtGui.QPushButton("Exe")
        self.Exe.clicked.connect(lambda: self.EjecutarComandos())
        
        self.Update=QtGui.QPushButton("Update PyCGI")
        self.Update.clicked.connect(lambda: self.UpdateFunc())        
        
        self.terminalDeTexto = QtGui.QTextEdit(self)
        self.terminalDeTexto.setReadOnly(True)
        self.terminalDeTexto.setFont(font)
        self.terminalDeTexto.setStyleSheet("background-color: #585858; color: #fff")
        
        self.terminalDeProceso = QtGui.QTextEdit(self)
        
        self.terminalDeProceso.setReadOnly(True)
        self.terminalDeProceso.setFont(font)
        self.terminalDeProceso.setStyleSheet("background-color: #595999; color: #fff")
        
        global cursor
        cursor = self.terminalDeTexto.textCursor()
        
        self.EditorDeTexto = QtGui.QPlainTextEdit()
        self.EditorDeTexto = CodeEditor()
        self.highlighter = Highlighter(self.EditorDeTexto.document())
        
        self.EditorDeTexto.setFont(font)
        self.EditorDeTexto.setStyleSheet("background-color: #f1f1f1;")
        self.EditorDeTexto.setMinimumHeight(100)
        
        self.terminalDeTexto.setMinimumHeight(100)
        self.cursor = QtGui.QTextCursor(self.terminalDeTexto.document())
        
        widget_central = QtGui.QWidget(self)
        self.setCentralWidget(widget_central)
        
        layout = QtGui.QVBoxLayout(widget_central)
        
        tabs=QTabWidget()
        tab1=QWidget()
        tab2=QWidget()
        tab3=QWidget()
#        tab4=QWidget()
         
        BotoneraInferior=QtGui.QHBoxLayout(widget_central)
        BotoneraInferior.addWidget(self.killButton)
        BotoneraInferior.addWidget(self.CleanTerminal)
        BotoneraInferior.addWidget(self.Update)
        BotoneraInferior.addWidget(self.killGo)
        BotoneraInferior.addWidget(self.Exe)
        
        splitterVert = QtGui.QSplitter(QtCore.Qt.Vertical)

        splitterVert.addWidget(self.terminalDeTexto)
        splitterVert.addWidget(self.terminalDeProceso)
        splitterVert.setSizes([200,200])
        
        tabs.addTab(tab1,"Proceso")        
        tabs.addTab(tab2,"Editor")
        tabs.addTab(tab3,"Tabla de secuencias")
        
        layoutTabs1 = QtGui.QVBoxLayout(tabs)      
        layoutTabs1.addWidget(splitterVert)
        tab1.setLayout(layoutTabs1)

        layoutTabs2 = QtGui.QVBoxLayout(tabs)      
        layoutTabs2.addWidget(self.EditorDeTexto)
        tab2.setLayout(layoutTabs2)        
        
        layoutTabs3 = QtGui.QVBoxLayout(tabs)    
        
        self.form=TablaMySQLEmbedded()
        layoutTabs3.addWidget(self.form)
        tab3.setLayout(layoutTabs3)         

        splitterHoriz = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitterHoriz.addWidget(tree)
        splitterHoriz.addWidget(tabs)
        splitterHoriz.setSizes([100,500])
  
        layout.addWidget(splitterHoriz)
        
        layout.addLayout(BotoneraInferior)

        self.processRun = QtCore.QProcess(self)
        self.processRun.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.processRun.setReadChannelMode(QtCore.QProcess.MergedChannels)        
        
        self.processRun.readyRead.connect(self.dataReady)
        self.TermX = TerminalX(self)
        
        self.setLayout(BotoneraInferior)
        self.show()
        

        
    def UpdateFunc(self):
        from OpenClose import OpenClose
        self.close()
        self.dialog_01 = OpenClose()
        self.dialog_01.show()
        self.dialog_01.raise_()
        
    def KillAndGo(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            cursor.insertText('\n--- Process stopped by user ---')
            self.processRun.close()
            exit()
        else:
            pass
            
    def KillingProcess(self):
        cursor.insertText('\n --- Process stopped by user --- ')
        cursor.movePosition(cursor.End)
        self.processRun.close()
    
    def CleaningTerminal(self):
        self.terminalDeTexto.setText(" ")
        self.terminalDeProceso.setText(" ")
    
   
    def dataReady(self):
        salida='OUT: '+str(self.processRun.readAllStandardOutput()).strip()
        error='ERR: '+str(self.processRun.readAllStandardError()).strip()
        
        if salida:
            self.terminalDeTexto.append(salida)
        else:
            self.terminalDeTexto.append(error)
            

        return
        
        
    def OpenDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname:
            with open(fname, 'r') as f:
                data = f.read()
                self.EditorDeTexto.setPlainText(data)
                self.is_new = False
                self.file_name = fname
            print 'OpenDialog - fname: '+str(fname)
            return fname
    
    
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def OpenFileNow(self, index):
        
        indexItem = self.model.index(index.row(), 0, index.parent())
        filePath=self.model.filePath(indexItem)
        fname=str(filePath)
        print 'fname vale: '+str(fname)
        if fname:
            with open(fname, 'r') as f:
                data = f.read()
                self.EditorDeTexto.setPlainText(data)
                self.is_new = False
                self.file_name = fname
            print 'OpenDialog - fname: '+str(fname)
            return fname   
            
    def saveAsDialog(self):
        name = QtGui.QFileDialog.getSaveFileName(self,'Save File',str(self.file_name))
        if name:
            textoParaGuardar = self.EditorDeTexto.toPlainText()
            with open(name, "w") as file:
                file.write(textoParaGuardar)
                self.is_new = False
                self.file_name = name
        
    def saveDialog(self):
        if self.is_new:
            self.saveAsDialog()
        else:
            textoParaGuardar = self.EditorDeTexto.toPlainText()
            with open (self.file_name, "w") as file:
                file.write(textoParaGuardar)

    def CloseDialog(self):
        # TO DO preguntar si desea guardar antes de borrar.
        if self.is_new:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText(u"Se modificó el documento desde la última vez que se guardó")
            msg.setInformativeText("desea guardar los cambios?")
            msg.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            resultado = msg.exec_()
            print resultado
            if resultado == QtGui.QMessageBox.Save:
                self.saveDialog()
            elif resultado == QtGui.QMessageBox.Discard:
                pass
            elif resultado == QtGui.QMessageBox.Cancel:
                return

        self.EditorDeTexto.clear()
        self.is_new = True
        self.file_name = "NewFile"
        
    def PreEjecutarComandos(self,idFilaTemp):
        query = QtSql.QSqlQuery()
        global lock
        
        idCampo         =[]
        Menu            =[]
        SubMenu         =[]
        SubSubMenu      =[]
        Coordenada      =[]
        OrdenDeSecuencia=[]
        ModuloPython    =[]
        ComandoDeSistema=[]
        LoopDeProceso   =[]
        
        query.exec_("TRUNCATE TABLE TablaDeSecuenciasTemp")
        
        query.exec_("SELECT * FROM TablaDeSecuencias where Coordenada='"+str(idFilaTemp) +"' ORDER BY OrdenDeSecuencia")
        
        while(query.next()):
            
            idTemp                  = query.value(0).toString()
            MenuTemp                = query.value(1).toString()
            SubMenuTemp             = query.value(2).toString()
            SubSubMenuTemp          = query.value(3).toString()
            CoordenadaTemp          = query.value(4).toString()
            OrdenDeSecuenciaTemp    = query.value(5).toString()
            ModuloPythonTemp        = query.value(6).toString()
            ComandoDeSistemaTemp    = query.value(7).toString()
            LoopDeProcesoTemp       = query.value(8).toString()
            
            idCampo.append(idTemp)
            Menu.append(MenuTemp)
            SubMenu.append(SubMenuTemp)
            SubSubMenu.append(SubSubMenuTemp)
            Coordenada.append(CoordenadaTemp)
            OrdenDeSecuencia.append(OrdenDeSecuenciaTemp)
            ModuloPython.append(ModuloPythonTemp)
            ComandoDeSistema.append(ComandoDeSistemaTemp)
            LoopDeProceso.append(LoopDeProcesoTemp)

        i=0
        
        for OrdenDeSecuenciaTemp in OrdenDeSecuencia:
            
            idTemp                  = idCampo[i]
            MenuTemp                = Menu[i]
            SubMenuTemp             = SubMenu[i]
            SubSubMenuTemp          = SubSubMenu[i]
            CoordenadaTemp          = Coordenada[i]
            OrdenDeSecuenciaTemp    = OrdenDeSecuencia[i]
            ModuloPythonTemp        = ModuloPython[i]
            ComandoDeSistemaTemp    = ComandoDeSistema[i]
            LoopDeProcesoTemp       = LoopDeProceso[i] 
        
            
            if ComandoDeSistemaTemp:
                
                query.exec_("INSERT INTO TablaDeSecuenciasTemp (id,Menu,SubMenu,SubSubMenu,Coordenada,OrdenDeSecuencia,ModuloPython,ComandoDeSistema,LoopDeProceso) VALUES ('"+str(idTemp)+"','"+str(MenuTemp)+"','"+str(SubMenuTemp)+"','"+str(SubSubMenuTemp)+"','"+str(CoordenadaTemp)+"','"+str(OrdenDeSecuenciaTemp)+"','"+str(ModuloPythonTemp)+"','"+str(ComandoDeSistemaTemp)+"','"+str(LoopDeProcesoTemp)+"')")
                    
            i=i+1
            
#            Hasta aca lo unico que hice fue agarrar todos los datos de un 
#            proceso y cargarlos en una nueva tabla de secuencias pero temporal
            
#            Ahora tengo que tomar todos los strings que contiene indicaciones 
#            entre del tipo '(tipee su comando)' y armar con todos ellos un formulario
        print 'idFilaTemp: '+str(idFilaTemp)  
        
        self.CargaEntradas=stringFinderV2(idFilaTemp)
        self.CargaEntradas

    def EjecutarComandos(self):
        
        global lock

        idFilaTemp=''
        query = QtSql.QSqlQuery()
        query.exec_("SELECT DISTINCT Coordenada FROM TablaDeSecuenciasTemp")
        
        while(query.next()):
            idFilaTemp        =query.value(0).toString()

        ModuloPython        =[]
        ComandoDeSistema    =[]
        OrdenDeSecuencia    =[]
        LoopDeProceso       =[]
        
        query.exec_("SELECT ModuloPython,ComandoDeSistema,OrdenDeSecuencia,LoopDeProceso FROM TablaDeSecuenciasTemp where Coordenada='"+ str(idFilaTemp) +"' ORDER BY OrdenDeSecuencia")
        
        while(query.next()):
            
            ModuloPythonTemp        =query.value(0).toString()
            ComandoDeSistemaTemp    =query.value(1).toString()
            OrdenDeSecuenciaTemp    =query.value(2).toString()
            LoopDeProcesoTemp       =query.value(3).toString()
            
            ModuloPython.append(ModuloPythonTemp)
            ComandoDeSistema.append(ComandoDeSistemaTemp)
            OrdenDeSecuencia.append(OrdenDeSecuenciaTemp)
            LoopDeProceso.append(LoopDeProcesoTemp)

        i=0
        
        LoopDeProceso=[int(r) for r in LoopDeProceso]

        for OrdenDeSecuenciaTemp in OrdenDeSecuencia:
            
            Loop=LoopDeProceso[i]+1
            
            for LoopDeProcesoTemp in range(Loop):
                
                ComandoDeSistemaTemp=ComandoDeSistema[i]
                ModuloPythonTemp=ModuloPython[i]
                
                if ComandoDeSistemaTemp:
                    try: 
                        
                        cmd=str(ComandoDeSistemaTemp)
                        self.processRun.waitForFinished()
                        lock.acquire()
                        self.terminalDeProceso.append('>>> PROC '+str(OrdenDeSecuenciaTemp) 
                                                        +': '+str(ComandoDeSistemaTemp)+' - LOOP:'
                                                        +str(LoopDeProcesoTemp))
                                                        
                        self.terminalDeTexto.append('>>> PROC '+str(OrdenDeSecuenciaTemp) +':')
                        self.processRun.start(cmd)
                        self.connect(self.TermX,QtCore.SIGNAL("Activated ( QString ) "), self.dataReady)
                        
                        lock.release()
                        
                        QtCore.QCoreApplication.processEvents()
                        
                    except:

                        self.terminalDeProceso.append('>>> ERROR en el proceso '
                                                        +str(OrdenDeSecuenciaTemp) +': '
                                                        +str(ComandoDeSistemaTemp)+' - LOOP:'
                                                        +str(LoopDeProcesoTemp))     
                                                        
                        self.terminalDeTexto.append('>>> PROC: '+str(ComandoDeSistemaTemp)+'\n')
                        break

            i=i+1
            
class TerminalX(QtCore.QThread):
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)
          
    def run(self):
        self.emit(QtCore.SIGNAL("Activated( QString )"), self.dataReady)

def conexionMySQL(self):
    global query
    global db
    
    db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    db.setHostName('localhost')
    db.setDatabaseName('PyCGI')
    db.setUserName('root')
    db.setPassword('23101log')
    db.open()
    query = QtSql.QSqlQuery()
        
    return query

def main():
    app = QtGui.QApplication(sys.argv)
    ex = PyCGI()
    ex.show()
    
    proceso1=mp.Pool(4)
    proceso1.map(PyCGI.EjecutarComandos,idFilaTemp)    
    proceso1.close()
    proceso1.join()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
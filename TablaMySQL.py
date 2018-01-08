import sys
from PyQt4 import QtCore, QtGui, QtSql
import MySQLdb

def initializeModel(model):
    
    global Tabla
    Tabla=sys.argv[1] # Tomo el valor que se define en la tablazde secuencias

#    Tabla="TablaDeSecuencias" #VariablesGlobales1
    with open('db', 'r') as f:
        data = f.read()
    
    Campos=[]
    db = MySQLdb.connect(host   ="localhost",   # host
                         user   ="root",        # nombre de usuario
                         passwd = "23101log",    # password
                         db     ="PyCGI")       # Nombre de la base de datos     
    cur = db.cursor()
    cur.execute("show columns from " + str(Tabla))
    db.commit()
    
    for row in cur.fetchall():   
        CamposTemp=row[0]
        Campos.append(CamposTemp)
#        print("Campo: "+ str(CamposTemp))
    db.close()    
    
    model.setTable(Tabla)
    model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
    model.select()
    j=0
    
    for CamposTemp in Campos:
        
        CampoTitulo = QtGui.QLabel(str(CamposTemp))
        model.setHeaderData(j, QtCore.Qt.Horizontal, str(CamposTemp))
        
        j=j+1
	
def createView(title, model):
    
    view = QtGui.QTableView()
    view.setModel(model)
    view.setWindowTitle(title)
    view.setMinimumHeight(150)
    view.setMinimumWidth(1100)
    view.verticalScrollBar()
    view.resizeColumnsToContents()
    view.setSortingEnabled(True)
    return view
	
def addrow():
#    print model.rowCount()
    ret = model.insertRows(model.rowCount(), 1)
    print ret
	
def findrow(i):
    delrow = i.row()    

 
if __name__ == '__main__':
    
    global Tabla
    
    app = QtGui.QApplication(sys.argv)
    db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    db.setHostName('localhost')
    db.setDatabaseName('PyCGI')
    db.setUserName('root')
    db.setPassword('23101log')
    model = QtSql.QSqlTableModel()
    delrow = -1
    
    initializeModel(model)
    
    view1 = createView("PyCGI - Configuracion de la Tabla "+str(Tabla), model)
    view1.clicked.connect(findrow)
    	
    dlg = QtGui.QDialog()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(view1)
    
    layoutH = QtGui.QHBoxLayout()
    
    btn0 = QtGui.QPushButton("Add a row")
    btn0.clicked.connect(addrow)
    layoutH.addWidget(btn0)
    	
    btn1 = QtGui.QPushButton("Del a row")
    btn1.clicked.connect(lambda: model.removeRow(view1.currentIndex().row()))
    layoutH.addWidget(btn1)

    btn2 = QtGui.QPushButton("Close")

    btn2.clicked.connect(lambda: exit())
    layoutH.addWidget(btn2)    	
     
    layout.addLayout(layoutH)
    
    dlg.setLayout(layout)
    dlg.setWindowTitle("PyCGI - Configuracion de la Tabla "+str(Tabla))
    dlg.show()
    sys.exit(app.exec_())
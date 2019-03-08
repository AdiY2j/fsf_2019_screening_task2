import csv, codecs 
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from scipy.interpolate import interp1d
from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt, QTextStream
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtGui import QImage, QPainter, QPixmap
from PyQt5.QtCore import QFile, pyqtSlot
from PyQt5.QtGui import QKeySequence
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QAction, QRadioButton,QCheckBox, QActionGroup, QApplication, QFrame,
        QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QVBoxLayout,
        QWidget,QTextEdit,QGraphicsScene,QTableWidget,QFileDialog, QTabWidget,QHBoxLayout,QFormLayout,QLineEdit)

df = pd.DataFrame()


class Plot(QWidget):
    def __init__(self):
        super(Plot, self).__init__()
        loadUi('plt.ui', self)

        self.scatterPoint.clicked.connect(self.plotScatterPoints)
        self.smoothLine.clicked.connect(self.plotSmoothLines)
        self.linePlot.clicked.connect(self.plotLines)
        self.savePNG.clicked.connect(self.saveAsPNG)

        list1 = list(df)
        n = len(list1)
        print(list1)
        for j in range(0,n):
            self.selectX.addItem(list1[j])
            self.selectY.addItem(list1[j])

        
        

    def plotScatterPoints(self):
        if(not df.empty):
            print("points")
            x_axis = self.selectX.currentText()
            y_axis = self.selectY.currentText()
            if(x_axis != y_axis):
                x = df[x_axis]
                y = df[y_axis]
                plt.scatter(x,y)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title("Scatter Points")
                plt.savefig('foo.png', bbox_inches='tight')
                self.scene = QGraphicsScene()
                self.scene.addPixmap(QPixmap('foo.png'))
                self.graphicsView.setScene(self.scene)
                os.remove('foo.png')
                plt.close()
            

    def plotSmoothLines(self):
        if(not df.empty):
            x_axis = self.selectX.currentText()
            y_axis = self.selectY.currentText()
            if(x_axis != y_axis):
                x = df[x_axis]
                y = df[y_axis]
                x_new = np.linspace(x.min(), x.max(),500)
                f = interp1d(x, y, kind='quadratic')
                y_smooth=f(x_new)
                plt.plot (x_new,y_smooth)
                plt.scatter (x, y)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title("Scatter Points with Smooth Lines")
                plt.savefig('foo.png', bbox_inches='tight')
                self.scene = QGraphicsScene()
                self.scene.addPixmap(QPixmap('foo.png'))
                self.graphicsView.setScene(self.scene)
                os.remove('foo.png')
                plt.close()

    def plotLines(self):
        if(not df.empty):
            x_axis = self.selectX.currentText()
            y_axis = self.selectY.currentText()
            if(x_axis != y_axis):
                x = df[x_axis]
                y = df[y_axis]
                plt.plot(x,y)
                plt.scatter (x, y)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title("Simple Plot Lines")
                plt.savefig('foo.png', bbox_inches='tight')
                self.scene = QGraphicsScene()
                self.scene.addPixmap(QPixmap('foo.png'))
                self.graphicsView.setScene(self.scene)
                os.remove('foo.png')
                plt.close()

    def saveAsPNG(self):
        pass


i = 1    
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('hi.ui', self)
        self.recentFileActs = []
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.fileName = ""
        self.fname = "File"
        
        self.model =  QtGui.QStandardItemModel(self)
        self.tableView.setModel(self.model)
        self.tabWidget.tabCloseRequested.connect(self.closeMyTab)
        

        #self.createActions()
        self.setWindowTitle("PlotyPY")
        self.resize(700, 500)

        # Trigger Event for File Menu
        self.actionNew.triggered.connect(self.newFile)
        self.actionLoad.triggered.connect(self.loadFile)
        self.actionSave.triggered.connect(self.writeCsv)
        self.actionExit.triggered.connect(self.close)

        # Trigger Event for Edit Menu
        self.actionCopy.triggered.connect(self.copyByContext)
        self.actionPaste.triggered.connect(self.pasteByContext)
        self.actionCut.triggered.connect(self.cutByContext)
        self.actionAdd_Row.triggered.connect(self.addRow)
        self.actionDelete_Row.triggered.connect(self.removeRow)
        self.actionAdd_Column.triggered.connect(self.addColumn)
        self.actionDelete_Column.triggered.connect(self.removeColumn)
        
        # Trigger Event for Plot Menu
        self.actionPlot_Data.triggered.connect(self.plot)

    @pyqtSlot()
    def closeMyTab(self):
        global i
        i -= 1
        index = self.tabWidget.currentIndex()
        self.tabWidget.removeTab(index)

    def finishedEdit(self):
       self.tableView.resizeColumnsToContents()

    def newFile(self):
        #self.tabWidget.addTab(Plot(), "tab")
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.show()

    def plot(self):
        global i
        self.tabWidget.addTab(Plot(), "Plot")
        self.tabWidget.setCurrentIndex(i)
        i += 1
        	
    def save(self):
        if self.curFile:
            self.saveFile(self.curFile)
        else:
            self.saveAs()

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.loadFile(action.data())


    def loadFile(self, fileName):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV",
               (QtCore.QDir.homePath()), "CSV (*.csv *.tsv)")
 
        if fileName:
           global df
           df = pd.read_csv(fileName)
           print(fileName)
           ff = open(fileName, 'r')
           mytext = ff.read()
#            print(mytext)
           ff.close()
           f = open(fileName, 'r')
           with f:
               self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
               self.tabWidget.setTabText(self.tabWidget.currentIndex(),self.fname)
               if mytext.count(';') <= mytext.count('\t'):
                   reader = csv.reader(f, delimiter = ',')
                   self.model.clear()
                   for row in reader:    
                       items = [QtGui.QStandardItem(field) for field in row]
                       self.model.appendRow(items)
                   self.tableView.resizeColumnsToContents()
               else:
                   reader = csv.reader(f, delimiter = ',')
                   self.model.clear()
                   for row in reader:    
                       items = [QtGui.QStandardItem(field) for field in row]
                       self.model.appendRow(items)
                   self.tableView.resizeColumnsToContents()


    def writeCsv(self, fileName):
       # find empty cells
       if(not df.empty):
           for row in range(self.model.rowCount()):
               for column in range(self.model.columnCount()):
                   myitem = self.model.item(row,column)
                   if myitem is None:
                       item = QtGui.QStandardItem("")
                       self.model.setItem(row, column, item)
           fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", 
                       (QtCore.QDir.homePath() + "/" + self.fname + ".csv"),"CSV Files (*.csv)")
           if fileName:
               print(fileName)
               f = open(fileName, 'w')
               with f:
                   writer = csv.writer(f, delimiter = ',')
                   for rowNumber in range(self.model.rowCount()):
                       fields = [self.model.data(self.model.index(rowNumber, columnNumber),
                                        QtCore.Qt.DisplayRole)
                        for columnNumber in range(self.model.columnCount())]
                       writer.writerow(fields)
                   self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                   self.setWindowTitle(self.fname)


    def addRow(self):
        item = QtGui.QStandardItem("")
        self.model.appendRow(item)

    def removeRow(self):
       model = self.model
       indices = self.tableView.selectionModel().selectedRows() 
       for index in sorted(indices):
           model.removeRow(index.row())

 
    def removeColumn(self):
        model = self.model
        indices = self.tableView.selectionModel().selectedColumns() 
        for index in sorted(indices):
            model.removeColumn(index.column()) 
 
    def addColumn(self):
        count = self.model.columnCount()
        print (count)
        self.model.setColumnCount(count + 1)
        self.model.setData(self.model.index(0, count), "", 0)
        self.tableView.resizeColumnsToContents()
 
 
    def copyByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row,col)
            if myitem is not None:
                clip = QtWidgets.QApplication.clipboard()
                clip.setText(myitem.text())
 
    def pasteByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row,col)
            clip = QtWidgets.QApplication.clipboard()
            myitem.setText(clip.text())
 
    def cutByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row,col)
            if myitem is not None:
                clip = QtWidgets.QApplication.clipboard()
                clip.setText(myitem.text())
                myitem.setText("")


    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()

    def Undo(self):
        pass

    def Redo(self):
        pass

    def selectData(self):
        pass


    
def stylesheet(self):
       return """
       QTableView
       {
border: 1px solid grey;
border-radius: 0px;
font-size: 12px;
background-color: #f8f8f8;
selection-color: white;
selection-background-color: #00ED56;
       }
 
QTableView QTableCornerButton::section {
    background: #D6D1D1;
    border: 1px outset black;
}
 
QPushButton
{
font-size: 11px;
border: 1px inset grey;
height: 24px;
width: 80px;
color: black;
background-color: #e8e8e8;
background-position: bottom-left;
} 
 
QPushButton::hover
{
border: 2px inset goldenrod;
font-weight: bold;
color: #e8e8e8;
background-color: green;
} 
"""

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('My Window')
    main = MainWindow()
    main.setMinimumSize(820, 300)
    main.setGeometry(50,50,1200,700)
    main.setWindowTitle("CSV Viewer")
    main.show()
    sys.exit(app.exec_())

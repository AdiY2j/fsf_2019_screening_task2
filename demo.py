# Import all the necessary packages
import csv, codecs 
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from scipy.interpolate import interp1d
from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt, QTextStream, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtGui import QImage, QPainter, QPixmap, QKeySequence
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QAction, QRadioButton,QCheckBox, QActionGroup, QAbstractItemView, QApplication, QFrame,
        QLabel, QMainWindow,QStyleFactory, QMenu, QMessageBox, QSizePolicy, QVBoxLayout,
        QWidget,QTextEdit,QGraphicsScene,QTableWidget,QFileDialog, QTabWidget,QHBoxLayout,QFormLayout,QLineEdit)

df = pd.DataFrame()

# Plot class which contains 3 methods: 1] Scatter Points, 2] Smooth Lines and 3] Line Plot
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
        if(df.empty):
            self.selectX.clear()
            self.selectY.clear()
        else:
            for j in range(0,n):
                self.selectX.addItem(list1[j])
                self.selectY.addItem(list1[j])

        
    # Plotting Scatter Points
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
            else:
                QMessageBox.about(self, 'Important', "X and Y axis cannot be same !!")
        else:
            QMessageBox.about(self, 'Important', "Please Load Data First !!")
        
            
    # Plotting Scatter Points with Smooth Lines
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
            else:
                QMessageBox.about(self, 'Important', "X and Y axis cannot be same !!")
        else:
            QMessageBox.about(self, 'Important', "Please Load Data First !!")
        
        
    # Plotting Simple Line Plots
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
            else:
                QMessageBox.about(self, 'Important', "X and Y axis cannot be same !!")
        else:
            QMessageBox.about(self, 'Important', "Please Load Data First !!")
                

    def saveAsPNG(self):
        if(not df.empty):
            imgPath, _ = QtWidgets.QFileDialog.getSaveFileName(self.graphicsView, "Save Image", 
                        "Image.png","PNG (*.png)")
            if(imgPath is not None):
                print("save")
                pixMap = QPixmap()
                pixMap = self.graphicsView.grab()
                pixMap.save(imgPath)

        else:
            QMessageBox.about(self, 'Important', "Please Load Data First !!")
        


i = 1    
class MainWindow(QMainWindow):
    windowList = []
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
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
        self.actionSave_as_PNG.triggered.connect(self.saveasPNG)
        self.actionAdd_Row_3.triggered.connect(self.addRow)
        self.actionRemove_Row.triggered.connect(self.removeRow)
        self.actionAdd_Column_3.triggered.connect(self.addColumn)
        self.actionRemove_Column.triggered.connect(self.removeColumn)
        self.actionExit.triggered.connect(self.close)

        # Trigger Event for Edit Menu
        self.actionEdit_Data.triggered.connect(self.editData)
        self.actionCopy.triggered.connect(self.copyByContext)
        self.actionPaste.triggered.connect(self.pasteByContext)
        self.actionCut.triggered.connect(self.cutByContext)
        
        
        # Trigger Event for Plot Menu
        self.actionPlot_Data.triggered.connect(self.plot)

    @pyqtSlot()
    def saveasPNG(self):
        if((self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            Plot().saveAsPNG()
        else:
            pass

    def closeMyTab(self):
        global i,df
        i -= 1
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            df = df.iloc[0:0]
            if QMessageBox.question(None, '', "Are you sure you want to quit?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No) == QMessageBox.Yes:
                self.close()
            else:
                pass
        else:
            index = self.tabWidget.currentIndex()
            self.tabWidget.removeTab(index)

    def finishedEdit(self):
       self.tableView.resizeColumnsToContents()


    def newFile(self):
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.show()

    def plot(self):
        global i
        self.tabWidget.addTab(Plot(), "Plot")
        self.tabWidget.setCurrentIndex(i)
        i += 1
        	

    def editData(self, fileName):
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            if(not df.empty):
                self.tableView.setEditTriggers(QAbstractItemView.EditKeyPressed |
                                 QAbstractItemView.DoubleClicked)
        else:
            pass



    def loadFile(self, fileName):
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV",
                   (QtCore.QDir.homePath()), "CSV (*.csv *.tsv)")
 
            if fileName:
                global df
                df = pd.read_csv(fileName)
                print(fileName)
                ff = open(fileName, 'r')
                mytext = ff.read()
                ff.close()
                f = open(fileName, 'r')
                with f:
                    self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                    self.tabWidget.setTabText(self.tabWidget.currentIndex(),self.fname)
                    reader = csv.reader(f, delimiter = ',')
                    self.model.clear()
                    for row in reader:    
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)
                    self.tableView.resizeColumnsToContents()
        else:
            pass


    def writeCsv(self, fileName):
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            global df
            if(not df.empty):
                fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", self.fname, "CSV (*.csv *.tsv)")
                if fileName:
                    with open(fileName, 'w', newline='') as stream:
                        print("saving", fileName)
                        writer = csv.writer(stream, delimiter=',')
                        for row in range(self.model.rowCount()):
                            rowdata = []
                            for column in range(self.model.columnCount()):
                                item = self.model.item(row, column)
                                if item is not None:
                                    rowdata.append(item.text())
                                else:
                                    rowdata.append('')
                            writer.writerow(rowdata)
                        self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                    df = pd.read_csv(fileName)
        else:
            pass


    def addRow(self):
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            item = QtGui.QStandardItem("")
            self.model.appendRow(item)
        else:
            pass

    def removeRow(self):
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            model = self.model
            indices = self.tableView.selectionModel().selectedRows() 
            for index in sorted(indices):
                model.removeRow(index.row())
        else:
            pass

 
    def removeColumn(self):
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            model = self.model
            indices = self.tableView.selectionModel().selectedColumns() 
            for index in sorted(indices):
                model.removeColumn(index.column())
        else:
            pass
 
    def addColumn(self):
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            count = self.model.columnCount()
            print (count)
            self.model.setColumnCount(count + 1)
            self.model.setData(self.model.index(0, count), "", 0)
            self.tableView.resizeColumnsToContents()
        else:
            pass
 
 
    def copyByContext(self, event):
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            for i in self.tableView.selectionModel().selection().indexes():
                row = i.row()
                col = i.column()
                myitem = self.model.item(row,col)
                if myitem is not None:
                    clip = QtWidgets.QApplication.clipboard()
                    clip.setText(myitem.text())
        else:
            pass
 
    def pasteByContext(self, event):
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            for i in self.tableView.selectionModel().selection().indexes():
                row = i.row()
                col = i.column()
                myitem = self.model.item(row,col)
                clip = QtWidgets.QApplication.clipboard()
                myitem.setText(clip.text())
        else:
            pass
 
    def cutByContext(self, event):
        if(not (self.tabWidget.tabText(self.tabWidget.currentIndex())) == "Plot"):
            for i in self.tableView.selectionModel().selection().indexes():
                row = i.row()
                col = i.column()
                myitem = self.model.item(row,col)
                if myitem is not None:
                    clip = QtWidgets.QApplication.clipboard()
                    clip.setText(myitem.text())
                    myitem.setText("")
        else:
            pass


    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('My Window')
    app.setStyle(QStyleFactory.create("Windows"))
    main = MainWindow()
    main.setMinimumSize(820, 300)
    main.setGeometry(50,50,1200,700)
    main.setWindowTitle("QtPy")
    main.show()
    sys.exit(app.exec_())

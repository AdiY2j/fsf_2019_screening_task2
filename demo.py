import csv, codecs 
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt, QTextStream
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QFile, pyqtSlot
from PyQt5.QtGui import QKeySequence
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QAction, QRadioButton,QCheckBox, QActionGroup, QApplication, QFrame,
        QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QVBoxLayout,
        QWidget,QTextEdit,QTableWidget,QFileDialog, QTabWidget,QHBoxLayout,QFormLayout,QLineEdit)


class MainWindow(QMainWindow):
    MaxRecentFiles = 5
    windowList = []

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('hi.ui', self)
        self.recentFileActs = []
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.fileName = ""
        self.fname = "File"
        self.df = pd.DataFrame()
        self.model =  QtGui.QStandardItemModel(self)
        self.tableView.setModel(self.model)

        '''
        print(self.tabWidget.currentIndex())
        if(self.tabWidget.currentIndex() == 0):
            self.tableView = QtWidgets.QTableView(self)
            self.tableView.setStyleSheet(stylesheet(self))
            self.tableView.setModel(self.model)
            self.tableView.horizontalHeader().setStretchLastSection(True)
            self.tableView.setShowGrid(True)
            self.tableView.setGeometry(10, 50, 1180, 645)
            self.model.dataChanged.connect(self.finishedEdit)
        '''	
        
        #self.createMenus()
        #self.statusBar()
        

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
        self.menuPlot.triggered.connect(self.newFile)

    @pyqtSlot()
    def finishedEdit(self):
       self.tableView.resizeColumnsToContents()

    def newFile(self):
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.show()
        	
    def save(self):
        if self.curFile:
            self.saveFile(self.curFile)
        else:
            self.saveAs()

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.loadFile(action.data())


    def createActions(self):
        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
                statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QAction("&Load CSV", self, shortcut=QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.loadFile)

        self.saveAct = QAction("&Save CSV", self, shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.writeCsv)

        for i in range(MainWindow.MaxRecentFiles):
            self.recentFileActs.append(
                    QAction(self, visible=False,
                            triggered=self.openRecentFile))

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application",
                triggered=QApplication.instance().closeAllWindows)
        
        self.addRowAct = QAction("&Add Row", self, 
                statusTip="Add Row to CSV",
                triggered=self.addRow)

        self.delRowAct = QAction("&Delete Row", self, 
                statusTip="Delete Row from CSV",
                triggered=self.removeRow)

        self.addColAct = QAction("&Add Column", self, 
                statusTip="Add Column to CSV",
                triggered=self.addColumn)

        self.delColAct = QAction("&Delete Column", self, 
                statusTip="Delete Column from CSV",
                triggered=self.removeColumn)

        self.clearAct = QAction("&Clear", self, 
                statusTip="Clear Window",
                triggered=self.clearList)

        self.plotScatterPointAct = QAction("&Scatter Points", self, 
                statusTip="Plot using Scatter Points",
                triggered=self.plotScatterPoints)

        self.plotSmoothLineAct = QAction("&Smooth Lines", self, 
                statusTip="Plot Scatter Points using Smooth Lines",
                triggered=self.plotSmoothLines)

        self.plotLineAct = QAction("&Line Plot", self, 
                statusTip="Plot using Simple Lines",
                triggered=self.plotLines)
        

        self.copyAct = QAction("&Copy", self, shortcut=QKeySequence.Copy,
                statusTip="Copy Data", triggered=self.copyByContext)

        self.pasteAct = QAction("&Paste", self, shortcut=QKeySequence.Paste,
                statusTip="Paste Data", triggered=self.pasteByContext)

        self.selectAct = QAction("&Select Data", self, shortcut="Ctrl+K",
                statusTip="Select existing data", triggered=self.selectData)


        self.cutAct = QAction("&Cut", self, shortcut=QKeySequence.Cut,
                statusTip="Delete and copy text to clipboard", triggered=self.cutByContext)


    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.separatorAct = self.fileMenu.addSeparator()
        for i in range(MainWindow.MaxRecentFiles):
            self.fileMenu.addAction(self.recentFileActs[i])
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.updateRecentFileActions()

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.clearAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.addRowAct)
        self.editMenu.addAction(self.delRowAct)
        self.editMenu.addAction(self.addColAct)
        self.editMenu.addAction(self.delColAct)
        self.editMenu.addAction(self.selectAct)

        self.plotMenu = self.menuBar().addMenu("&Plot")
        self.plotMenu.addAction(self.plotScatterPointAct)
        self.plotMenu.addAction(self.plotSmoothLineAct)
        self.plotMenu.addAction(self.plotLineAct)

        self.menuBar().addSeparator()



    def loadFile(self, fileName):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV",
               (QtCore.QDir.homePath()), "CSV (*.csv *.tsv)")
 
        if fileName:
           self.df = pd.read_csv(fileName)
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
       if(not self.df.empty):
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
 
    def clearList(self):
        self.df = self.df.iloc[0:0]
        self.setWindowTitle("CSV Viewer")
        self.model.clear()
 
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


    def plotScatterPoints(self):
        if(not self.df.empty):
            x = self.df['No']
            y = self.df['Price']
            plt.scatter(x,y)
            plt.xlabel("Day")
            plt.ylabel("Price")
            plt.title("Scatter Points")
            plt.show()

    def plotSmoothLines(self):
        if(not self.df.empty):
            x = self.df['No']
            y = self.df['Price']
            x_new = np.linspace(x.min(), x.max(),500)
            f = interp1d(x, y, kind='quadratic')
            y_smooth=f(x_new)
            plt.plot (x_new,y_smooth)
            plt.scatter (x, y)
            plt.xlabel("Day")
            plt.ylabel("Price")
            plt.title("Scatter Points with Smooth Lines")
            plt.show()

    def plotLines(self):
        if(not self.df.empty):
            x = self.df['No']
            y = self.df['Price']
            plt.plot(x,y)
            plt.xlabel("Day")
            plt.ylabel("Price")
            plt.title("Simple Plot Lines")
            plt.show()
 
    def deleteRowByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            self.model.removeRow(row)
            print("Row " + str(row) + " deleted")
            self.tableView.selectRow(row)
 
    def addRowByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row() + 1
            self.model.insertRow(row)
            print("Row at " + str(row) + " inserted")
            self.tableView.selectRow(row)
 
    def addRowByContext2(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            self.model.insertRow(row)
            print("Row at " + str(row) + " inserted")
            self.tableView.selectRow(row)
 
    def addColumnBeforeByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            col = i.column()
            self.model.insertColumn(col)
            print("Column at " + str(col) + " inserted")
 
    def addColumnAfterByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            col = i.column() + 1
            self.model.insertColumn(col)
            print("Column at " + str(col) + " inserted")
 
    def deleteColumnByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            col = i.column()
            self.model.removeColumn(col)
            print("Column at " + str(col) + " removed")
 
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


    def setCurrentFile(self, fileName):
        self.curFile = fileName
        if self.curFile:
            self.setWindowTitle("%s - Recent Files" % self.strippedName(self.curFile))
        else:
            self.setWindowTitle("Recent Files")

        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[MainWindow.MaxRecentFiles:]

        settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.updateRecentFileActions()

    def updateRecentFileActions(self):
        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        numRecentFiles = min(len(files), MainWindow.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, MainWindow.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))

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

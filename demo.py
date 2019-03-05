import csv, codecs 
import os
from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt, QTextStream
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QFrame,
        QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QVBoxLayout,
        QWidget,QTextEdit,QTableWidget,QFileDialog)


class MainWindow(QMainWindow):
    MaxRecentFiles = 5
    windowList = []

    def __init__(self):
        super(MainWindow, self).__init__()

        self.recentFileActs = []

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.statusBar()

        self.setWindowTitle("PlotyPY")
        self.resize(700, 500)

    def newFile(self):
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.show()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if fileName:
            self.loadFile(fileName)
        	
    def save(self):
        if self.curFile:
            self.saveFile(self.curFile)
        else:
            self.saveAs()

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            self.saveFile(fileName)

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.loadFile(action.data())


    def createActions(self):
        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
                statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QAction("&Open...", self, shortcut=QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction("Save &As...", self,
                shortcut=QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.saveAs)

        for i in range(MainWindow.MaxRecentFiles):
            self.recentFileActs.append(
                    QAction(self, visible=False,
                            triggered=self.openRecentFile))

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application",
                triggered=QApplication.instance().closeAllWindows)
        
        self.editAct = QAction("&Edit Data", self, shortcut="Ctrl+E",
                statusTip="Edit Existing Data",
                triggered=self.editData)

        self.copyAct = QAction("&Copy", self, shortcut=QKeySequence.Copy,
                statusTip="Copy Data", triggered=self.copyData)

        self.pasteAct = QAction("&Paste", self, shortcut=QKeySequence.Paste,
                statusTip="Paste Data", triggered=self.pasteData)

        self.selectAct = QAction("&Select Data", self, shortcut="Ctrl+K",
                statusTip="Select existing data", triggered=self.selectData)

        self.plotAct = QAction("&Plot Data...", self, shortcut="Ctrl+Shift+P",
                statusTip="Plot existing data", triggered=self.plotData)

        self.redoAct = QAction("&Redo", self, shortcut=QKeySequence.Redo,
                statusTip="Redo last undone thing", triggered=self.Redo)

        self.undoAct = QAction("&Undo", self, shortcut=QKeySequence.Undo,
                statusTip="Undo last action", triggered=self.Undo)

        self.cutAct = QAction("&Cut", self, shortcut=QKeySequence.Cut,
                statusTip="Delete and copy text to clipboard", triggered=self.Cut)


    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.separatorAct = self.fileMenu.addSeparator()
        for i in range(MainWindow.MaxRecentFiles):
            self.fileMenu.addAction(self.recentFileActs[i])
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.updateRecentFileActions()

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.editAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addAction(self.selectAct)

        self.plotMenu = self.menuBar().addMenu("&Plot")
        self.plotMenu.addAction(self.plotAct)

        self.menuBar().addSeparator()



    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open( QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Recent Files",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.textEdit.setPlainText(instr.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QFile(fileName)
        if not file.open( QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Recent Files",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return

        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)

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
        self.textEdit.undo()

    def Redo(self):
        self.textEdit.redo()

    def Cut(self):
        self.textEdit.cut()

    def editData(self):
        pass

    def copyData(self):
        self.textEdit.copy()

    def pasteData(self):
        self.textEdit.paste()

    def selectData(self):
        pass

    def plotData(self):
        pass

    


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

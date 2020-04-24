import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QCheckBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class subwindow(QWidget):
    def createWindow(self,WindowWidth,WindowHeight):
       parent=None
       super(subwindow,self).__init__(parent)
       selt.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
       self.resize(WindowWidth,WindowHeight)

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.setFixedWidth(120)
        
        # Create a button in the window
        self.button = QPushButton('Show text', self)

        hbox = QHBoxLayout()
        #hbox.addStretch(1)
        hbox.addWidget(self.textbox)
        hbox.addWidget(self.button)
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignTop)
        self.vbox.addLayout(hbox)


        self.setLayout(self.vbox)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.setWindowTitle('cellular automata')   
        self.setGeometry(1000, 1000, 1000, 1000)
        self.show()
        
    def createsASubwindow(self):
         self.mySubwindow=subwindow()
         self.mySubwindow.createWindow(500,400)
         self.mySubwindow.setWindowTitle('cell plot data')
       #make pyqt items here for your subwindow
         self.mySubwindow.button = QtGui.QPushButton(self.mySubwindow)

         self.mySubwindow.show() 
    # take in number to represent cells.
    #  
    @pyqtSlot()
    def on_click(self):
        cellSize = self.textbox.text()
        QMessageBox.question(self, '', "Ok. your Automata will have " + cellSize + " cells.", QMessageBox.Ok, QMessageBox.Ok)
        cellsizeint = int(cellSize)
        hbox = QHBoxLayout()
        for i in range(0,cellsizeint): 
            hbox.addWidget(QCheckBox()) 
        self.vbox.addLayout(hbox)
        #self.up1.show()
        #alphabet = QLineEdit()
        #alphabet.move(20, 70)
        #alphabet.resize(280, 40)
        #self.textbox.setText("")
        #box = QCheckBox
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



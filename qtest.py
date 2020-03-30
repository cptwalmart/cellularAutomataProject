import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 textbox - pythonspot.com'
        self.left = 1000
        self.top = 1000
        self.width = 1000
        self.height = 1000
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
        
        # Create a button in the window
        self.button = QPushButton('Show text', self)
        self.button.move(20,80)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
      
    # take in number to represent cells.
    #  
    @pyqtSlot()
    def on_click(self):
        cellSize = self.textbox.text()
        QMessageBox.question(self, '', "Ok. your Automata will have " + cellSize + " cells.", QMessageBox.Ok, QMessageBox.Ok)
        int(cellSize)
        g5 = ["o"] * cellSize
        for i in range(g5): 
          
        
        self.up1 = QCheckBox("o", self)
        self.up1.move(20, 140)
        self.up1.resize(200, 50)
        
        self.up1.show()
        alphabet = QLineEdit()
        alphabet.move(20, 70)
        alphabet.resize(280, 40)
        #self.textbox.setText("")
        #box = QCheckBox
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

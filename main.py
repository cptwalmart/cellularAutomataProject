"""
This project was created for COSC 425 for use by Salisbury University.
Programmers: Joseph Craft, Sean Dunn, Malik Green, Kevin Koch
COSC 425 Cellular Automata Project
"""


import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication
import MplCanvas as mpl
import MainWindow as mw
"""
Classes MplCanvas and MainWindow are needed to run the GUI
The CellularAutomata class is used for the logic of the program
"""
app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')
w = mw.MainWindow()
app.exec_()
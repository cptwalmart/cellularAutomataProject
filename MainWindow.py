"""
This project was created for COSC 425/426 for use by Salisbury University.
Programmers: Joseph Craft, Sean Dunn, Malik Green, Kevin Koch
COSC 425/426 Cellular Automata Project

******************************************

This is the GUI file of the project, primarily using the PyQt5 library, as well as matplotlib for graphing.
The main computational file CellularAutomata.py is imported and called throughout to incorporate functions into the GUI.
"""

import MplCanvas as mpl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt, QTextStream
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QTextEdit, QMessageBox, QLabel, QGroupBox, QToolBar, QMenu
from PyQt5.QtWidgets import QDialog, QFileDialog, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from sympy import *     # For nullspace
import numpy as np
import CellularAutomata
import AutomataStats as stats
import random

### Cached Prime Numbers ###
# initialising primes
minPrime = 0
maxPrime = 1000
cached_primes = [i for i in range(minPrime,maxPrime) if isprime(i)]
### Cached Prime Numbers ###

"""
This class represents the main window of the GUI. As such, all of the GUI is accessed here, as well as the main computational file CellularAutomata.py.
"""
class MainWindow(QtWidgets.QMainWindow):
    """
    Initialization of variables and GUI.
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)


        ### Cellular Automata ###
        self.CA = CellularAutomata.CellularAutomata()
        ### ###

        # Set Window Elements
        self.title = 'PyQt5 - Cellular Automata'
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        # Display cellular automata as graphs in the GUI
        self.canvas = mpl.MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.axes.matshow(self.CA.get_cellular_automata())

        #### Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second ###
        self.toolbar = NavigationToolbar(self.canvas, self)
        ### --- ###

        # Flag to determine which matrix certain functions work with.
        # Default is base matrix.
        self.activeMatrixLabel = 'base'

        """
        self.activeMatrix and self.lastMatrix are variables to hold the currently active matrix and the most recently used matrix, respectively.
        The important distinction between these two variables is the active matrix will always be a standard matrix, which is to say it will never be a calculation matrix, such as rref or nullspace.
        """
        self.activeMatrix = []
        self.lastMatrix = []

        # Create output file
        self.textEdit = QTextEdit()
        self.outputFile = ''

        """ Menu Bar Creation """
        menubar = self.menuBar()

        # Adds a 'File' tab, which is placed in the top left of the GUI.
        fileMenu = menubar.addMenu('File')

        # Adds an action to 'File' tab.
        saveFile_simple = QAction('Save - Simple Statistics', self)
        fileMenu.addAction(saveFile_simple)
        # self.saveFile_simple.clicked.connect(lambda: self.get_automata_stats())

        saveFile_complex = QAction('Save - Complex Statistics', self)
        fileMenu.addAction(saveFile_complex)
        # self.saveFile_complex.clicked.connect(lambda: self.get_automata_stats())

        # Adds a 'Help' tab, which is placed to the right of 'File' in the top left of the GUI.
        help_act = QAction('Help', self)
        menubar.addAction(help_act)        

        # Adds a 'Display' tab,  which is placed to the right of 'Help' in the top left of the GUI.
        display_menu = menubar.addMenu('Display')

        # Adds actions to 'Display' tab.
        base_matrix_act = QAction('Base Matrix', self)
        evo_matrix_act = QAction('Transition (Evolution) Matrix', self)
        display_menu.addAction(base_matrix_act)
        display_menu.addAction(evo_matrix_act)

        # Adds a 'Calculation' tab, which is placed to the right of 'Display' in the top left of the GUI.
        calculation_menu = menubar.addMenu('Calculation')

        # Adds actions to 'Calculation' tab.
        rref_act = QAction('Row Reduced Echelon Form', self)
        nullspace_act = QAction('Nullspace of Matrix', self)
        rank_act = QAction('Rank of Matrix', self)
        cycle_act = QAction('Detect First Cycle', self)
        stats_act = QAction('Generate Cycle Statistics', self)
        calculation_menu.addAction(rref_act)
        calculation_menu.addAction(nullspace_act)
        calculation_menu.addAction(rank_act)
        calculation_menu.addAction(cycle_act)
        calculation_menu.addAction(stats_act)


        """
        Commands to set the function that calls when an item is selected.
        The flag 'base' refers to the base automata matrix, while 'evo' refers to the Transition (Evolution) matrix.
        """
        saveFile_simple.triggered.connect(lambda: self.saveToFile('Simple'))
        saveFile_complex.triggered.connect(lambda: self.saveToFile('Complex'))

        help_act.triggered.connect(lambda: self.display_help())

        base_matrix_act.triggered.connect(lambda: self.display_matrix('base'))
        evo_matrix_act.triggered.connect(lambda: self.display_matrix('evo'))
        rref_act.triggered.connect(lambda: self.rref_of_matrix())
        nullspace_act.triggered.connect(lambda: self.nullspace_of_matrix())
        rank_act.triggered.connect(lambda: self.display_pop_up('rank'))
        cycle_act.triggered.connect(lambda: self.display_pop_up('cycle'))
        stats_act.triggered.connect(lambda: self.get_automata_stats('Simple'))

        """ End Menu Bar Creation """

        """ Begin Default Input Form Creation """

        """
        Input form for number of cells. The input value will determine the number of columns in the automata.
        """
        self.number_of_cells_label = QLabel(self)
        self.number_of_cells_label.setText('Number Of Cells:')
        self.number_of_cells = QLineEdit(self)
        self.number_of_cells.move(20, 20)
        self.number_of_cells.resize(280,40)

        """
        Input form for alphabet size. The input value will determine the alphabet of our automata (ie. 0, 1, 2, 3), as well as the modulo division of our system.
        """
        self.alphabet_size_label = QLabel(self)
        self.alphabet_size_label.setText('Alphabet Size:')
        self.alphabet_size = QLineEdit(self)
        self.alphabet_size.move(20, 20)
        self.alphabet_size.resize(280,40)

        """
        Input form for the initial state of the automata. The input value will be the state at which the system begins.
        The initial state must agree with the number of cells (columns) in the automata and the size of the alphabet in the automata.
        The user may input 'random' for a random initial state, while retaining the other variables.
        """
        self.initial_state_label = QLabel(self)
        self.initial_state_label.setText('Initial State:')
        self.initial_state = QLineEdit(self)
        self.initial_state.move(20, 20)
        self.initial_state.resize(280,40)

        """
        Input form for the update rule of the automata. The update rule will be used to transition the automata between steps.
        The update rule is of the form: n1 n2 n3 ... nm, where n is an element of R (all real integers) and m is an element of Z (all positive integers).
        This string of integers represents the positional elements relative to the current cell, which will be computed in transition to the next state of the automata.

        UNDER CONSTRUCTION: Will be replaced later with a radius of elements to choose from, in order to add complexity and functionality to the system.
        """
        self.update_rule_label = QLabel(self)
        self.update_rule_label.setText('Update Rule:')
        self.update_rule = QLineEdit(self)
        self.update_rule.move(20, 20)
        self.update_rule.resize(280,40)

        """
        Input form the number of steps of the automata. The input value will determine how large the generating automata will be.
        """
        self.number_of_steps_label = QLabel(self)
        self.number_of_steps_label.setText('Number Of Steps:')
        self.number_of_steps = QLineEdit(self)
        self.number_of_steps.move(20, 20)
        self.number_of_steps.resize(280,40)

        """
        Update Automata Button - will regenerate automata with current entries in the input forms.
        """
        self.update_automata_button = QPushButton('Submit', self)
        self.update_automata_button.setToolTip('Submit an update to the automaton')
        self.update_automata_button.clicked.connect(self.on_click_update_automata)

        """
        Randomly Populate Automata Button - will randomly fill each form with a valid entry, yielding a random automata.
        """
        self.random_automata_button = QPushButton('Random', self)
        self.random_automata_button.setToolTip('Randomly Populate the Automata')
        self.random_automata_button.clicked.connect(self.on_click_randomly_populate_automata)

        """
        Pushes form to the GUI.
        """
        self.input_form_default = QtWidgets.QFormLayout()
        self.input_form_default.addRow(self.number_of_cells_label, self.number_of_cells)
        self.input_form_default.addRow(self.alphabet_size_label, self.alphabet_size)
        self.input_form_default.addRow(self.initial_state_label, self.initial_state)
        self.input_form_default.addRow(self.update_rule_label, self.update_rule)
        self.input_form_default.addRow(self.number_of_steps_label, self.number_of_steps)
        self.input_form_default.addRow(self.random_automata_button, self.update_automata_button)

        """ End Default Input Form Creation """

        """ Begin Nullspace Input Form Creation """

        self.nullspace_label = QLabel(self)
        self.nullspace_label.setText('Power of matrix to generate:')
        self.nullspace_powers = QLineEdit(self)
        self.nullspace_powers.setText("0")
        self.nullspace_powers.move(20, 20)
        self.nullspace_powers.resize(280,40)

        self.nullspace_tk_button1 = QPushButton('Find nullspace of T^k', self)
        self.nullspace_tk_button1.clicked.connect(lambda: self.matrix_nullspace('None'))
        
        self.nullspace_tk_button2 = QPushButton('Find nullspace of T^k - I', self)
        self.nullspace_tk_button2.clicked.connect(lambda: self.matrix_nullspace('identity'))

        self.nullspace_output = QTextEdit(self)

        self.nullspace_form = QtWidgets.QFormLayout()
        self.nullspace_form.addRow(self.nullspace_label, self.nullspace_powers)
        self.nullspace_form.addRow(self.nullspace_tk_button1, self.nullspace_tk_button2)
        self.nullspace_form.addRow(self.nullspace_output)

        """ End Nullspace Input Form Creation """

        """ Begin Powers Of Matrix Input Form Creation """

        # Matrix powers tab
        # Powers of matrix label
        self.powers_of_matrix_label = QLabel(self)
        self.powers_of_matrix_label.setText('Power of matrix to generate:')
        self.powers_of_matrix = QLineEdit(self)
        self.powers_of_matrix.setText("0")
        self.powers_of_matrix.move(20, 20)
        self.powers_of_matrix.resize(280,40)

        # Submit button for T^k
        self.update_powers_button1 = QPushButton('Find T^k', self)
        self.update_powers_button1.setToolTip('Submit an update to the automaton')
        self.update_powers_button1.clicked.connect(lambda: self.matrix_powers('None'))

        # Submit button for T^k - I
        self.update_powers_button2 = QPushButton('Find T^k - I', self)
        self.update_powers_button2.setToolTip('Submit an update to the automaton')
        self.update_powers_button2.clicked.connect(lambda: self.matrix_powers('identity'))

        self.matrix_output = QTextEdit(self)

        self.matrix_powers_form = QtWidgets.QFormLayout()
        self.matrix_powers_form.addRow(self.powers_of_matrix_label, self.powers_of_matrix)
        self.matrix_powers_form.addRow(self.update_powers_button1, self.update_powers_button2)
        self.matrix_powers_form.addRow(self.matrix_output)

        """ End Powers Of Matrix Input Form Creation """

        """ Begin Cycle Statistics Input Form Creation """

        # self.cycle_stats_label = QLabel(self)
        # self.cycle_stats_label.setText('Power of matrix to generate:')
        # self.cycle_stats = QLineEdit(self)
        # self.cycle_stats.move(20, 20)
        # self.cycle_stats.resize(280,40)

        # Submit button for simple statistics output
        self.cycle_stats_button1 = QPushButton('Simple Statistics', self)
        self.cycle_stats_button1.setToolTip('Submit an update to the automaton')
        self.cycle_stats_button1.clicked.connect(lambda: self.get_automata_stats('Simple'))

        # Submit button for complex statistics output
        self.cycle_stats_button2 = QPushButton('Complex Statistics', self)
        self.cycle_stats_button2.setToolTip('Submit an update to the automaton')
        self.cycle_stats_button2.clicked.connect(lambda: self.get_automata_stats('Complex'))

        self.cycle_output = QTextEdit(self)

        self.cycle_stats_form = QtWidgets.QFormLayout()
        # self.cycle_stats_form.addRow(self.cycle_stats_label, self.cycle_stats)
        self.cycle_stats_form.addRow(self.cycle_stats_button1, self.cycle_stats_button2)
        self.cycle_stats_form.addRow(self.cycle_output)

        """ End Cycle Statistics Input Form Creation """

        """ Begin Output Form Creation """

        self.output_label = QLabel(self)
        self.output_label.setText('Please note that you must select a file to write to before you generate data, otherwise it will only output here.')

        self.output_text = QTextEdit(self)

        self.output_form_layout = QtWidgets.QFormLayout()
        self.output_form_layout.addRow(self.output_label)
        self.output_form_layout.addRow(self.output_text)

        """ End Output Form Creation """

        """ Begin Layout Creation """
        self.layout = QtWidgets.QVBoxLayout()

        # Create tabs to hold various inputs and outputs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tabs.resize(300,200)

        # Add tabs to widget
        self.tabs.addTab(self.tab1, "Default Input")
        self.tabs.addTab(self.tab2, "Nullspace")
        self.tabs.addTab(self.tab3, "Matrix Powers")
        self.tabs.addTab(self.tab4, "Cycle Statistics")
        self.tabs.addTab(self.tab5, "Output")

        """
        Tab 1: Default Input
        """
        self.tab1.setLayout(self.input_form_default)

        """
        Tab 2: Nullspace
        """

        self.tab2.setLayout(self.nullspace_form)

        """
        Tab 3: Matrix Powers
        """
        self.tab3.setLayout(self.matrix_powers_form)

        """
        Tab 4: Cycle Statistics
        """
        self.tab4.setLayout(self.cycle_stats_form)

        """
        Tab 5: Output
        """
        self.tab5.setLayout(self.output_form_layout)

        """ Finish placing items in page layout """
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.tabs)

        # Create a placeholder widget to hold our toolbar and canvas.
        plot = QtWidgets.QWidget()
        plot.setLayout(self.layout)
        self.setCentralWidget(plot)
        # Diplay the GUI
        self.show()

        """ End Initialization """

    @pyqtSlot()
    def on_click_update_automata(self):

        try:
            number_of_cells = int(self.number_of_cells.text())
        except ValueError:
            number_of_cells = 0

        try:
            alphabet_size = int(self.alphabet_size.text())
        except ValueError:
            alphabet_size = 0

        try:
            number_of_steps = int(self.number_of_steps.text())
        except ValueError:
            number_of_steps = 0

        initial_state = self.initial_state.text()
        update_rule = self.update_rule.text()

        self.CA.set_number_of_cells(number_of_cells)
        self.CA.set_alphabet_size(alphabet_size)
        self.CA.set_initial_state(initial_state)
        self.CA.set_update_rule(update_rule)
        self.CA.set_number_of_steps(number_of_steps)

        print('Number of Cells: {}'.format(self.number_of_cells.text()))
        print('Alphabet Size: {}'.format(self.alphabet_size.text()))
        print('Initial State: {}'.format(self.initial_state.text()))
        print('Update Rule: {}'.format(self.update_rule.text()))
        print('Number of Steps: {}'.format(self.number_of_steps.text()))

        self.CA.generate_evolution_matrix()
        self.CA.generate_cellular_automata()

        self.activeMatrix = self.CA.get_cellular_automata()
        #self.CA.generate_nullspace_matrix('cell')
        # self.CA.generate_nullspace_matrix('evo')
        # self.CA.detect_first_cycle()

        # Redraw the plat
        self.display_matrix('base')

    def on_click_randomly_populate_automata(self):
        # Init variables for contraint checking
        num_cells = random.randint(2, 10)
        alphabet = random.choice([i for i in cached_primes if 3 <= i <= 7]) # make prime number only (min:3 max:13)
        num_steps = random.randint(10, 50)
        # Init starting state
        state = ''
        for i in range(num_cells):
            state += str(random.randint(0, alphabet-1))
        # Init update rule - randomly decide when to stop
        rule = ''
        for i in range(5):
            rule += str(random.randint(-1*num_cells+1, num_cells-1))
            rule += " "
            if (random.randint(0, 1) == 0):
                break


        # Clear text fields
        self.number_of_cells.clear()
        self.alphabet_size.clear()
        self.initial_state.clear()
        self.update_rule.clear()
        self.number_of_steps.clear()

        # Insert text fields
        self.number_of_cells.insert(str(num_cells))
        self.alphabet_size.insert(str(alphabet))
        self.initial_state.insert(state)
        self.update_rule.insert(rule)
        self.number_of_steps.insert(str(num_steps))


    """
    Main function for displaying the matrix.
    """
    def display_matrix(self, flag='None'):
        self.canvas.axes.cla()  # Clear the canvas.
        if flag == 'base':
            """
            If function is called with 'base' flag, the base matrix becomes the last matrix displayed.
            The base matrix is then displayed in the canvas.
            The base matrix is then displayed in the output.
            """
            self.activeMatrixLabel = 'base'
            self.lastMatrix = self.CA.get_cellular_automata()
            self.activeMatrix = self.lastMatrix
            self.canvas.axes.matshow(self.activeMatrix)

            msg = '\nBase Matrix:\n' + str(self.lastMatrix)
            # self.output_text.setText(msg)

            # Append to file if file is selected
            if self.outputFile:
                print('outputting to file')
                self.outputFile.write(msg)


        elif flag == 'evo':
            """
            If function is called with 'evo' flag, the Transition (Evolution) matrix of the base matrix becomes the last matrix displayed.
            The Transition (Evolution) matrix is then displayed in the canvas.
            The Transition (Evolution) matrix is then displayed in the output.
            """
            self.activeMatrixLabel = 'evo'
            self.lastMatrix = self.CA.get_evolution_matrix()
            self.activeMatrix = self.lastMatrix
            self.canvas.axes.matshow(self.activeMatrix)

            msg = '\nTransition (Evolution) Matrix:\n' + str(self.lastMatrix)
            self.output_text.setText(msg)

            # Append to file if file is selected
            if self.outputFile:
                print('outputting to file')
                self.outputFile.write(msg)

        elif flag == 'last':
            """
            If function is called with 'last' flag, the last used matrix is displayed in the canvas.
            The last used matrix is then displayed in the output.
            """
            self.canvas.axes.matshow(self.lastMatrix)

            if self.activeMatrixLabel == 'evo':
                msg = '\nTransition (Evolution) Matrix:\n' + str(self.lastMatrix)
            else:
                msg = '\nBase Matrix:\n' + str(self.lastMatrix)
            self.output_text.setText(msg)

            # Append to file if file is selected
            if self.outputFile:
                print('outputting to file')
                self.outputFile.write(msg)

        else:
            if self.activeMatrixLabel == 'base':
                self.lastMatrix = self.CA.get_cellular_automata()
                self.activeMatrix = self.lastMatrix
                self.canvas.axes.matshow(self.activeMatrix)

                # Print matrix to output
                msg = '\nBase Matrix:\n' + str(self.lastMatrix)
                self.output_text.setText(msg)

                # Append to file if file is selected
                if self.outputFile:
                    print('outputting to file')
                    self.outputFile.write(msg)

            elif self.activeMatrixLabel == 'evo':
                self.lastMatrix = self.CA.get_evolution_matrix()
                self.activeMatrix = self.lastMatrix
                self.canvas.axes.matshow(self.activeMatrix)

                # Print matrix to output
                msg = '\nTransition (Evolution) Matrix:\n' + str(self.lastMatrix)
                self.output_text.setText(msg)

                # Append to file if file is selected
                if self.outputFile:
                    print('outputting to file')
                    self.outputFile.write(msg)

        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def rref_of_matrix(self, flag='None'):
        self.canvas.axes.cla()  # Clear the canvas.
        if self.activeMatrixLabel == 'base':
            self.lastMatrix = self.CA.row_reduced_echelon_form(self.CA.get_cellular_automata())
            self.canvas.axes.matshow(self.lastMatrix)
            msg = "Row Reduced Echelon Form of Cellular Automata: "

            # Append to file if file is selected
            if self.outputFile:
                print('outputting to file')
                self.outputFile.write(msg)

        elif self.activeMatrixLabel == 'evo':
            self.canvas.axes.matshow(self.CA.row_reduced_echelon_form(self.CA.get_evolution_matrix()))
            msg = "Row Reduced Echelon Form of Transition (Evolution) Matrix: "

            # Append to file if file is selected
            if self.outputFile:
                print('outputting to file')
                self.outputFile.write(msg)

        # Trigger the canvas to update and redraw.
        self.canvas.draw()


    """
    When the Update Powers button is clicked, calculate and display the corresponding matrix power.
    """
    def matrix_powers(self, flag = 'None'):
        
        if self.CA.get_is_automata_generated() == 0:
            return

        if flag == 'identity':
            self.lastMatrix = self.CA.generate_T_pow_minus_I(int(self.powers_of_matrix.text()))
        else:
            self.lastMatrix = self.CA.generate_T_pow(int(self.powers_of_matrix.text()))

        msg = str(self.lastMatrix)

        self.matrix_output.setText(msg)
        
        self.display_matrix('last')

    def matrix_nullspace(self, flag = 'None'):
        
        if self.CA.get_is_automata_generated() == 0:
            return

        if flag == 'identity':
            self.lastMatrix = self.CA.generate_null_T_minus_I(int(self.nullspace_powers.text()))
        else:
            self.lastMatrix = self.CA.generate_null_T(int(self.nullspace_powers.text()))

        msg = str(self.lastMatrix)

        self.nullspace_output.setText(msg)

        self.display_matrix('last')

    def nullspace_of_matrix(self, flag='None'):

        if self.lastMatrix.shape[0] != self.lastMatrix.shape[1]:
            return

        self.canvas.axes.cla()  # Clear the canvas.

        # Take the nullspace of the matrix currently in the canvas
        nullspace = self.CA.get_nullspace_matrix(self.lastMatrix)

        # lastMatrix = Basis type: list
        nullspace = np.asarray(nullspace)
        
        if nullspace.size == 0:
            nullspace = np.zeros([int(self.number_of_cells.text()), int(self.number_of_cells.text())], dtype=int)

        self.lastMatrix = nullspace

        msg = 'Nullspace = ' + str(self.lastMatrix)

        self.output_text.setText(msg)

        # Append to file if file is selected
        if self.outputFile:
            print('outputting to file')
            self.outputFile.write(msg)
        else:
            print('no file selected')

        self.canvas.axes.matshow(self.lastMatrix)
        self.canvas.draw()


    def display_pop_up(self, flag_type="None", flag_call="None"):
        dlg = QMessageBox(self)

        if flag_type == "cycle":
            msg = self.CA.detect_first_cycle(self.lastMatrix)
            dlg.setWindowTitle("Cycle Detected")

        elif flag_type == "rank":
            if self.activeMatrixLabel == 'base':
                rank = self.CA.rank(self.CA.get_cellular_automata())
                msg = "RANK = {}".format(rank)
            elif self.activeMatrixLabel == 'evo':
                rank = self.CA.rank(self.CA.get_evolution_matrix())
                msg = "RANK = {}".format(rank)

            dlg.setWindowTitle("Rank")

        dlg.setText(msg)
        dlg.exec_()


    """
    Help Window:
    Displays information about the software.
    """
    def display_help(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Help')
        msg = 'This is helpful.\n'
        msg += 'The functions in the Calculation tab apply to the currently displayed matrix in the canvas.\n'
        msg += 'The \'Matrix Powers\' tab generates the powers of the transition matrix.\n'
        dlg.setText(msg)
        dlg.exec_()


    def save(self):
        if self.curFile:
            self.saveToFile(self.curFile)
        else:
            self.saveAs()

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            self.saveFile(fileName)


    """
    When this function is called, open a file explorer window for user to select a file to append to.
    """
    def saveToFile(self, flag):
        if self.CA.get_is_automata_generated() == 0:
            return

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Output to a file", "example.txt","All Files (*);;Python Files (*.py)", options=options)

        print (fileName)
        if fileName:
            self.outputFile = open(fileName, 'w')

        self.get_automata_stats(flag)
        self.outputFile.close()

        # Temp output for GUI to save to save file later
        self.outputFile = open('temp_data', 'w')


    def toggleGroup(self, ctrl):
        state = ctrl.isChecked()
        if state:
            ctrl.setFixedHeight(ctrl.sizeHint().height())
        else:
            ctrl.setFixedHeight(30)


    """
    Generates statistics about the system, called from AutomataStats.py
    Two outputs:
    Simple:
        cycle length, cycle copies, number of states, nullspace
    Complex:
        powers, rref, nullspaces, etc
    """
    def get_automata_stats(self, print_type):
        
        if(print_type == "Simple" or print_type == "Complex"):
            automata_stats, reversibility, s, n, cycle_type = stats.generate_automata_stats(self.CA.get_evolution_matrix(), int(self.number_of_cells.text()), int(self.alphabet_size.text()))

            msg = ''

            msg += 'Number of Cells: {}\n'.format(self.number_of_cells.text())
            msg += 'Alphabet Size: {}\n'.format(self.alphabet_size.text())
            msg += 'Update Rule: {}\n'.format(self.update_rule.text())

            msg += str(reversibility) + '\n'

            if(cycle_type == "0"):
                msg += '\nTransition Matrix Powers: T^{} = Zero Matrix\n'.format(n+1)
            elif(cycle_type == "I"):
                msg += '\nTransition Matrix Powers: T^{} = Identity Matrix\n'.format(n+1)
            elif(cycle_type == "Cycle"):
                msg += '\nTransition Matrix Powers: Cycle T^{} = T^{}\n'.format(s+1, n+1)

            I = np.identity(int(self.number_of_cells.text()), dtype=int)

            for i in range(len(automata_stats)):
                msg += "\n"
                msg += ("Cycle Length: {}\n".format(automata_stats[i]["power"]))
                msg += ("Cycles Copies: {}\n".format(int(automata_stats[i]["cycles_count"])))
                msg += ("Number of States on Length {} Cycles: {}\n".format(automata_stats[i]["power"], automata_stats[i]["states"]))
                msg += ("Dimension of nullspace: {}\n".format(automata_stats[i]["cycles_size"]))



                if np.array_equal(automata_stats[i]["nullspace"], I):
                    msg += ("Nullspace: {}\n".format("Entire Cellular Automata"))
                else:
                    msg += "Nullspace: \n" + str(automata_stats[i]["nullspace"]) + '\n\n'

            if (print_type == "Complex"):
                
                result_matrix_pow = self.CA.get_evolution_matrix()
                for i in range(1, n+2):
                    msg += ("\n(T)^{}: \n".format(i))
                    if(i > 0):
                        result_matrix_pow = (np.matmul(self.CA.get_evolution_matrix(), result_matrix_pow)) % int(self.alphabet_size.text())
                    result_matrix = (result_matrix_pow) % int(self.alphabet_size.text())
                    msg += str(result_matrix)

                msg += ("\n")

                result_matrix_pow = self.CA.get_evolution_matrix()
                for i in range(1, n+2):
                    msg += ("\n(T)^{} - I: \n".format(i))
                    if(i > 0):
                        result_matrix_pow = (np.matmul(self.CA.get_evolution_matrix(), result_matrix_pow)) % int(self.alphabet_size.text())
                    result_matrix = (result_matrix_pow - I) % int(self.alphabet_size.text())
                    msg += str(result_matrix)

            self.output_text.setText(msg)
            self.cycle_output.setText(msg)

            # Append to file if file is selected
            if self.outputFile:
                print('outputting to file')
                self.outputFile.write(msg)
            else:
                print('no file selected')

        return()

    """
    Upon app close, close output file.
    """
    def closeEvent(self, event):
        if self.outputFile:
            self.outputFile.close()

    """ End Main Window """

"""
"""

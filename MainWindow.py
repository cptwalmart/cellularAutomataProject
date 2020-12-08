"""
This project was created for COSC 425 for use by Salisbury University.
Programmers: Joseph Craft, Sean Dunn, Malik Green, Kevin Koch
COSC 425 Cellular Automata Project

******************************************

This is the GUI file of the project, primarily using the PyQt5 library, as well as matplotlib for graphing.
The main computational file CellularAutomata.py is imported and called throughout to incorporate functions into the GUI.
"""

import MplCanvas as mpl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QGroupBox, QToolBar, QMenu, QDialog, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from sympy import *     # For nullspace
import CellularAutomata
import random

### Cached Prime Numbers ###
# initialising primes
minPrime = 0
maxPrime = 1000
cached_primes = [i for i in range(minPrime,maxPrime) if isprime(i)]
### Cached Prime Numbers ###

"""
This class represents the main window of the GUI. As such, most of the GUI is accessed here, as well as the main computational file CellularAutomata.py.
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

        # Display cellular automata as graphs in the GUI
        self.canvas = mpl.MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.axes.matshow(self.CA.get_cellular_automata())

        #### Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second ###
        self.toolbar = NavigationToolbar(self.canvas, self)
        ### --- ###

        # Flag to determine which matrix certain functions work with.
        # Default is base matrix.
        self.activeMatrix = 'base'

        """ Menu Bar Creation """
        menubar = self.menuBar()

        # Adds a 'File' tab, which is placed in the top left of the GUI.
        fileMenu = menubar.addMenu('File')

        # Adds an action to 'File' tab.
        saveFile = QAction('Output to file', self)
        fileMenu.addAction(saveFile)

        # Adds a 'Display' tab,  which is placed to the right of 'File' in the top left of the GUI.
        display_menu = menubar.addMenu('Display')

        # Adds actions to 'Display' tab.
        base_matrix_act = QAction('Base Matrix', self)
        evo_matrix_act = QAction('Evolution Matrix', self)
        active_matrix_act = QAction('Make this my base matrix for future calculations', self)
        display_menu.addAction(base_matrix_act)
        display_menu.addAction(evo_matrix_act)
        display_menu.addAction(active_matrix_act)

        # Adds a 'Calculation' tab, which is placed to the right of 'Display' in the top left of the GUI.
        calculation_menu = menubar.addMenu('Calculation')

        # Adds actions to 'Calculation' tab.
        rref_act = QAction('Row Reduced Echelon Form', self)
        nullspace_act = QAction('Nullspace of Matrix', self)
        rank_act = QAction('Rank of Matrix', self)
        cycle_act = QAction('Detect Cycle', self)
        calculation_menu.addAction(rref_act)
        calculation_menu.addAction(nullspace_act)
        calculation_menu.addAction(rank_act)
        calculation_menu.addAction(cycle_act)

        # Nullspace sub-tab
        #nullspace_menu = QMenu('Basis of Nullspace', self)
        #nullspace_display_act = QAction('Display Nullspace', self)
        #nullspace_rank_display_act = QAction('Display Rank of Nullspace', self)
        #nullspace_menu.addAction(nullspace_display_act)
        #nullspace_menu.addAction(nullspace_rank_display_act)

        """
        Commands to set the function that calls when an item is selected.
        The flag 'base' refers to the base automata matrix, while 'evo' refers to the evolution matrix.
        """
        base_matrix_act.triggered.connect(lambda: self.display_matrix('base'))
        evo_matrix_act.triggered.connect(lambda: self.display_matrix('evo'))
        rref_act.triggered.connect(lambda: self.display_rref_of_matrix())
        nullspace_act.triggered.connect(lambda: self.display_nullspace_of_matrix())
        rank_act.triggered.connect(lambda: self.display_pop_up('rank'))
        cycle_act.triggered.connect(lambda: self.display_pop_up('cycle'))

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
        self.update_automata_button.setToolTip('Submit an Update to the Automata')
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
        input_form_default = QtWidgets.QFormLayout()
        input_form_default.addRow(self.number_of_cells_label, self.number_of_cells)
        input_form_default.addRow(self.alphabet_size_label, self.alphabet_size)
        input_form_default.addRow(self.initial_state_label, self.initial_state)
        input_form_default.addRow(self.update_rule_label, self.update_rule)
        input_form_default.addRow(self.number_of_steps_label, self.number_of_steps)
        input_form_default.addRow(self.random_automata_button, self.update_automata_button)

        # Functionality to enable or disable powers input.
        self.default_input_groupbox = QGroupBox("Cellular Automata Input")
        self.default_input_groupbox.setCheckable(True)
        self.default_input_groupbox.setChecked(True)
        self.default_input_groupbox.setLayout(input_form_default)

        self.default_input_groupbox.toggled.connect(lambda:self.toggleGroup(self.default_input_groupbox))
        ### --- ###

        """ End Default Input Form Creation """

        """ Begin Powers Of Matrix Input Form Creation """

        # Matrix powers tab
        # Powers of matrix label
        self.powers_of_matrix_label = QLabel(self)
        self.powers_of_matrix_label.setText('Power of matrix to generate:')
        self.powers_of_matrix = QLineEdit(self)
        self.powers_of_matrix.move(20, 20)
        self.powers_of_matrix.resize(280,40)

        input_form_matrix_powers = QtWidgets.QFormLayout()
        input_form_matrix_powers.addRow(self.powers_of_matrix_label, self.powers_of_matrix)

        # Functionality to enable or disable powers input.
        self.powers_input_groupbox = QGroupBox("Matrix Powers Input")
        self.powers_input_groupbox.setCheckable(True)
        self.powers_input_groupbox.setChecked(False)
        self.powers_input_groupbox.setLayout(input_form_matrix_powers)

        self.powers_input_groupbox.toggled.connect(lambda: self.toggleGroup(self.powers_input_groupbox))

        """ End Powers Of Matrix Input Form Creation """

        """ Begin Output Form Creation """

        self.output_label = QLabel(self)
        self.output_label.setText('Please note that you must select a file to write to before you generate data, otherwise it will only output here.')

        self.output_form = QtWidgets.QFormLayout()
        self.output_form.addRow(self.output_label)

        self.output_form_groupbox = QGroupBox("Output")
        self.output_form_groupbox.setLayout(self.output_form)

        """ End Output Form Creation """

        """ Begin Layout Creation """
        self.layout = QtWidgets.QVBoxLayout()

        # Create tabs to hold various inputs and outputs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(300,200)

        self.tabs.addTab(self.tab1, "Default Input")
        self.tabs.addTab(self.tab2, "Update Rule")
        self.tabs.addTab(self.tab3, "Matrix Powers")
        self.tabs.addTab(self.tab4, "Output")

        """
        Tab 1: Default Input
        """
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.default_input_groupbox)
        self.tab1.setLayout(self.tab1.layout)

        """
        Tab 2: Update Rule (Currently not implemented)
        """
        self.tab2.layout = QVBoxLayout(self)
        # self.tab2.layout.addWidget()
        self.tab2.setLayout(self.tab2.layout)

        """
        Tab 3: Matrix Powers
        """
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.layout.addWidget(self.powers_input_groupbox)
        self.tab3.setLayout(self.tab3.layout)

        """
        Tab 4: Output
        """
        self.tab4.layout = QVBoxLayout(self)
        self.tab4.layout.addWidget(self.output_form_groupbox)
        self.tab4.setLayout(self.tab4.layout)

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
        #self.CA.generate_nullspace_matrix('cell')
        self.CA.generate_nullspace_matrix('evo')
        self.CA.detect_cycle()

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

    def display_matrix(self, flag='None'):
        self.canvas.axes.cla()  # Clear the canvas.
        if flag == 'base':
            self.activeMatrix = 'base'
            self.canvas.axes.matshow(self.CA.get_cellular_automata())
        elif flag == 'evo':
            self.activeMatrix = 'evo'
            self.canvas.axes.matshow(self.CA.get_evolution_matrix())
        else:
            if self.activeMatrix == 'base':
                self.canvas.axes.matshow(self.CA.get_cellular_automata())
            elif self.activeMatrix == 'evo':
                self.canvas.axes.matshow(self.CA.get_evolution_matrix())

        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def display_rref_of_matrix(self, flag='None'):
        self.canvas.axes.cla()  # Clear the canvas.
        if self.activeMatrix == 'base':
            self.canvas.axes.matshow(self.CA.row_reduced_echelon_form(self.CA.get_cellular_automata()))
            print("Row Reduced Echelon Form of Cellular Automata: ")
        elif self.activeMatrix == 'evo':
            #self.canvas.axes.matshow(self.CA.rref(self.CA.get_evolution_matrix()))
            self.canvas.axes.matshow(self.CA.row_reduced_echelon_form(self.CA.get_evolution_matrix()))
            print("Row Reduced Echelon Form of Evolution Matrix: ")
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def display_nullspace_of_matrix(self, flag='None'):
        self.canvas.axes.cla()  # Clear the canvas.
        if self.activeMatrix == 'base':
            #self.canvas.axes.matshow(self.CA.get_nullspace_matrix())
            print("Under Construction")
        elif self.activeMatrix == 'evo':
            #self.canvas.axes.matshow(self.CA.get_nullspace_matrix())
            print("Under Construction")
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def display_rank_of_matrix(self, flag='None'):
        self.canvas.axes.cla()  # Clear the canvas.
        if self.activeMatrix == 'base':
            rank = self.CA.rank(self.CA.get_cellular_automata())
            print("Rank of Cellular Automata: ")
            pprint(rank)
        elif self.activeMatrix == 'evo':
            rank = self.CA.rank(self.CA.get_evolution_matrix())
            print("Rank of Evolution Matrix: ")
            pprint(rank)
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def display_pop_up(self, flag_type="None", flag_call="None"):
        dlg = QMessageBox(self)

        if flag_type == "cycle":
            msg = self.CA.detect_cycle()
            dlg.setWindowTitle("Cycle Detected")

        elif flag_type == "rank":
            if self.activeMatrix == 'base':
                rank = self.CA.rank(self.CA.get_cellular_automata())
                msg = "RANK = {}".format(rank)
            elif self.activeMatrix == 'evo':
                rank = self.CA.rank(self.CA.get_evolution_matrix())
                msg = "RANK = {}".format(rank)

            dlg.setWindowTitle("Rank")

        dlg.setText(msg)
        dlg.exec_()

    def toggleGroup(self, ctrl):
        state = ctrl.isChecked()
        if state:
            ctrl.setFixedHeight(ctrl.sizeHint().height())
        else:
            ctrl.setFixedHeight(30)

    """ End Main Window """

"""
"""

import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QGroupBox, QToolBar, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import matplotlib.pyplot as plt
import re       # Needed for parsing


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        ### Cellular Automata ###
        self.CA = CellularAutomata()
        ### ###

        # Set Window Elements
        self.title = 'PyQt5 - Cellular Automata'
        self.setWindowTitle(self.title)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.axes.matshow(self.CA.get_cellular_automata())

        #### Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second ###
        self.toolbar = NavigationToolbar(self.canvas, self)
        ### --- ###

        ### Menu Bar ###
        menubar = self.menuBar()

        # File tab
        fileMenu = menubar.addMenu('File')
        newAct = QAction('New', self)
        impMenu = QMenu('Import', self)
        importAct = QAction('Import Automata', self) 
        impMenu.addAction(importAct)

        # Add sub-tab to File tab
        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)

        # Calculation tab
        calculation_menu = menubar.addMenu('Calculation')

        # Cellular Automata sub-tab
        automata_menu = QMenu('Automata Matrix', self)
        automata_display_act = QAction('Display Matrix', self) 
        automata_menu.addAction(automata_display_act)

        # Evolution sub-tab
        evolution_menu = QMenu('Evolution Matrix', self)
        evolition_display_act = QAction('Display Matrix', self) 
        evolution_menu.addAction(evolition_display_act)

        # Nullspace sub-tab
        nullspace_menu = QMenu('Basis of Nullspace', self)
        nullspace_display_act = QAction('Display Nullspace', self)
        nullspace_rank_display_act = QAction('Display Rank of Nullspace', self) 
        nullspace_menu.addAction(nullspace_display_act)
        nullspace_menu.addAction(nullspace_rank_display_act)

        # Add sub-tab to File tab
        calculation_menu.addMenu(automata_menu)
        calculation_menu.addMenu(evolution_menu)
        calculation_menu.addMenu(nullspace_menu)

        automata_display_act.triggered.connect(self.display_automata_matrix)
        evolition_display_act.triggered.connect(self.display_evolition_matrix)
        nullspace_display_act.triggered.connect(self.display_nullspace_of_matrix)
        nullspace_rank_display_act.triggered.connect(self.display_rank_of_matrix)

 
        ### --- ###

        ### Create Input Form Elements ###
        self.number_of_cells_lable = QLabel(self)
        self.number_of_cells_lable.setText('# of cells:')
        self.number_of_cells = QLineEdit(self)
        self.number_of_cells.move(20, 20)
        self.number_of_cells.resize(280,40)

        self.alphabet_size_lable = QLabel(self)
        self.alphabet_size_lable.setText('alphablet size:')
        self.alphabet_size = QLineEdit(self)
        self.alphabet_size.move(20, 20)
        self.alphabet_size.resize(280,40)

        self.initial_state_lable = QLabel(self)
        self.initial_state_lable.setText('initial state:')
        self.initial_state = QLineEdit(self)
        self.initial_state.move(20, 20)
        self.initial_state.resize(280,40)

        self.update_rule_lable = QLabel(self)
        self.update_rule_lable.setText('update rule:')
        self.update_rule = QLineEdit(self)
        self.update_rule.move(20, 20)
        self.update_rule.resize(280,40)

        # Update Automata Button
        update_automata_button = QPushButton('Submit', self)
        update_automata_button.setToolTip('Submit an Update to the Automata')
        update_automata_button.clicked.connect(self.on_click_update_automata)

        input_form = QtWidgets.QFormLayout()
        input_form.addRow(self.number_of_cells_lable, self.number_of_cells)
        input_form.addRow(self.alphabet_size_lable, self.alphabet_size)
        input_form.addRow(self.initial_state_lable, self.initial_state)
        input_form.addRow(self.update_rule_lable, self.update_rule)
        input_form.addRow(update_automata_button)

        self.automata_input_groupbox = QGroupBox("Cellular Automata Input")
        self.automata_input_groupbox.setCheckable(True)
        self.automata_input_groupbox.setChecked(True)
        self.automata_input_groupbox.setLayout(input_form)

        self.automata_input_groupbox.toggled.connect(lambda: self.toggleGroup(self.automata_input_groupbox))
        ### --- ###

        ### Place items in page layout ###
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.automata_input_groupbox)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        ### --- ###

        # Create a placeholder widget to hold our toolbar and canvas.
        plot = QtWidgets.QWidget()
        plot.setLayout(layout)
        self.setCentralWidget(plot)
        # Diplay the GUI
        self.show()

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

        initial_state = self.initial_state.text()
        update_rule = self.update_rule.text()

        self.CA.set_number_of_cells(number_of_cells)
        self.CA.set_alphabet_size(alphabet_size)
        self.CA.set_initial_state(initial_state)
        self.CA.set_update_rule(update_rule)

        print('Cell number: {}'.format(self.number_of_cells.text()))
        print('Alphabet Size: {}'.format(self.alphabet_size.text()))
        print('Initial state: {}'.format(self.initial_state.text()))
        print('Update Rule: {}'.format(self.update_rule.text()))

        self.CA.generate_evolution_matrix()
        self.CA.generate_cellular_automata()

        # Redraw the plat
        self.display_automata_matrix()

    def display_automata_matrix(self):
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.matshow(self.CA.get_cellular_automata())
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def display_evolition_matrix(self):
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.matshow(self.CA.get_evolution_matrix())
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def display_nullspace_of_matrix(self):
        print("hello")

    def display_rank_of_matrix(self):
        print("hello")

    def toggleGroup(self, ctrl):
        state = ctrl.isChecked()
        if state:
            ctrl.setFixedHeight(ctrl.sizeHint().height())
        else:
            ctrl.setFixedHeight(30)

        



# The class is setup as a Method so all function must pass 'self' for the 1st variable
class CellularAutomata:

    def __init__(self):
        self.cellular_automata = np.zeros([2,2], dtype=int)
        self.evolution_matrix = np.zeros([2,2], dtype=int)
        self.num_elements = 0
        self.num_alphabet = 0
        self.ca_next = 0
        self.num_steps = 10
        self.debug=False

        self.initial_state = []
        self.update_rule = 0

    def set_number_of_cells(self, number_of_cells):
        self.num_elements = number_of_cells
    def set_alphabet_size(self, alphabet_size):
        self.num_alphabet = alphabet_size
    def set_initial_state(self, initial_state):
        """
        This process takes a string of integers as input and verifies that it is a valid starting state.
        """

        start_state = []  # Starting state will be appended one element at a time.
        valid = True

        num_digits = 0
        #test_state = input('Enter starting state: ')
        if initial_state == 'random':
            for x in range(0, num_elements):
                start_state.append(random.randint(0, num_alphabet-1))
            print("Your random state is ", start_state)

        else:
            #for i in test_state:
                #if (i.isdigit() and int(i) < num_alphabet):
                    #if debug == True:
                        #print(i, " is a digit and is less than ", num_alphabet)
                    #num_digits = num_digits + 1
                    #valid = True
                #else:
                    #print('Incorrect character: ', i)
                    #valid = False
                    #break

            #while (not valid or num_digits != num_elements):
                #if (num_digits != num_elements):
                    #print('You entered: ', num_digits,
                        #' element(s)\nThis automaton needs: ', num_elements, ' element(s)\n')
                #num_digits = 0
                #test_state = input('Enter starting state: ')
                #for i in test_state:
                    #if (i.isdigit() and int(i) < num_alphabet):
                        #if debug == True:
                            #print(i, " is a digit and is less than ", num_alphabet)
                        #num_digits = num_digits + 1
                        #valid = True
                    #else:
                        #print('Incorrect character: ', i)
                        #valid = False
                        #break

            for i in initial_state:
                start_state.append(int(i))

        self.initial_state = start_state
        
        
    def set_update_rule(self, string):
        """
        This function takes a string of numbers as input, which represent cells in a row. If a number exist outside the boundaries of the row, the string must be reentered.
            num_elements        -- Number of cells in row.
            valid               -- Flag that checks whether a string of numbers is valid.
        """

        valid = False

        while not valid:
            update_rule = []

            # Each number represents a cell in relation to the current one. +1 is one to the right. -1 is one to the left.
            #string = input("Enter cells to be added for the rule (i.e. -2 0 3): ")
            update_rule = [int(d) for d in re.findall(r'-?\d+', string)]

            for i in update_rule:
                if abs(i) > self.num_elements:
                    print(i, ' is not a valid element for this automaton.\n')
                    valid = False
                    break
                else:
                    valid = True

            #if debug == True:
            print('The update rule is ', update_rule)
        self.update_rule = update_rule

    def get_cellular_automata(self):
        return self.cellular_automata

    def get_evolution_matrix(self):
        return self.evolution_matrix

    def get_nullspace(self):
        return self.cellular_automata

    def get_rank(self):
        return self.cellular_automata

    def generate_cellular_automata(self):
        """Takes a state and evolves it over n steps.
        cellular_automata   -- Main matrix
        ca_next             -- Current state in iteration of process
        step                -- Number of states in the matrix
        The final output will look like:
                0001
                1001
                0101
                1111
        """

        step = 1
        ca_next = self.initial_state
        cellular_automata = []
        cellular_automata.append((ca_next))

        while (step <= self.num_steps):

            if (self.debug == True):
                print('Step # ', step, ':\nEvolution Matrix:\n', np.matrix(
                    self.evolution_matrix), '\nMultiplied by State:', cellular_automata[step-1])
            ca_next = np.matmul(self.evolution_matrix, cellular_automata[step-1]) % self.num_alphabet
            if (self.debug == True):
                print('Equals: ', ca_next, ' Equals: ', np.transpose(ca_next))
            cellular_automata.append(ca_next)

            step += 1  # Step increment

        print("\nFinal Matrix: ")
        for i in range(0, self.num_steps):
            print(cellular_automata[i], end=" ")
            print()

        self.cellular_automata = cellular_automata
    
    def generate_evolution_matrix(self):
        """
        This function translates an identity_matrix into an evolution_matrix, given an update rule.
            num_elements        -- Number of cells in a row.
            update_rule         -- Rule that defines the evolution_matrix.
            debug               -- Flag that offers insight to program if set.
            identity_matrix     -- n by n matrix filled with 0s aside from 1s in the top-left diagonal.
            evolution_matrix    -- n by n matrix that when multiplied to a state, gives the next state.
            row                 -- Temporary variable for each row in the matrix.
        """

        identity_matrix = np.identity(self.num_elements, int)
        if self.debug == True:
            print('Identity Matrix:\n', identity_matrix)

        evolution_matrix = []
        row = []
        new_element = 0

        for i in range(0, self.num_elements):		# Every row in matrix
            row = []
            for j in range(0, self.num_elements):    # Every element in row
                new_element = 0

                for k in self.update_rule:           # Every element in update rule
                    if j + k >= self.num_elements:
                        l = j + k - self.num_elements
                    else:
                        l = j + k

                    if self.debug == True:
                        print('l = ', l)
                        print(
                            new_element, '+', identity_matrix[i][l], '=', new_element + identity_matrix[i][l])

                    new_element = new_element + identity_matrix[i][l]

                    if self.debug == True:           # Debug -- print the location and value of element
                        print('Element [', i, ', ', j,
                            '] will now be ', new_element)

                row.append(new_element % self.num_alphabet)

                if self.debug == True:
                    print(new_element, ' % ', self.num_alphabet,
                        ' = ', new_element % self.num_alphabet)
                    print('Row ', i, ':\n', row)
            evolution_matrix.append(row)
            if self.debug == True:
                print('\nEvolution Matrix (Row ', i, '):\n',
                    np.matrix(evolution_matrix))

        if self.debug == True:
            print('Identity Matrix:\n', identity_matrix)

        self.evolution_matrix = np.transpose(evolution_matrix)
        


app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')
w = MainWindow()
app.exec_()
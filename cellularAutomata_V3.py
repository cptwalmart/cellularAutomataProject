"""
This project was created for COSC 425 for use by Salisbury University.
Programmers: Joseph Craft, Sean Dunn, Malik Green, Kevin Koch
COSC 425 Cellular Automata Project
"""


import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QGroupBox, QToolBar, QMenu, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
from numpy.linalg import *
import matplotlib.pyplot as plt
from sympy import *     # For nullspace
import re       # Needed for parsing
import random

"""
Classes MplCanvas and MainWindow are needed to run the GUI
The CellularAutomata class is used for the logic of the program
"""


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
        automata_rref_act = QAction('Row Reduced Echelon Form', self)
        automata_nullspace_act = QAction('Nullspace of Matrix', self)
        automata_rank_act = QAction('Rank of Matrix', self)
        automata_cycle_act = QAction('Detect Cycle', self)
        automata_menu.addAction(automata_display_act)
        automata_menu.addAction(automata_rref_act)
        automata_menu.addAction(automata_nullspace_act)
        automata_menu.addAction(automata_rank_act)
        automata_menu.addAction(automata_cycle_act)

        # Evolution sub-tab
        evolution_menu = QMenu('Evolution Matrix', self)
        evolution_display_act = QAction('Display Matrix', self)
        evolution_rref_act = QAction('Row Reduced Echelon Form', self)
        evolution_nullspace_act = QAction('Nullspace of Matrix', self)
        evolution_rank_act = QAction('Rank of Matrix', self)
        evolution_menu.addAction(evolution_display_act)
        evolution_menu.addAction(evolution_rref_act)
        evolution_menu.addAction(evolution_nullspace_act)
        evolution_menu.addAction(evolution_rank_act)

        # Nullspace sub-tab
        #nullspace_menu = QMenu('Basis of Nullspace', self)
        #nullspace_display_act = QAction('Display Nullspace', self)
        #nullspace_rank_display_act = QAction('Display Rank of Nullspace', self) 
        #nullspace_menu.addAction(nullspace_display_act)
        #nullspace_menu.addAction(nullspace_rank_display_act)

        # Add sub-tab to File tab
        calculation_menu.addMenu(automata_menu)
        calculation_menu.addMenu(evolution_menu)
        #calculation_menu.addMenu(nullspace_menu)

        automata_display_act.triggered.connect(lambda: self.display_matrix('cell'))
        automata_rref_act.triggered.connect(lambda: self.display_rref_of_matrix('cell'))
        automata_nullspace_act.triggered.connect(lambda: self.display_nullspace_of_matrix('cell'))
        automata_rank_act.triggered.connect(lambda: self.display_pop_up('rank', 'cell'))
        automata_cycle_act.triggered.connect(lambda: self.display_pop_up('cycle', 'cell'))

        evolution_display_act.triggered.connect(lambda: self.display_matrix('evo'))
        evolution_rref_act.triggered.connect(lambda: self.display_rref_of_matrix('evo'))
        evolution_nullspace_act.triggered.connect(lambda: self.display_nullspace_of_matrix('evo'))
        evolution_rank_act.triggered.connect(lambda: self.display_pop_up('rank', 'evo'))

 
        ### --- ###

        ### Create Input Form Elements ###
        self.number_of_cells_label = QLabel(self)
        self.number_of_cells_label.setText('# of cells:')
        self.number_of_cells = QLineEdit(self)
        self.number_of_cells.move(20, 20)
        self.number_of_cells.resize(280,40)

        self.alphabet_size_label = QLabel(self)
        self.alphabet_size_label.setText('alphabet size:')
        self.alphabet_size = QLineEdit(self)
        self.alphabet_size.move(20, 20)
        self.alphabet_size.resize(280,40)

        self.initial_state_label = QLabel(self)
        self.initial_state_label.setText('initial state:')
        self.initial_state = QLineEdit(self)
        self.initial_state.move(20, 20)
        self.initial_state.resize(280,40)

        self.update_rule_label = QLabel(self)
        self.update_rule_label.setText('update rule:')
        self.update_rule = QLineEdit(self)
        self.update_rule.move(20, 20)
        self.update_rule.resize(280,40)
        
        # Steps
        self.number_of_steps_label = QLabel(self)
        self.number_of_steps_label.setText('# of steps:')
        self.number_of_steps = QLineEdit(self)
        self.number_of_steps.move(20, 20)
        self.number_of_steps.resize(280,40)

        # Update Automata Button
        self.update_automata_button = QPushButton('Submit', self)
        self.update_automata_button.setToolTip('Submit an Update to the Automata')
        self.update_automata_button.clicked.connect(self.on_click_update_automata)

        # Randomly Populate Automata Button
        self.random_automata_button = QPushButton('Random', self)
        self.random_automata_button.setToolTip('Randomly Populate the Automata')
        self.random_automata_button.clicked.connect(self.on_click_randomly_populate_automata)

        input_form = QtWidgets.QFormLayout()
        input_form.addRow(self.number_of_cells_label, self.number_of_cells)
        input_form.addRow(self.alphabet_size_label, self.alphabet_size)
        input_form.addRow(self.initial_state_label, self.initial_state)
        input_form.addRow(self.update_rule_label, self.update_rule)
        input_form.addRow(self.number_of_steps_label, self.number_of_steps)
        input_form.addRow(self.random_automata_button, self.update_automata_button)

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
        self.display_matrix('cell')

    def on_click_randomly_populate_automata(self):
        # Init variables for contraint checking
        num_cells = random.randint(1, 10)
        alphabet = random.randint(1, 5)
        num_steps = random.randint(1, 50)
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

    #def display_automata_matrix(self):
        #self.canvas.axes.cla()  # Clear the canvas.
        #self.canvas.axes.matshow(self.CA.get_cellular_automata())
        ## Trigger the canvas to update and redraw.
        #self.canvas.draw()

    #def display_evolution_matrix(self):
        #self.canvas.axes.cla()  # Clear the canvas.
        #self.canvas.axes.matshow(self.CA.get_evolution_matrix())
        ## Trigger the canvas to update and redraw.
        #self.canvas.draw()
        
    def display_matrix(self, flag='None'):
        self.canvas.axes.cla()  # Clear the canvas.
        if flag == 'cell':
            self.canvas.axes.matshow(self.CA.get_cellular_automata())
        elif flag == 'evo':
            self.canvas.axes.matshow(self.CA.get_evolution_matrix())
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def display_rref_of_matrix(self, flag='None'):
        self.canvas.axes.cla()  # Clear the canvas.
        if flag == 'cell':
            self.canvas.axes.matshow(self.CA.rref(self.CA.get_cellular_automata()))
            print("Row Reduced Echelon Form of Cellular Automata: ")
        elif flag == 'evo':
            self.canvas.axes.matshow(self.CA.rref(self.CA.get_evolution_matrix()))
            print("Row Reduced Echelon Form of Evolution Matrix: ")
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def display_nullspace_of_matrix(self, flag='None'):
        self.canvas.axes.cla()  # Clear the canvas.
        if flag == 'cell':
            #self.canvas.axes.matshow(self.CA.get_nullspace_matrix())
            print("Under Construction")
        elif flag == 'evo':
            #self.canvas.axes.matshow(self.CA.get_nullspace_matrix())
            print("Under Construction")
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def display_rank_of_matrix(self, flag='None'):
        self.canvas.axes.cla()  # Clear the canvas.
        if flag == 'cell':
            rank = self.CA.rank(self.CA.get_cellular_automata())
            print("Rank of Cellular Automata: ")
            pprint(rank)
        elif flag == 'evo':
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
            if flag_call == "cell":
                rank = self.CA.rank(self.CA.get_cellular_automata())
                msg = "RANK = {}".format(rank)
            elif flag_call == "evo":
                rank = self.CA.rank(self.CA.get_evolution_matrix())
                msg = "RANK = {}".format(rank)

            dlg.setWindowTitle("Rank")

        dlg.setText(msg)
        dlg.exec_()

        



# The class is setup as a Method so all function must pass 'self' for the 1st variable
class CellularAutomata:

    def __init__(self):
        self.cellular_automata = np.zeros([2,2], dtype=int)
        self.evolution_matrix = np.zeros([2,2], dtype=int)
        self.nullspace_matrix = np.zeros([2,2], dtype=int)
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
        if initial_state == 'random':
            for x in range(0, self.num_elements):
                start_state.append(random.randint(0, self.num_alphabet-1))
            print("Your random state is ", start_state)

        else:
            #for i in start_state:
                #if (i.isdigit() and int(i) < self.num_alphabet):
                    #if self.debug == True:
                        #print(i, " is a digit and is less than ", self.num_alphabet)
                    #num_digits = num_digits + 1
                    #valid = True
                #else:
                    #print('Incorrect character: ', i)
                    #valid = False
                    #break

            #if (not valid or num_digits != self.num_elements):
                #if (num_digits != self.num_elements):
                    #print('You entered: ', num_digits,
                        #' element(s)\nThis automaton needs: ', self.num_elements, ' element(s)\n')
                #return


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
            update_rule = [int(d) for d in re.findall(r'-?\d+', string)]

            for i in update_rule:
                if abs(i) > self.num_elements:
                    print(i, ' is not a valid element for this automaton.\n')
                    valid = False
                    return
                else:
                    valid = True

            if self.debug == True:
                print('The update rule is ', update_rule)
        self.update_rule = update_rule

    def set_number_of_steps(self, number_of_steps):
        self.num_steps = number_of_steps

    def get_cellular_automata(self):
        return self.cellular_automata

    def get_evolution_matrix(self):
        return self.evolution_matrix

    def get_nullspace_matrix(self):
        return self.nullspace_matrix

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
        ca_next = np.asarray(self.initial_state)
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

    def generate_nullspace_matrix(self, flag="None"):
        if flag == 'cell':
            nullspace = Matrix(self.cellular_automata)
            nullspace.nullspace()
        if flag == 'evo':
            nullspace = Matrix(self.evolution_matrix)
            nullspace.nullspace()
            self.nullspace_matrix = np.matrix(nullspace)
        
    def detect_cycle(self):
            for i in range(len(self.cellular_automata)):
                for j in range(len(self.cellular_automata)):
                    if i != j:
                        if (self.cellular_automata[i] == self.cellular_automata[j]).all():
                            msg = ("CYCLE DETECTED FROM STEP {} TO STEP {}".format(i, j))
                            #print(msg)
                            return(msg)
                            break
                    elif i == len(self.cellular_automata):
                        msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
                        return(msg)
                else:
                    continue
                break
            msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
            return(msg)


    
    def rref(self, B, tol=1e-8, debug=False):
        B = np.asarray(B, dtype=np.int32)        
        
        A = B.copy()
        rows, cols = A.shape
        r = 0
        pivots_pos = []
        row_exchanges = np.arange(rows)
        for c in range(cols):
            if debug:
                print("Now at row", r, "and col", c, "with matrix:")
                print(A)

            # Find the pivot row:
            pivot = np.argmax(np.abs(A[r:rows, c])) + r
            m = np.abs(A[pivot, c])
            if debug:
                print("Found pivot", m, "in row", pivot)
            if m <= tol:
                # Skip column c, making sure the approximately zero terms are
                # actually zero.
                A[r:rows, c] = np.zeros(rows-r)
                if debug:
                    print("All elements at and below (", r,
                        ",", c, ") are zero.. moving on..")
            else:
                # keep track of bound variables
                pivots_pos.append((r, c))

                if pivot != r:
                    # Swap current row and pivot row
                    A[[pivot, r], c:cols] = A[[r, pivot], c:cols]
                    row_exchanges[[pivot, r]] = row_exchanges[[r, pivot]]

                    if debug:
                        print("Swap row", r, "with row", pivot, "Now:")
                        print(A)

                # Normalize pivot row
                A[r, c:cols] = A[r, c:cols] / A[r, c]

                # Eliminate the current column
                v = A[r, c:cols]
                # Above (before row r):
                if r > 0:
                    ridx_above = np.arange(r)
                    A[ridx_above, c:cols] = A[ridx_above, c:cols] - \
                        np.outer(v, A[ridx_above, c]).T
                    if debug:
                        print("Elimination above performed:")
                        print(A)
                # Below (after row r):
                if r < rows-1:
                    ridx_below = np.arange(r+1, rows)
                    A[ridx_below, c:cols] = A[ridx_below, c:cols] - \
                        np.outer(v, A[ridx_below, c]).T
                    if debug:
                        print("Elimination below performed:")
                        print(A)
                r += 1
            # Check if done
            if r == rows:
                break
        return (A)#, pivots_pos, row_exchanges)
    
    
    def rank(self, A, atol=1e-13, rtol=0):
        """Estimate the rank (i.e. the dimension of the nullspace) of a matrix.
        The algorithm used by this function is based on the singular value
        decomposition of `A`.
        Parameters
        ----------
        A : ndarray
            A should be at most 2-D.  A 1-D array with length n will be treated
            as a 2-D with shape (1, n)
        atol : float
            The absolute tolerance for a zero singular value.  Singular values
            smaller than `atol` are considered to be zero.
        rtol : float
            The relative tolerance.  Singular values less than rtol*smax are
            considered to be zero, where smax is the largest singular value.
        If both `atol` and `rtol` are positive, the combined tolerance is the
        maximum of the two; that is::
            tol = max(atol, rtol * smax)
        Singular values smaller than `tol` are considered to be zero.
        Return value
        ------------
        r : int
            The estimated rank of the matrix.
        See also
        --------
        numpy.linalg.matrix_rank
            matrix_rank is basically the same as this function, but it does not
            provide the option of the absolute tolerance.
        """

        A = np.atleast_2d(A)
        s = svd(A, compute_uv=False)
        tol = max(atol, rtol * s[0])
        rank = int((s >= tol).sum())
        return rank


app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')
w = MainWindow()
app.exec_()
import MplCanvas as mpl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QGroupBox, QToolBar, QMenu, QDialog
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

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        ### Cellular Automata ###
        self.CA = CellularAutomata.CellularAutomata()
        ### ###

        # Set Window Elements
        self.title = 'PyQt5 - Cellular Automata'
        self.setWindowTitle(self.title)

        self.canvas = mpl.MplCanvas(self, width=5, height=4, dpi=100)
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
            #self.canvas.axes.matshow(self.CA.rref(self.CA.get_evolution_matrix()))
            self.canvas.axes.matshow(self.CA.row_echelon_form(self.CA.get_evolution_matrix()))
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

    def toggleGroup(self, ctrl):
        state = ctrl.isChecked()
        if state:
            ctrl.setFixedHeight(ctrl.sizeHint().height())
        else:
            ctrl.setFixedHeight(30)
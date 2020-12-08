import numpy as np
from numpy.linalg import *
import matplotlib.pyplot as plt
from sympy import *     # For nullspace
import re       # Needed for parsing
import random
import Nayuki as field
import gistfile1 as gist
from sympy import Matrix, Rational, mod_inverse, pprint

# The class is setup as a method so all functions must pass 'self' for the 1st variable.
class CellularAutomata:

    # Initialization of variables.
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

	# Set function for number of columns in the matrix.
    def set_number_of_cells(self, number_of_cells):
        self.num_elements = number_of_cells


	# Set function for size of alphabet.
    def set_alphabet_size(self, alphabet_size):
        self.num_alphabet = alphabet_size


	# Set function for number of discrete time steps (rows in matrix).
    def set_number_of_steps(self, number_of_steps):
        self.num_steps = number_of_steps


	# Set function for initial state.
    def set_initial_state(self, initial_state):
        """
        This function takes a string of integers as input and converts it to a compatible starting state for the matrix.
        """
        start_state = []
        num_digits = 0
        if initial_state == 'random':
            for x in range(0, self.num_elements):
                start_state.append(random.randint(0, self.num_alphabet-1))
            print("Your random state is ", start_state)

        else:
            for i in initial_state:
                start_state.append(int(i))

        self.initial_state = start_state


    # Set function for update rule.
    def set_update_rule(self, string):
        """
        This function takes a string of numbers as input, which represent cells in a row. If a number exists outside the boundaries of the row, the string must be reentered.
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

            #if self.debug == True:
                #print('The update rule is ', update_rule)
        self.update_rule = update_rule


	# Return function for main matrix
    def get_cellular_automata(self):
        return self.cellular_automata


	# Return function for evolution matrix
    def get_evolution_matrix(self):
        return self.evolution_matrix


	# Return function for the nullspace of the matrix
    def get_nullspace_matrix(self):
        return self.nullspace_matrix


    # Primary function - determines the automaton itself.
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

            #if (self.debug == True):
                #print('Step # ', step, ':\nEvolution Matrix:\n', np.matrix(
                    #self.evolution_matrix), '\nMultiplied by State:', cellular_automata[step-1])
            ca_next = np.matmul(self.evolution_matrix, cellular_automata[step-1]) % self.num_alphabet
            #if (self.debug == True):
                #print('Equals: ', ca_next, ' Equals: ', np.transpose(ca_next))
            cellular_automata.append(ca_next)

            step += 1  # Step increment

        print("\nFinal Matrix: ")
        for i in range(0, self.num_steps):
            print(cellular_automata[i], end=" ")
            print()

        self.cellular_automata = np.asarray(cellular_automata)


    # Function to determine the evolution matrix based on the update rule.
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
        #if self.debug == True:
            #print('Identity Matrix:\n', identity_matrix)

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

                    #if self.debug == True:
                        #print('l = ', l)
                        #print(
                            #new_element, '+', identity_matrix[i][l], '=', new_element + identity_matrix[i][l])

                    new_element = new_element + identity_matrix[i][l]

                    #if self.debug == True:           # Debug -- print the location and value of element
                        #print('Element [', i, ', ', j,
                            #'] will now be ', new_element)

                row.append(new_element % self.num_alphabet)

                #if self.debug == True:
                    #print(new_element, ' % ', self.num_alphabet,
                        #' = ', new_element % self.num_alphabet)
                    #print('Row ', i, ':\n', row)
            evolution_matrix.append(row)
            #if self.debug == True:
                #print('\nEvolution Matrix (Row ', i, '):\n',
                    #np.matrix(evolution_matrix))

        #if self.debug == True:
            #print('Identity Matrix:\n', identity_matrix)

        self.evolution_matrix = np.transpose(evolution_matrix)


	# Generate nullspace of the matrix
    def generate_nullspace_matrix(self, flag="None"):
        if flag == 'cell':
            nullspace = Matrix(self.cellular_automata)
            nullspace.nullspace()
        if flag == 'evo':
            nullspace = Matrix(self.evolution_matrix)
            nullspace.nullspace()
            self.nullspace_matrix = np.matrix(nullspace)


    # Row reduced echelon form using multiplicative inverse
    def row_reduced_echelon_form(self, A):

        print(type(A))

        ### Using Sympy ###
        #A_rref = Matrix(A, dtype=int)
        #A_rref = A_rref.rref(iszerofunc=lambda x: x % self.num_alphabet==0)
        #A_rref[0].applyfunc(lambda x: gist.mod(x,self.num_alphabet))
        #print(A_rref)

        ### Using Nayuki ####
        F = field.PrimeField(self.num_alphabet)
        B = field.Matrix(A.shape[0], A.shape[1], F)
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                B.set(i, j, ( int(A[i][j])) )

        print(B)
        B.reduced_row_echelon_form()
        print(B)

        # Convert back to numpy matrix
        B_rref = np.zeros([A.shape[0],A.shape[1]], dtype=int)
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                B_rref[i][j] = B.get(i, j)

        ### using Gist ####
        # my re-visit to correct multiplcative inverse errors
        # Issue: number of cells cannot be bigger than mod p
        #C = np.asarray(A, dtype=np.int32)
        #C = gist.modrref(B, self.num_alphabet)

        return B_rref


    # # Row reduced echelon form using floating point arithmetic
    # def rref(self, B, tol=1e-8, debug=False):
    #     B = np.asarray(B, dtype=np.int32)
    #
    #     A = B.copy()
    #     rows, cols = A.shape
    #     r = 0
    #     pivots_pos = []
    #     row_exchanges = np.arange(rows)
    #     for c in range(cols):
    #         if debug:
    #             print("Now at row", r, "and col", c, "with matrix:")
    #             print(A)
    #
    #         # Find the pivot row:
    #         pivot = np.argmax(np.abs(A[r:rows, c])) + r
    #         m = np.abs(A[pivot, c])
    #         if debug:
    #             print("Found pivot", m, "in row", pivot)
    #         if m <= tol:
    #             # Skip column c, making sure the approximately zero terms are
    #             # actually zero.
    #             A[r:rows, c] = np.zeros(rows-r)
    #             if debug:
    #                 print("All elements at and below (", r,
    #                     ",", c, ") are zero.. moving on..")
    #         else:
    #             # keep track of bound variables
    #             pivots_pos.append((r, c))
    #
    #             if pivot != r:
    #                 # Swap current row and pivot row
    #                 A[[pivot, r], c:cols] = A[[r, pivot], c:cols]
    #                 row_exchanges[[pivot, r]] = row_exchanges[[r, pivot]]
    #
    #                 if debug:
    #                     print("Swap row", r, "with row", pivot, "Now:")
    #                     print(A)
    #
    #             # Normalize pivot row
    #             A[r, c:cols] = A[r, c:cols] / A[r, c]
    #
    #             # Eliminate the current column
    #             v = A[r, c:cols]
    #             # Above (before row r):
    #             if r > 0:
    #                 ridx_above = np.arange(r)
    #                 A[ridx_above, c:cols] = A[ridx_above, c:cols] - \
    #                     np.outer(v, A[ridx_above, c]).T
    #                 if debug:
    #                     print("Elimination above performed:")
    #                     print(A)
    #             # Below (after row r):
    #             if r < rows-1:
    #                 ridx_below = np.arange(r+1, rows)
    #                 A[ridx_below, c:cols] = A[ridx_below, c:cols] - \
    #                     np.outer(v, A[ridx_below, c]).T
    #                 if debug:
    #                     print("Elimination below performed:")
    #                     print(A)
    #             r += 1
    #         # Check if done
    #         if r == rows:
    #             break
    #     return (A)#, pivots_pos, row_exchanges)


    # Function to determine the rank of a matrix.
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


    # This function will be improved later, in terms of versatility and time complexity.
	# Detect the first cycle in the range of the matrix
    def detect_cycle(self):
        """
        This function loops through the range of the matrix and compares each row i to each row j in the rest of the matrix.
        It stops either when it finds two of the same row (a cycle), or it reaches the end of the matrix.
        Because there are a finite number of states, given enough discrete time steps, there will be a cycle.

        This function will be improved later, in terms of versatility and time complexity.
        """

        for i in range(len(self.cellular_automata)):
            for j in range(i+1, len(self.cellular_automata)):
                if (self.cellular_automata[i] == self.cellular_automata[j]).all():
                    msg = ("CYCLE DETECTED FROM STEP {} TO STEP {}".format(i, j))
                    return(msg)
                elif i == len(self.cellular_automata):
                    msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
                    return(msg)
        msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
        return(msg)

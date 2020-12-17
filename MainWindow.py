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

        self.is_automata_generated = 0

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


    # Set function for main matrix
    def set_cellular_automata(self, new_matrix):
        self.cellular_automata = np.asarray(new_matrix)


	# Return function for main matrix
    def get_cellular_automata(self):
        return self.cellular_automata


	# Return function for evolution matrix
    def get_evolution_matrix(self):
        return self.evolution_matrix

    # Return function to check if the automata has been generated
    def get_is_automata_generated(self):
        return self.is_automata_generated


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
            ca_next = np.matmul(self.evolution_matrix, cellular_automata[step-1]) % self.num_alphabet

            cellular_automata.append(ca_next)

            step += 1  # Step increment

        # print("\nFinal Matrix: ")
        # for i in range(0, self.num_steps):
        #     print(cellular_automata[i], end=" ")
        #     print()

        self.cellular_automata = np.asarray(cellular_automata)
        self.is_automata_generated = 1


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

                    new_element = new_element + identity_matrix[i][l]

                row.append(new_element % self.num_alphabet)

            evolution_matrix.append(row)

        self.evolution_matrix = np.transpose(evolution_matrix)


    # Row reduced echelon form using multiplicative inverse
    def row_reduced_echelon_form(self, A):

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

        B.reduced_row_echelon_form()

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


    # Returns the nullspace of the given matrix using Nayuki
    def get_nullspace_matrix(self, data):

        F = field.PrimeField(self.num_alphabet)
        B = field.Matrix(self.num_elements, self.num_elements, F)

        # Nayuki Matrix "B"
        for i in range(self.num_elements):
            for j in range(self.num_elements):
                B.set(i, j, int(data[i][j]))

        B.reduced_row_echelon_form()
        Basis = B.get_nullspace()

        # for i in range(self.num_elements):
        #     for j in range(self.num_elements):
        #         print('test')
                # data[i][j] = Basis[i][j]

        # data = np.asarray(Basis)
        # print("In get_null_mat: ",type(Basis))
        return Basis


    """
    Compute nullspace for (T)^{power}
    """
    def generate_null_T(self, power):

        if power == 0:
            I = np.identity(self.num_elements, dtype=int)
            return I, []

        original_evolution_matrix = self.get_evolution_matrix()
        power = int(power)

        try:
            return_matrix_pow = original_evolution_matrix
            for i in range(power):
                if(i > 0):
                    return_matrix_pow = (np.matmul(original_evolution_matrix, return_matrix_pow)) % self.num_alphabet
                return_matrix = (return_matrix_pow) % self.num_alphabet

        except:
            print('The matrix must be square!')
            return_matrix = original_evolution_matrix


        if return_matrix.all() == 0:
            return return_matrix, "Entire cellular automata"

        ### Using Nayuki ####
        F = field.PrimeField(self.num_alphabet)
        B = field.Matrix(return_matrix.shape[0], return_matrix.shape[1], F)
        for i in range(return_matrix.shape[0]):
            for j in range(return_matrix.shape[1]):
                B.set(i, j, ( int(return_matrix[i][j])) )

        B.reduced_row_echelon_form()
        Basis = B.get_nullspace()

        numpy_Basis = np.array(Basis)


        for i in range(return_matrix.shape[0]):
            for j in range(return_matrix.shape[1]):
                return_matrix[i][j] = B.get(i, j)

        return return_matrix, numpy_Basis



    """
    Compute nullspace for (T)^{power} - I
    """
    def generate_null_T_minus_I(self, power):
        I = np.identity(self.num_elements, dtype=int)

        if power == 0:
            return I, []

        original_evolution_matrix = self.get_evolution_matrix()
                # Identity Matrix
        power = int(power)

        try:
            return_matrix_pow = original_evolution_matrix
            for i in range(power):
                if(i > 0):
                    return_matrix_pow = (np.matmul(original_evolution_matrix, return_matrix_pow)) % self.num_alphabet
                return_matrix = (return_matrix_pow - I) % self.num_alphabet

        except:
            print('The matrix must be square!')
            return_matrix = original_evolution_matrix

        if return_matrix.all() == 0:
            return return_matrix, "Entire cellular automata"

        ### Using Nayuki ####
        F = field.PrimeField(self.num_alphabet)
        B = field.Matrix(return_matrix.shape[0], return_matrix.shape[1], F)
        for i in range(return_matrix.shape[0]):
            for j in range(return_matrix.shape[1]):
                B.set(i, j, ( int(return_matrix[i][j])) )

        B.reduced_row_echelon_form()
        B.get_nullspace()

        Basis = B.get_nullspace()
        #print(type(Basis))

        numpy_Basis = np.array(Basis)


        print("Value of B from generate_null_T_minus_I: ", B)
        print("Nullspace of T^{} : {}".format(power, Basis))

        for i in range(return_matrix.shape[0]):
            for j in range(return_matrix.shape[1]):
                return_matrix[i][j] = B.get(i, j)



        #return return_matrix
        return return_matrix, numpy_Basis

    """
    Compute power  for (T)^{power}
    """
    def generate_T_pow(self, power):

        # Any matrix to 0 power is identity.
        I = np.eye(self.get_evolution_matrix().shape[0], dtype=int)
        if power == 0:
            return I

        original_evolution_matrix = self.get_evolution_matrix()
        power = int(power)

        try:
            return_matrix_pow = original_evolution_matrix
            for i in range(power):
                if(i > 0):
                    return_matrix_pow = (np.matmul(original_evolution_matrix, return_matrix_pow)) % self.num_alphabet
                return_matrix = (return_matrix_pow) % self.num_alphabet

        except:
            print('The matrix must be square!')
            return_matrix = original_evolution_matrix

        return return_matrix

    """
    Compute power  for (T)^{power} - I
    """
    def generate_T_pow_minus_I(self, power):

        if power == 0:
            return self.get_evolution_matrix()

        original_evolution_matrix = self.get_evolution_matrix()
        I = np.identity(self.num_elements, dtype=int) # Identity Matrix

        power = int(power)

        try:
            return_matrix_pow = original_evolution_matrix
            for i in range(power):
                if(i > 0):
                    return_matrix_pow = (np.matmul(self.get_evolution_matrix(), return_matrix_pow)) % self.num_alphabet
                return_matrix = (return_matrix_pow - I) % self.num_alphabet

        except:
            print('The matrix must be square!')
            return_matrix = original_evolution_matrix

        # rows = cols = size
        # transition = data
        # result_matrix = np.zeros([rows, cols], dtype=int)

        # result_matrix_pow = transition
        # for i in range(power):
        #     if(i > 0):
        #         result_matrix_pow = (np.matmul(transition, result_matrix_pow)) % alphabet
        #     result_matrix = (result_matrix_pow - I) % alphabet

        return return_matrix


    # This function will be improved later, in terms of versatility and time complexity.
	# Detect the first cycle in the range of the matrix
    def detect_first_cycle(self, data):
        """
        This function loops through the range of the matrix and compares each row i to each row j in the rest of the matrix.
        It stops either when it finds two of the same row (a cycle), or it reaches the end of the matrix.
        Because there are a finite number of states, given enough discrete time steps, there will be a cycle.
        This function will be improved later, in terms of versatility and time complexity.
        """

        # for i in range(len(self.cellular_automata)):
        #     for j in range(i+1, len(self.cellular_automata)):
        #         if (self.cellular_automata[i] == self.cellular_automata[j]).all():
        #             msg = ("CYCLE DETECTED FROM STEP {} TO STEP {}".format(i, j))
        #             return(msg)
        #         elif i == len(self.cellular_automata):
        #             msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
        #             return(msg)
        # msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")


        for i in range(len(data)):
            for j in range(i+1, len(data)):
                if (data[i] == data[j]).all():
                    msg = ("CYCLE DETECTED FROM STEP {} TO STEP {}".format(i, j))
                    return(msg)
                elif i == len(data):
                    msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
                    return(msg)
        msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")

        return(msg)

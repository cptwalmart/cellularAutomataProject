import numpy as np
from numpy.linalg import svd  # calc nullspace
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import re		# Regular expression - used for parsing
import random

# from http://wiki.scipy.org/Cookbook/RankNullspace
# code for rref(), rank(), nullspace() are referenced from scipy libs

# Code is referenced from python sympy library. Reference for further explanation
def rref(B, tol=1e-8, debug=False):
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
    return (A, pivots_pos, row_exchanges)


def cellular_automata(num_elements, num_alphabet, ca_next, num_steps, evolution_matrix, debug=False):
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

    cellular_automata = []
    cellular_automata.append(np.transpose(ca_next))

    while (step <= num_steps):

        if (debug == True):
            print('Step # ', step, ':\nEvolution Matrix:\n', np.matrix(
                evolution_matrix), '\nMultiplied by State:', cellular_automata[step-1])
        ca_next = np.transpose(
            np.matmul(evolution_matrix, cellular_automata[step-1]) % num_alphabet)
        if (debug == True):
            print('Equals: ', ca_next, ' Equals: ', np.transpose(ca_next))
        cellular_automata.append(ca_next)

        step += 1  # Step increment

    print("\nFinal Matrix: ")
    for i in range(0, num_steps):
        print(cellular_automata[i], end=" ")
        print()

    cellular_automata_rref = np.asarray(cellular_automata, dtype=np.int32)
    print("\nFinal Matrix in Row Reduced Echelon Form:\n",
          rref(cellular_automata_rref))
    # rref(M_rref, tol=1e-8, debug=True)

    # Output the matplot graph
    wait = input("Press enter to continue...")
    plt.matshow(cellular_automata)
    plt.show()


def check_state(num_elements, num_alphabet, debug=False):
    """
    This process takes a string of integers as input and verifies that it is a valid starting state.
    """

    start_state = []  # Starting state will be appended one element at a time.
    valid = True

    num_digits = 0
    test_state = input('Enter starting state: ')
    if test_state == 'random':
        for x in range(0, num_elements):
            start_state.append(random.randint(0, num_alphabet-1))
        print("Your random state is ", start_state)

    else:
        for i in test_state:
            if (i.isdigit() and int(i) < num_alphabet):
                if debug == True:
                    print(i, " is a digit and is less than ", num_alphabet)
                num_digits = num_digits + 1
                valid = True
            else:
                print('Incorrect character: ', i)
                valid = False
                break

        while (not valid or num_digits != num_elements):
            if (num_digits != num_elements):
                print('You entered: ', num_digits,
                      ' element(s)\nThis automaton needs: ', num_elements, ' element(s)\n')
            num_digits = 0
            test_state = input('Enter starting state: ')
            for i in test_state:
                if (i.isdigit() and int(i) < num_alphabet):
                    if debug == True:
                        print(i, " is a digit and is less than ", num_alphabet)
                    num_digits = num_digits + 1
                    valid = True
                else:
                    print('Incorrect character: ', i)
                    valid = False
                    break

        for i in test_state:
            start_state.append(int(i))

    return start_state


def evolve_matrix(num_elements, update_rule, debug=False):
    """
    This function translates an identity_matrix into an evolution_matrix, given an update rule.
        num_elements        -- Number of cells in a row.
        update_rule         -- Rule that defines the evolution_matrix.
        debug               -- Flag that offers insight to program if set.
        identity_matrix     -- n by n matrix filled with 0s aside from 1s in the top-left diagonal.
        evolution_matrix    -- n by n matrix that when multiplied to a state, gives the next state.
        row                 -- Temporary variable for each row in the matrix.
    """

    identity_matrix = np.identity(num_elements, int)
    if debug == True:
        print('Identity Matrix:\n', identity_matrix)

    evolution_matrix = []
    row = []
    new_element = 0

    for i in range(0, num_elements):		# Every row in matrix
        row = []
        for j in range(0, num_elements):    # Every element in row
            new_element = 0

            for k in update_rule:           # Every element in update rule
                if j + k >= num_elements:
                    l = j + k - num_elements
                else:
                    l = j + k

                if debug == True:
                    print('l = ', l)
                    print(
                        new_element, '+', identity_matrix[i][l], '=', new_element + identity_matrix[i][l])

                new_element = new_element + identity_matrix[i][l]

                if debug == True:           # Debug -- print the location and value of element
                    print('Element [', i, ', ', j,
                          '] will now be ', new_element)

            row.append(new_element % num_alphabet)

            if debug == True:
                print(new_element, ' % ', num_alphabet,
                      ' = ', new_element % num_alphabet)
                print('Row ', i, ':\n', row)
        evolution_matrix.append(row)
        if debug == True:
            print('\nEvolution Matrix (Row ', i, '):\n',
                  np.matrix(evolution_matrix))

    if debug == True:
        print('Identity Matrix:\n', identity_matrix)

    return np.transpose(evolution_matrix)


def det_update_rule(num_elements, debug=False):
    """
    This function takes a string of numbers as input, which represent cells in a row. If a number exist outside the boundaries of the row, the string must be reentered.
        num_elements        -- Number of cells in row.
        valid               -- Flag that checks whether a string of numbers is valid.
    """

    valid = False

    while not valid:
        update_rule = []

        # Each number represents a cell in relation to the current one. +1 is one to the right. -1 is one to the left.
        string = input("Enter cells to be added for the rule (i.e. -2 0 3): ")
        update_rule = [int(d) for d in re.findall(r'-?\d+', string)]

        for i in update_rule:
            if abs(i) > num_elements:
                print(i, ' is not a valid element for this automaton.\n')
                valid = False
                break
            else:
                valid = True

        if debug == True:
            print('The update rule is ', update_rule)

    return update_rule


def rank(A, atol=1e-13, rtol=0):
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


def nullspace(A, atol=1e-13, rtol=0):
    """Compute an approximate basis for the nullspace of A.
    The algorithm used by this function is based on the singular value
    decomposition of `A`.
    Parameters
    ----------
    A : ndarray
        A should be at most 2-D.  A 1-D array with length k will be treated
        as a 2-D with shape (1, k)
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
    ns : ndarray
        If `A` is an array with shape (m, k), then `ns` will be an array
        with shape (k, n), where n is the estimated dimension of the
        nullspace of `A`.  The columns of `ns` are a basis for the
        nullspace; each element in numpy.dot(A, ns) will be approximately
        zero.

    np.linalg.svd
        Single Value Decomposition
    """

    A = np.atleast_2d(A)
    u, s, vh = svd(A)
    tol = max(atol, rtol * s[0])
    nnz = (s >= tol).sum()
    ns = vh[nnz:].conj().T
    return ns


if __name__ == '__main__':
    """ Main function will serve as the driver for the program.
    It takes user input and runs cellular_automata() with given parameters:
            num_elements	-- Number of elements in automaton
            num_alphabet	-- Number of elements in the alphabet
                                -- In general, our alphabet will be numerical, starting at 0, and incrementing up to user input.
            start_state     -- Starting state of automaton.
                        evolution_matrix     --n by n matrix which, when multiplied to a state in the automaton, will determine the next state.
                        update_rule      -- Rule that governs how the automaton will evolve
                                    -- In general, the rule will be of the form: ( a + b + c + ... + n ) mod m, where a...n are elements of the previous state, and m is the number of elements in the alphabet.

            num_steps		-- Number of steps through which the automaton will evolve
    """

    # Debug mode -- displays math and logic of program where applicable
    debug = input('Debug? (Y/N) ')
    if debug == 'y' or debug == 'Y':
        debug = True
        print('Debug Mode On')
    else:
        debug = False

    num_elements = int(input('Enter # of elements in automaton: '))
    if debug == True:
        print("\t", num_elements, " elements in automaton.", sep='')

    num_alphabet = int(input('Enter # of elements in alphabet: '))

    alphabet = []  # Used to make a nice visualization in the terminal

    for i in range(0, num_alphabet):
        alphabet.append(i)
    print('\tYour alphabet is', *alphabet)

    start_state = check_state(num_elements, num_alphabet, debug)
    if debug == True:
        print('\tStart State: ', start_state)

    update_rule = det_update_rule(num_elements, debug)
    if debug == True:
        print('\tUpdate Rule: ', update_rule)

    evolution_matrix = evolve_matrix(num_elements, update_rule, debug)
    print("Evolution Matrix:\n", np.matrix(evolution_matrix))
    evolution_matrix_rref = np.asarray(evolution_matrix, dtype=np.int32)
    print("Evolution Matrix in Row Reduced Echelon Form:\n",
          rref(evolution_matrix_rref))

    rank_of_evolution_matrix = rank(evolution_matrix)
    print("\nRank of Evolution Matrix: ", rank_of_evolution_matrix)
    nullspace_basis = nullspace(evolution_matrix_rref)
    print("Nullspace of Evolution Matrix: \n", nullspace_basis)

    #if nullspace_basis.size > 0:
    #    res = np.abs(np.dot(evolution_matrix, nullspace_basis)).max()
    #    print("max residual is", res)

    num_steps = int(input('Enter # of steps the automaton will take: '))
    if debug == True:
        print('\t', num_steps, " steps in automaton.")

    print('\nBeginning process...\n')

cellular_automata(num_elements, num_alphabet, start_state,
                  num_steps, evolution_matrix, debug)

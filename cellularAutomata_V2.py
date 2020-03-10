import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors

# Code is referenced from python sympy library. Reference for further explination


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


def cellular_automata(num_elements, num_alphabet, cellular_automata, num_steps):
    """Takes a state and evolves it over n steps.

    The final output will look like:
            0001
            1001
            0101
            1111
    """

    ca_next = cellular_automata[:]  # List representation of next state

    print(*ca_next)  # Prints the starting state

    step = 1  # Number of current state

    M = []
    M.append(ca_next)

    while (step < num_steps):
        ca_next = []  # Reset list for every new step

        # Add elements to next state according to update rule
        for i in range(0, num_elements):
            if i > 0:
                ca_next.append(
                    (cellular_automata[i-1]+cellular_automata[i]) % num_alphabet)

            elif(i == 0):
                ca_next.append(
                    (cellular_automata[num_elements - 1]+cellular_automata[i]) % num_alphabet)

        M.append(ca_next)

        cellular_automata = ca_next[:]  # Update cell list

        step += 1  # Step increment

    #for i in range(0, num_steps-1):
    #    for j in range(0, num_elements):
    #        print(M[i][j], end = " ")
    #    print()

    #plt.matshow(M)
    #plt.show()

    M_rref = np.asarray(M, dtype=np.int32)
    print(rref(M_rref))
    #rref(M_rref, tol=1e-8, debug=True)


if __name__ == '__main__':
    """ Main function will serve as the driver for the program.
    It takes user input and runs cellular_automata() with given parameters:
            num_elements	-- Number of elements in automaton
            num_alphabet	-- Number of elements in the alphabet
                                                    -- In general, our alphabet will be numerical, starting at 0, and incrementing up to user input.
            start_state		-- Starting state of automaton
            update_rule		-- Rule that governs how the automaton will evolve
                                                    -- In general, the rule will be of the form: ( a + b + c + ... + n ) mod m, where a...n are elements of the previous state, and m is the number of elements in the alphabet.
            num_steps		-- Number of steps through which the automaton will evolve
    """

    num_elements = int(input('Enter # of elements in automaton: '))

    num_alphabet = int(input('Enter # of elements in alphabet: '))

    alphabet = []  # Used to make a nice visualization in the terminal

    for i in range(0, num_alphabet):
        alphabet.append(i)
    print('Your alphabet is', *alphabet)

    start_state = []  # Starting state will be appended one element at a time.

    print('Enter starting state, one element per line: ')
    for i in range(0, num_elements):
        element = int(input())
        start_state.append(element)

    # update_rule = input ('Enter update rule: ')

    num_steps = int(input('Enter # of steps the automaton will take: '))

    print('\n\nBeginning process...\n')
    cellular_automata(num_elements, num_alphabet, start_state, num_steps)

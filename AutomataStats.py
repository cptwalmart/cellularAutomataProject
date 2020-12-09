import Nayuki
import numpy as np
import math
import sys

"""*** Notes from meeting on 11/24: Don't need to double count cycles already counted. """
"""5mod5: Need to extend for longer cycle detection. Bardzell says there is another / more cycles that we have not shown."""
"""7mod3: Should output one cycle and one other cycle 20 < C < 90, but not all the other cycles. """
"""9mod3: Extreme irrevesible system that should only produce 1 1-cycle (after certain step, should evolve to 0-state forever)."""


############################# Find T^k = T^n-k (IF there is one) ##########################
# finds the max number of cycle of transtion matrix to compute
def detect_cycle_transtion(transition, alphabet, size):

    u_bound = 100000
    power = 1
    M_list = []
    ZERO = np.zeros((size, size), dtype=int)
    I = np.identity(size, dtype=int)


    #for i in range(u_bound):
    #    result_matrix = (np.linalg.matrix_power(transition, power)) % alphabet
    #    M_list.append(result_matrix)
    #    power += 1

    result_matrix = transition
    for i in range(u_bound):
        M_list.append(result_matrix)
        result_matrix = (np.matmul(transition, result_matrix)) % alphabet
        power += 1

    for i in range(len(M_list)):
        for j in range(i + 1, len(M_list)):
            if i != j:
                # If true all states evloves to Zero State
                if(M_list[j] == I).all():
                    return(j)
                if(M_list[j] == ZERO).all():
                    return(j)
                if (M_list[i] == M_list[j]).all():
                    return(j)
            elif i == len(M_list):
                return(-1)
        else:
            continue

    return(-1)

#######################################     END     ######################################

############################ Find if N(T) == O-matrix #########################
def is_reversable(B, rows, cols, size):
    B.reduced_row_echelon_form()
    result = np.zeros([rows, cols], dtype=int)
    I = np.identity(size, dtype=int)

    for i in range(rows):
        for j in range(cols):
            result[i][j] = B.get(i, j)

    # if reduced_row_echelon_form of transtion matrix = Idn matrix
    # the matrix is reversable
    # else it is irreverable
    if (result == I).all():
        print("reversible")
        f.write("reversible")
        return(True)

    print("irreversible")
    f.write("irreversible")
    return(False)

#######################################     END     ######################################

############################ Find N(T^k -I) = cylces in automata #########################
def detect_unique_cycle(Nullspace_list, alphabet, size):

    # taking an input list
    unique_nullspace = { "nullspace": [], "power": [] }

    # traversing the dict
    idx = 0
    for item in Nullspace_list["nullspace"]:
        if item not in unique_nullspace["nullspace"]:
            unique_nullspace["nullspace"].append(item)
            unique_nullspace["power"].append(Nullspace_list["power"][idx])
        idx += 1

    return(unique_nullspace)

#######################################     END     ######################################

####################################### RREF & NULL #######################################

def generate_automata_stats(data, size , alphabet):
    inputFile = input("Enter in the name of the file you want to write to: ")
    f = open(inputFile, "w") # for output file.
    
    rows = cols = size
    F = Nayuki.PrimeField(alphabet)
    B = Nayuki.Matrix(rows, cols, F)

    # Nayuki Matrix "B"
    inc = 0
    for i in range(size):  # For each column
        for j in range(size):
            B.set(i,j,data[inc])
            inc += 1

    # Transisition Matrix "transition"
    transition = np.zeros([rows, cols], dtype=int)
    result_matrix = np.zeros([rows, cols], dtype=int)

    for i in range(rows):
        for j in range(cols):
            transition[i][j] = B.get(i, j)

    I = np.identity(size, dtype=int)        # Identity Matrix
    power = 1                               # power
    reverable = is_reversable(B, rows, cols, size)   # is automate reverable
    n = detect_cycle_transtion(transition, alphabet, size)  # max steps

    #print("\nrref for matrix:")
    #B.reduced_row_echelon_form()
    #print(B)

    #print("\nnullspace for matrix:")
    #Basis = B.get_nullspace()
    #print(Basis)

    #######################################     END     #######################################
    ####################################### NULL POW(N) #######################################

    result_matrix_pow = transition
    Nullspace_list = { "nullspace": [], "power": [] }
    power = 1
    for i in range(n):
        #print("\n(T)^{} - I: ".format(power))
        #result_matrix = ( np.linalg.matrix_power( transition, power ) - I ) % alphabet

        if(i > 0):
            result_matrix_pow = (np.matmul(transition, result_matrix_pow)) % alphabet
        result_matrix = (result_matrix_pow - I) % alphabet

        # Set Nayuki Matrix to reult of (T)^n - I
        for i in range(size):  # For each column
            for j in range(size):
                B.set( i,j,int( result_matrix[i,j] ))

        #print("\nrref for (T)^{} - I: ".format(power))
        B.reduced_row_echelon_form()
        #print("\nnullspace for (T)^{} - I: ".format(power))
        Basis = B.get_nullspace()

        Nullspace_list["nullspace"].append(Basis)
        Nullspace_list["power"].append(power)

        power += 1

    # Get Automata Stats
    unique_nullspace = detect_unique_cycle( Nullspace_list, alphabet, size )  # max steps
    Automata_stats = []

    # Add final Cycle since the entire system is reverable
    if(reverable):
        result_matrix = I
        unique_nullspace["nullspace"].append(result_matrix)
        unique_nullspace["power"].append(power)

    #Automata_stats.append( { "nullspace": [], "power": 0, "cycles_size": 0, "cycles_count": 0, "states": 0} )
    # Prints all of the unique nullspaces to a file.
    for i in range( len(unique_nullspace["nullspace"]) ):
        power  = unique_nullspace["power"][i]
        cycles_size = len( unique_nullspace["nullspace"][i] )
        states = pow( alphabet, cycles_size )
        Automata_stats.append( { "nullspace": [], "power": 0, "cycles_size": 0, "cycles_count": 0, "states": 0} )

        subtract_repeat_states = 0
        if(i != 0):
            # Checks for divisibility now!
            for j in range(i, 0, -1):
                if j > 0 and power % unique_nullspace["power"][j-1] == 0:
                    item = Automata_stats[j-1]
                    subtract_repeat_states += item["states"]

            #print("Value for States for power {}: {}".format(power, states))
            #print("States to be subtracted for power {}: {}".format(power, subtract_repeat_states))
            states -= subtract_repeat_states


        Automata_stats[i]["nullspace"] = unique_nullspace["nullspace"][i]
        Automata_stats[i]["power"] = power
        Automata_stats[i]["cycles_size"] = cycles_size
        Automata_stats[i]["cycles_count"] = states / power
        Automata_stats[i]["states"] = states

        #prev = power

        f.write("\n")
        f.write("Length: {}\n".format(power))
        f.write("Dimension of nullspace: {}\n".format(cycles_size))
        f.write("Cycles Copies: {}\n".format(int(states / power)))
        f.write("States: {}\n".format(states))

        if np.array_equal(Automata_stats[i]["nullspace"], I):
            f.write("Nullspace: {}\n".format("Entire Cellular Automata"))
        else:
            f.write("Nullspace: {}\n".format(Automata_stats[i]["nullspace"]))

    f.close()

    return Automata_stats
#######################################     END     #######################################
import Nayuki
import numpy as np

####################################### 3 x 3 mod(5) #######################################
#F = Nayuki.PrimeField(5)
#B = Nayuki.Matrix(3, 3, F)
#size = 3
#data = [1, 2, 3, 2, 4, 0, 1, 2 ,3] # nullspace = [[3, 1, 0]]
#data = [2, 4, 1, 2, 1, 0, 4, 3, 4] # nullspace = []


#######################################     END     #######################################

####################################### 4 x 4 mod(5) #######################################
#alphabet = 5 # our mod(p)
#F = Nayuki.PrimeField(alphabet)
#B = Nayuki.Matrix(4, 4, F)
#size = 4
#rows = cols = size
#data = [2, 4, 1, 2,
#        1, 0, 4, 3,
#        4, 0, 3, 2,
#        2, 0, 0, 0] # nullspace = [] # cycle = 0 - 1632
#data = [2, 4, 1, 2,
#        1, 0, 4, 3,
#        4, 0, 3, 2,
#        0, 0, 0, 0] # nullspace = [[2, 1, 0, 1]] # cycle = 0 - 7637

#######################################     END     #######################################

####################################### 6 x 6 mod(5) #######################################
#alphabet = 5 # our mod(p)
#F = Nayuki.PrimeField(alphabet)
#B = Nayuki.Matrix(6, 6, F)
#size = 6
#rows = cols = size
#data = [0, 1, 1, 0, 0, 0,
#        0, 0, 1, 1, 0, 0,
#        0, 0, 0, 1, 1, 0,
#        0, 0, 0, 0, 1, 1,
#        1, 0, 0, 0, 0, 1,
#        1, 1, 0, 0, 0, 0] # nullspace = [[4, 1, 4, 1, 4, 1]]

#######################################     END     #######################################

####################################### 9 x 9 mod(2) #######################################
""" alphabet = 2 # our mod(p)
F = Nayuki.PrimeField(alphabet)
B = Nayuki.Matrix(9, 9, F)
size = 9
rows = cols = size
data = [0, 1, 1, 0, 0, 0, 0, 0, 1,
        1, 0, 1, 1, 0, 0, 0, 0, 0,
        0, 1, 0, 1, 1, 0, 0, 0, 0,
        0, 0, 1, 0, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 0, 1, 1, 0, 0,
        0, 0, 0, 0, 1, 0, 1, 1, 0,
        0, 0, 0, 0, 0, 1, 0, 1, 1,
        1, 0, 0, 0, 0, 0, 1, 0, 1,
        1, 1, 0, 0, 0, 0, 0, 1, 0,] """

#######################################     END     #######################################

""" ####################################### 8 x 8 mod(3) #######################################
alphabet = 3 # our mod(p)
size = 8
F = Nayuki.PrimeField(alphabet)
B = Nayuki.Matrix(size, size, F)
rows = cols = size

data = [1, 1, 1, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 0, 0, 0, 0,
        0, 0, 1, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 0, 0,
        0, 0, 0, 0, 1, 1, 1, 0,
        0, 0, 0, 0, 0, 1, 1, 1,
        1, 0, 0, 0, 0, 0, 1, 1,
        1, 1, 0, 0, 0, 0, 0, 1]


#######################################     END     ####################################### """












""" ####################################### 5 x 5 mod(5) #######################################
alphabet = 5 # our mod(p)
size = 5
F = Nayuki.PrimeField(alphabet)
B = Nayuki.Matrix(size, size, F)
rows = cols = size

data = [0, 1, 0, 0, 1,
        1, 0, 1, 0, 0,
        0, 1, 0, 1, 0,
        0, 0, 1, 0, 1,
        1, 0, 0, 1, 0]

#######################################     END     ####################################### """

""" ####################################### 9 x 9 mod(3) #######################################
alphabet = 3 # our mod(p)
F = Nayuki.PrimeField(alphabet)
B = Nayuki.Matrix(9, 9, F)
size = 9
rows = cols = size
data = [1, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 1, 1, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 0, 0, 0, 0, 0,
        0, 0, 1, 1, 1, 0, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 0, 0, 0,
        0, 0, 0, 0, 1, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 1, 1, 1, 0,
        0, 0, 0, 0, 0, 0, 1, 1, 1,
        1, 0, 0, 0, 0, 0, 0, 1, 1]

#######################################     END     ####################################### """

####################################### 7 x 7 mod(3) #######################################
alphabet = 3 # our mod(p)
size = 7
F = Nayuki.PrimeField(alphabet)
B = Nayuki.Matrix(size, size, F)
rows = cols = size

data = [0, 1, 0, 0, 0, 1, 1,
        1, 0, 1, 0, 0, 0, 1,
        1, 1, 0, 1, 0, 0, 0,
        0, 1, 1, 0, 1, 0, 0,
        0, 0, 1, 1, 0, 1, 0,
        1, 0, 0, 1, 1, 0, 1,
        1, 1, 0, 0, 1, 1, 0]

#######################################     END     #######################################

############################# Find T^k = T^n-k (IF there is one) ##########################
# finds the max number of cycle of transtion matrix to compute
def detect_cycle_transtion(transition, alphabet):

    u_bound = 100000
    power = 1
    M_list = []


    for i in range(u_bound):
        result_matrix = (np.linalg.matrix_power(transition, power)) % alphabet
        M_list.append(result_matrix)
        power += 1

    for i in range(len(M_list)):
        for j in range(i + 1, len(M_list)):
            if i != j:
                if (M_list[i] == M_list[j]).all():
                    #msg = ("CYCLE DETECTED FROM STEP {} TO STEP {}".format(i, j))
                    return(j)
            elif i == len(M_list):
                #msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
                return(-1)
        else:
            continue
    #msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
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
        print("reverable")
        return(True)
    print("irreverable")
    return(False)

#######################################     END     ######################################

############################ Find N(T^k -I) = cylces in automata #########################
def detect_unique_cycle(Nullspace_list, alphabet, size):

    # taking an input list 
    unique_nullspace = { "nullspace": [], "power": []} 
    
    # travesing the dict 
    #for item in Nullspace_list["nullspace"]: 
    #    if item not in unique_nullspace["nullspace"]: 
    #        unique_nullspace["nullspace"].append(item) 

    # travesing the dict 
    idx = 0
    for item in Nullspace_list["nullspace"]: 
        if item not in unique_nullspace["nullspace"]: 
            unique_nullspace["nullspace"].append(item)
            unique_nullspace["power"].append(Nullspace_list["power"][idx])
        idx += 1

    return(unique_nullspace)

#######################################     END     ######################################

####################################### RREF & NULL #######################################

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
n = detect_cycle_transtion(transition, alphabet)  # max steps

print("\nrref for matrix:")
B.reduced_row_echelon_form()
print(B)

print("\nnullspace for matrix:")
Basis = B.get_nullspace()
print(Basis)

#######################################     END     #######################################
""" 
power = 1
for i in range(n):
    print("\n(T)^{}: ".format(power))
    result_matrix = (np.linalg.matrix_power(transition, power)) % alphabet
    print(result_matrix)
    power += 1
 """
####################################### NULL POW(N) #######################################

Nullspace_list = { "nullspace": [], "power": []}
power = 1
for i in range(n):
    #print("\n(T)^{} - I: ".format(power))
    result_matrix = (np.linalg.matrix_power(transition, power) - I) % alphabet
    #print(result_matrix)

    # Set Nayuki Matrix to reult of (T)^n - I
    for i in range(size):  # For each column
        for j in range(size):
            B.set(i,j,int(result_matrix[i,j]))

    #print("\nrref for (T)^{} - I: ".format(power))
    B.reduced_row_echelon_form()
    #print(B)

    #print("\nnullspace for (T)^{} - I: ".format(power))
    Basis = B.get_nullspace()
    #print(Basis)
    
    Nullspace_list["nullspace"].append(Basis)
    Nullspace_list["power"].append(power)

    power += 1



# Get Automata Stats
unique_nullspace = detect_unique_cycle(Nullspace_list, alphabet, size)  # max steps
Automata_stats = []

for i in range( len(unique_nullspace["nullspace"]) ):
    power  = unique_nullspace["power"][i]
    cylces_size = len(unique_nullspace["nullspace"][i])
    states = pow( alphabet, cylces_size)
    Automata_stats.append({ "nullspace": [], "power": 0, "cylces_size": 0, "cylces_count": 0, "states": 0})

    subtract_repeat_states = 0
    if(i != 0):
        for j in range(i, 0, -1):
            item = Automata_stats[j-1]
            subtract_repeat_states += item["states"]
        states -= subtract_repeat_states
            


    Automata_stats[i]["nullspace"] = unique_nullspace["nullspace"][i]
    Automata_stats[i]["power"] = power
    Automata_stats[i]["cylces_size"] = cylces_size
    Automata_stats[i]["cylces_count"] = states / power
    Automata_stats[i]["states"] = states

    print("\n")
    print("Length:", power)
    print("Cylces Count:", cylces_size)
    print("Cylces Copies:", states / power)
    print("States:", states)
    print("Nullspace:", Automata_stats[i]["nullspace"])


#######################################     END     #######################################
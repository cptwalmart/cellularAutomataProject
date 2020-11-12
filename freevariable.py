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

####################################### 6 x 6 mod(5) #######################################
alphabet = 2 # our mod(p)
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
        1, 1, 0, 0, 0, 0, 0, 1, 0,]

#######################################     END     #######################################

############################# Find T^k = T^n-k (IF there is one) ##########################
def detect_cycle(transition, alphabet):

    u_bound = 1000
    power = 1
    M_list = []


    for i in range(u_bound):
        result_matrix = (np.linalg.matrix_power(transition, power)) % alphabet
        M_list.append(result_matrix)
        power += 1

    for i in range(len(M_list)):
        for j in range(len(M_list)):
            if i != j:
                if (M_list[i] == M_list[j]).all():
                    msg = ("CYCLE DETECTED FROM STEP {} TO STEP {}".format(i, j))
                    return(j)
            elif i == len(M_list):
                msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
                return(msg)
        else:
            continue
    msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
    return(msg)

def detect_cycle2(transition, alphabet):

    u_bound = 10000
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
                    msg = ("CYCLE DETECTED FROM STEP {} TO STEP {}".format(i, j))
                    return(j+1)
            elif i == len(M_list):
                msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
                return(msg)
        else:
            continue
    msg = ("NO CYCLES DETECTED IN THIS RANGE. TRY USING MORE STEPS.")
    return(msg)


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
n = detect_cycle2(transition, alphabet)  # max steps

print("\nrref for matrix:")
B.reduced_row_echelon_form()
print(B)

print("\nnullspace for matrix:")
Basis = B.get_nullspace()
print(Basis)

#######################################     END     #######################################

power = 1
for i in range(n):
    print("\n(T)^{}: ".format(power))
    result_matrix = (np.linalg.matrix_power(transition, power)) % alphabet
    print(result_matrix)
    power += 1

####################################### NULL POW(N) #######################################

power = 1
for i in range(n):
    print("\n(T)^{} - I: ".format(power))
    result_matrix = (np.linalg.matrix_power(transition, power) - I) % alphabet
    print(result_matrix)

    # Set Nayuki Matrix to reult of (T)^n - I
    for i in range(size):  # For each column
        for j in range(size):
            B.set(i,j,int(result_matrix[i,j]))

    print("\nrref for (T)^{} - I: ".format(power))
    B.reduced_row_echelon_form()
    print(B)

    print("\nnullspace for (T)^{} - I: ".format(power))
    Basis = B.get_nullspace()
    print(Basis)
    
    power += 1

#######################################     END     #######################################
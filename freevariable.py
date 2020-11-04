import Nayuki
import numpy as np



F = Nayuki.PrimeField(5)

# B is transistion matrix
B = Nayuki.Matrix(6, 6, F)

# C is the transition matrix - Identity.
C = Nayuki.Matrix(6, 6, F)



tmp = Nayuki.Matrix(5, 1, F)
res = Nayuki.Matrix(5, 1, F)

cols = 6
rows = 6

# Going to copy Nayuki matrix B into this numpy matrix.
transit = np.zeros([rows, cols], dtype=int)
transit_tmp = np.zeros([rows, cols], dtype=int)

# Temporary storage for our transition matrix.
data = [0, 1, 1, 0, 0, 0,
        0, 0, 1, 1, 0, 0,
        0, 0, 0, 1, 1, 0,
        0, 0, 0, 0, 1, 1,
        1, 0, 0, 0, 0, 1,
        1, 1, 0, 0, 0, 0]

# Identity Matrix.
I = np.identity(6)


# Convert data to Nayuki type matrix.
inc = 0
for i in range(rows):  # For each column
    for j in range(cols):
        B.set(i,j,data[inc])
        inc += 1



print("Nullspace testing *** \n")
print("mod 5 matrix:\n")
print(B)

for i in range(rows):
    for j in range(cols):
        transit[i][j] = B.get(i, j)



print("rref for matrix:")
B.reduced_row_echelon_form()
print(B)


print("nullspace for matrix:")

Basis = B.get_nullspace()
print(Basis)



# Get dimensions of the Basis.
# Make into numpy array anmd use numpy.add and numpy.multiply.
res = []


# Lines 77 - 83 I made following up on what Bardzell told us about adding all of the vectors within the basis.
# Will be incorporated after.
for i in range(0, len(Basis)):
    tmp = np.array([Basis[i]])
    res.append([tmp])

# To add up all the vectors in the Basis.
sumOfBasis = [sum(i) for i in zip(*res)]

# Cycle detection work.


print("\nFor cycle detection: \n")

# For multiple powers of the same matrix (going up to 6 for this example).
# First, convert cycles Basis to a numpy matrix.


pow = 1
n = 6
for i in range(n):

    transit_tmp = np.power(transit, pow)
    A = transit_tmp - I

    # Must mod A after every operation to ensure it is in same prime field.
    for i in range(rows):
        for j in range(cols):
            A[i][j] = A[i][j] % 5



    print("(T)^n - I power: ", pow, "\n\n", A)
    # Have to convert back to Nayuki inorder to get null space.
    nay_cycles = Nayuki.Matrix(6, 6, F)
    for j in range(rows):
        for k in range(cols):
            val = int(A[j][k])
            nay_cycles.set(j,k,val)


    tmp_cycles = nay_cycles.get_nullspace()

    print("\nCycle Basis for (Transition - Identity) To the power of ", pow, "\n\n", tmp_cycles, "\n\n")
    pow += 1

import Nayuki

F = Nayuki.PrimeField(5)
B = Nayuki.Matrix(3, 3, F)
cols = 3
rows = 3
data = [1, 2 ,3, 2, 4, 0, 1, 2 ,3]
inc = 0
for i in range(rows):  # For each column
    for j in range(cols):
        B.set(i,j,data[inc])
        inc += 1
#print(B)
B.reduced_row_echelon_form()
#print(B)
#test = B.find_pivots()
#print(test)
test = B.get_nullspace()
print(test)
import numpy as np
import sympy as sp

from sympy import Matrix, Rational, mod_inverse, pprint

#def modinv(n, mod):
#  '''
#  Lazily finds the multiplicative inverse of n modulo mod.
#  '''
#  for x in range(1, mod):
#    if (n * x) % mod == 1: return x
#  else:
#    raise ArithmeticError('%i has no multiplicative inverse modulo %i.' % (n, mod))

# A naive method to find modulor  
# multiplicative inverse of 'a'  
# under modulo 'm' 
def modinv(a, m) : 
  a = a % m
  for x in range(1, m) : 
      if ((a * x) % m == 1) : 
          return x 
      else:
        raise ArithmeticError('%i has no multiplicative inverse modulo %i.' % (a, m))

def firstnonzero(row):
  '''
  Finds the index of the first non-zero element of the row.
  return next((i for i, x in enumerate(row) if x), None)
  '''
  print(row)
  for i, r in enumerate(row):
    if r != 0: return i
  else:
    raise Exception('No non-zeros elements found.')

def swaprows(M, i, j):
  '''
  Swaps rows i and j of the matrix M.
  '''
  M[i], M[j] = M[j], M[i]

def subrow(M, i):
  '''
  Subtracts row i from each other row in the matrix M.
  Assumes that the first non-zero element of i is a 1.
  '''
  f = firstnonzero(M[i])
  for j in range(M.shape[0]):
    if i == j: continue
    M[j] -= M[j,f] * M[i]

def normrow(M, i, mod):
  '''
  Normalizes row i of the matrix M such that the first non-zero element is 1.
  '''
  f = firstnonzero(M[i])
  M[i] *= modinv(M[i,f], mod)
  M[i] %= mod
    
def modrref(M, mod):
  '''
  Computes the row-reduced echelon form of the matrix M modulo mod.
  '''
  r = 0
  while r < M.shape[0]:
    # Ignore non-zero rows.
    try: f = firstnonzero(M[r])
    except:
      r += 1
      continue

    # Rule 1: Swap with the row above if out of order.
    if r > 0:
      swap = False
      try: g = firstnonzero(M[r - 1])
      except: swap = True
      if swap:
        swaprows(M, r, r - 1)
        continue
    
    # Rule 2: Normalize each row
    normrow(M, r, mod)
    
    # Rule 3: Subtract it from the others
    subrow(M, r)
    r += 1
  M = organize(M)
  return M

def matmodinv(M, mod):
  '''
  Computes the multiplicative inverse of M modulo mod.
  '''
  assert M.shape[0] == M.shape[1]
  I = np.identity(M.shape[0], M.dtype)
  N = np.concatenate((M, I), axis = 1)
  modrref(N, mod)
  M = N[:,M.shape[0]:] % mod
  return M

def organize(B, debug=False):
        B = np.asarray(B, dtype=int)        
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
                pivots_pos.append((r, c))

            if pivot != r:
              # Swap current row and pivot row
              A[[pivot, r], c:cols] = A[[r, pivot], c:cols]
              row_exchanges[[pivot, r]] = row_exchanges[[r, pivot]]

              if debug:
                print("Swap row", r, "with row", pivot, "Now:")
                print(A)

            r += 1
            # Check if done
            if r == rows:
                break
        return (A)

def mod(x,modulus):
    numer, denom = x.as_numer_denom()
    return numer*mod_inverse(denom,modulus) % modulus

def rref_sp(A, m):
  B_rref = A.rref(iszerofunc=lambda x: x % m==0)
  pprint(B_rref[0].applyfunc(lambda x: mod(x,m)))

if __name__ == "__main__":
  #cellular_automata = np.array([[1,2],[3,4]], dtype=int)
  #cellular_automata = np.array([[0,1],[1,0]], dtype=int)
  cellular_automata = np.array([[8,1,6],[3,5,7],[4,9,2]], dtype=int)
  m = 5

  B = Matrix(cellular_automata)
  C = Matrix(cellular_automata)
  cellular_automata = modrref(cellular_automata, m)
  print(cellular_automata)

  #B = Matrix([
  #      [2,2,3,2,2],
  #      [2,3,1,1,4],
  #      [0,0,0,1,0],
  #      [4,1,2,2,3]
  #], dtype=int)

  rref_sp(B, m)

  #C_null = C.nullspace(iszerofunc=lambda x: x % 5==0) 
  #pprint(C_null[0].applyfunc(lambda x: mod(x,5)))
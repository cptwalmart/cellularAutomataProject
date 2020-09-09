import numpy as np

def modinv(n, mod):
  '''
  Lazily finds the multiplicative inverse of n modulo mod.
  '''
  for x in range(1, mod):
    if (n * x) % mod == 1: return x
  else:
    raise ArithmeticError('%i has no multiplicative inverse modulo %i.' % (n, mod))

def firstnonzero(row):
  '''
  Finds the index of the first non-zero element of the row.
  '''
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
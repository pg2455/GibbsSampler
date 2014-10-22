import math
def radix(A):
  n= len(A)
  for D in range(3)[::-1]:
    C=[[] for i in range(10)]
    for i in range(n):
      bucket = (A[i]/10**D) % 10
      C[bucket].append(A[i])
    A = [j for a_list in C for j in a_list]
  return A

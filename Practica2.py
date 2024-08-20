import time 
import random
import sys

sys.setrecursionlimit(1_000_000)

def QuickSort(A, p, r):
    if p < r:
        q = Particionar(A, p, r)
        QuickSort(A, p, q-1)
        QuickSort(A, q+1, r)
    
def Particionar(A, p, r):
    x = A[r]
    i = p-1
    for j in range(p, r):
        if A[j] <= x : 
            i = i + 1
            A[i], A[j] = A[j], A[i]
    
    A[i+1], A[r] = A[r], A[i+1]
    return i+1

def LlenarArreglo(arreglo,n,LimiteI, LimiteS):
    for i in range(n):
        arreglo.append(random.randint(LimiteI, LimiteS)) 

def main():
    A = []
    LlenarArreglo(A, 10, 0, 10)
    print(A)
    QuickSort(A,0, len(A)-1)
    print(A)

main()
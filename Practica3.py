import random 
import time
import math

def CountingSort(A):
    k = max(A)
    C = []
    B = [] 
#Formamos el arrglo auxiliar que va a almacenar llenandolo de 0
    for i in range (k+1): #Es k+1 por que se cuenta el indice 0
        C.append(0)
    
    for i in range (len(A)):
        B.append(0)
    """ for i in range(k):
        C[i] = 0    """
    #Para obtener el acomulado 
    for j in range(len(A)):
        #Tomamos el valor de A en el indice j y con eso vamos a ese indice dentro del arreglo, y como este numero corresponde a cierto indice en C, incrementamos el valor del arreglo C que contiene el contenido de ese valor 
        C[A[j]] = C[A[j]] + 1
    
    for i in range(1,k+1):
        #Empieza en 1 para que no nos de el indie -1 en la primera iteracion
        C[i] = C[i] + C[i-1]
        
    for j in range(len(A)-1, -1, -1):
        B[C[A[j]]-1] = A[j]
        C[A[j]] -= 1
    return B

def LlenarArreglo(arreglo,n,LimiteI, LimiteS):
    for i in range(n):
        arreglo.append(random.randint(LimiteI, LimiteS)) #Rango de los numeros
        
def CountigSort_RadixSort(A):
    k = max(A)
    d = math.log10()
    C = []
    B = [] 
#Formamos el arrglo auxiliar que va a almacenar llenandolo de 0
    for i in range (k+1): #Es k+1 por que se cuenta el indice 0
        C.append(0)
    
    for i in range (len(A)):
        B.append(0)
    """ for i in range(k):
        C[i] = 0    """
    #Para obtener el acomulado 
    for j in range(len(A)):
        #Tomamos el valor de A en el indice j y con eso vamos a ese indice dentro del arreglo, y como este numero corresponde a cierto indice en C, incrementamos el valor del arreglo C que contiene el contenido de ese valor 
        C[A[j]] = C[A[j]] + 1
    
    for i in range(1,k+1):
        #Empieza en 1 para que no nos de el indie -1 en la primera iteracion
        C[i] = C[i] + C[i-1]
        
    for j in range(len(A)-1, -1, -1):
        B[C[A[j]]-1] = A[j]
        C[A[j]] -= 1
    return B
def ObtenDigito(num, i):
    return  (num//10 ** i) % 10
    
A = []
LlenarArreglo(A, 10, 0, 10)
print(A)
B =CountingSort(A)
print(B)
    
        
#List comprehesion
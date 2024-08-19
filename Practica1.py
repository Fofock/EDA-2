import random
#Desarrollar los explciaciones de los algoritmos de ordenamiento de este modulo

def BubbleSort(A):
    n = len(A)
    for i in range(n-1):
        for j in range (n-1-i):
            if A[j] > A[j+1]:
                A[j],A[j+1] = A[j+1], A[j]

def BubbleSortOptimizado(A):
    n = len(A)
    #Ramge llega hasta n sin tomar n 
    for i in range(n-1):
        orden = True
        for j in range(n-1-i):
            if A[j] >  A[j+1]:
                orden = False
                A[j], A[j+1] = A[j+1], A[j]
        if orden == True:
            break
                
def MergeSort(A,p,r):
    #Verificamos que la lista sea mayor a un elemento 
    if p < r:
        #Obtenemos el valor de la mitad de la longitud de la lista para poder dividirla
        q = (p+r)//2
        #Llamamos recursivamente al Merge Sort ya con el valor de q para "dividir" imaginariamente la lista, obtenemos la lista derecha que va desde el inicio "p" hasta la mitad "q", después tomamos el valor que le sigue a q "q+1" para el inicio de la lista derecha y tomamos r como el final de la segunda lista
        
        MergeSort(A,p,q)
        MergeSort(A,q+1,r)
        Merge(A,p,q,r)
        
def Merge(A,p,q,r):
    #Lista izquierda 
    izq = A[p:q+1]
    
    #Lista derecha 
    der = A[q+1:r+1]
    
    i = 0
    j = 0
    #Establecemos este valor porque queremos que el rango sea el tamaño de las nuevas listas creadas 
    for k in range(p, r+1):
        #Los valores que ponemos se colocan en el mismo A, sobreescribimos 
        #Checa que el arreglo derecho no se haya acabado(Primera condición), esto porque r-q nos da el indice de la mitad del arreglo; se coloca el igual porque en el caso que ambas listas tengan un elemento su valor el valor de sus indices sera 0 
        #Va avanzando el indice i hasta que llega al final de este, lo que nos permite conocer el final que es q, que es la mitad - la mitad más uno(Segunda condición)
        #Compara los valores de los arrglos para determinar cual copia para cambiar el orden
        # "r-q" tamaño del derecho
        # "q-p+1" tamaño del izquierdo
        
        if  (j >= r-q) or ((i < q-p+1) and (izq[i] < der[j])):
            A[k] =izq[i]
            i += 1
        else:
            A[k] = der[j]
            j += 1 
            
def MergeSortInverso(A,p,r):
    #Verificamos que la lista sea mayor a un elemento 
    if p < r:
        #Obtenemos el valor de la mitad de la longitud de la lista para poder dividirla
        q = (p+r)//2

        MergeSortInverso(A,p,q)
        MergeSortInverso(A,q+1,r)
        Merge(A,p,q,r)

def MergeInverso(A,p,q,r):
    #Lista izquierda 
    izq = A[p:q+1]
    
    #Lista derecha 
    der = A[q+1:r+1]
    
    i = 0
    j = 0
    #Establecemos este valor porque queremos que el rango sea el tamaño de las nuevas listas creadas 
    for k in range(p, r+1):
        
        if  (j >= r-q) or ((i < q-p+1) and (izq[i] > der[j])):
            A[k] =izq[i]
            i += 1
        else:
            A[k] = der[j]
            j += 1            
        
        
        
    
A = [4,3,2,5,1]            
B = A[:] #Funcion splice
C = A[:]
"""for i in range(100):
    A.append(random.randint(1,10))"""

print("Desordenado", A)
BubbleSort(A)
print("Ordenado", A)

print("Desordenado", B)
BubbleSortOptimizado(B)
print("Ordenado", B)

print("Desordenado", C)
MergeSort(C,0,len(C)-1)
print("Ordenado", C)


#Un analisis de complejidad me mide como se comporta el algoritmo dependeiendo de la cantidad de entrada de datos, no mide velocidad

#if __name__ = __main__: invetigar esta sintaxis 
    
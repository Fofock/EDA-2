import time 
import random
import sys
import matplotlib as plt

sys.setrecursionlimit(1_000_000) #LIMITE DE RECURSIVIDAD
#SELECCIONA PIVOTE, MENORES A LA IZQUIERDA, MAYORES A LA DERECHA
def QuickSort(A, p, r):
    if p < r:
        q = Particionar(A, p, r)
        QuickSort(A, p, q-1)
        QuickSort(A, q+1, r)
    
def Particionar(A, p, r):
    x = A[r] #SE TOMA COMO PIVOTE EL ULTIMO ELEMENTO Y SU VALOR SE LE ASIGNA A X
    i = p-1 # INICIAMOS A I EN -1
    for j in range(p, r):
        if A[j] <= x : #COMPARACIÓN PARA SABER SI ES MENOR O MAYOR 
            i = i + 1 #SE CAMBIA CON EL INIDICE CORRESPONDINTE A LA ITERACIÓN
            A[i], A[j] = A[j], A[i]
    
    A[i+1], A[r] = A[r], A[i+1] #SI EL VALOR EN EL INDICE J ES MAYOR ESE VALOR LO ENVIA AL FINAL
    return i+1 #SE REGRESA EL INDICE DEL PIVOTE EN DONDE YA SE CUMPLE LA CONDICIÓN DE,MENORES A LA IZQUIERDA, MAYORES A LA DERECHA

def RandQuickSort(A, p, r):
    if p < r:
        q = ParticionarRand(A, p, r)
        QuickSort(A, p, q-1)
        QuickSort(A, q+1, r)

def ParticionarRand(A, p ,r):
    k = random.randint(p,r)
    x = A[k] #SE TOMA COMO PIVOTE UN INDICE ALEATORIO Y SU VALOR SE LE ASIGNA A X
    A[k], A[r] = A[r], A[k]  #CAMBIA EL PIVOTE AL FINAL 
    i = p-1 # INICIAMOS A I EN -1
    for j in range(p, r):
        if A[j] <= x : #COMPARACIÓN PARA SABER SI ES MENOR O MAYOR 
            i = i + 1 #SE CAMBIA CON EL INIDICE CORRESPONDINTE A LA ITERACIÓN
            A[i], A[j] = A[j], A[i]
    
    A[i+1], A[r] = A[r], A[i+1] #SI EL VALOR EN EL INDICE J ES MAYOR ESE VALOR LO ENVIA AL FINAL
    return i+1 #SE REGRESA EL INDICE DEL PIVOTE EN DONDE YA SE CUMPLE LA CONDICIÓN DE,MENORES A LA IZQUIERDA, MAYORES A LA DERECHA
    
def LlenarArreglo(arreglo,n,LimiteI, LimiteS):
    for i in range(n):
        arreglo.append(random.randint(LimiteI, LimiteS)) 
        
def HeapSort(A):
    MaxHeapInit(A)
    n = len(A)
    for i in range(n-1, 1, -1):
        A[0], A[i] = A[i], A[0]
        n = n-1
        MaxHeapify(A, 0, n)

#HACE QUE SOLO SE LLAME AL MAXHEAP PARA LA MITAD, YA QUE SOLO LA MITAD DE EL ARREGLO TIENE HIJOS
def MaxHeapInit(A):
    n = len(A)
    #EL VALOR QUE TOMA I EN UN BUCLE FOR ES EL PRIMER ARGUMENTO DEL IN RANGE
    for i in range((n//2), -1, -1):
        MaxHeapify(A, i, n)
        
#SE COMPARAN LOS HIJOS CON EL PADRE PARA SABER SI SE DEBE DE RALIZAR UN CAMBIO PARA LLEGAR AL HEAP; ES IMPORTANTE NOTAR QUE SI SE REALIZA UN CAMBIO EN EL SUBPADRE DE UNA SUBRAMA SE TIENE QUE VERIFICAR DE NUEVO PARA GRANATIZAR QUE SE CUMPLA LA ESTRUCTURA DEL HEAP
def MaxHeapify(A, i, n):
    SonL = 2*i + 1
    SonR = 2*i + 2
    posMAx = None
    if (SonL < n) and (A[SonL] > A[i]):
        posMAx = SonL
    else:
        posMAx = i
    if (SonR < n) and (A[SonR] > A[posMAx]):
        posMAx = SonR
    if posMAx != i: #ESTO QUIERE DECIR QUE SI ALGUNO DE LOS HIJOS ES MAYOR AL PADRE, DE AHI EL INTERCAMBIO
        A[i], A[posMAx] = A[posMAx], A[i] 
        MaxHeapify(A, posMAx, n)
        
def medirQuicks(fn, A, p, r, arrTiempos):
    Ti = time.perf_counter()
    fn(A, p, r)
    Tf = time.perf_counter()
    Tt = Tf - Ti
    #print(f"El algoritmo tardo {Tt} segundos en ordenar la lista" )
    arrTiempos.append(Tt)

def medirHeap(fn, A, arrTiempos):
    Ti = time.perf_counter()
    fn(A)
    Tf = time.perf_counter()
    Tt = Tf - Ti
    #print(f"El algoritmo tardo {Tt} segundos en ordenar la lista" )
    arrTiempos.append(Tt)

def TimepoPromedio(arrTiempos, algoritmo, elemetos):
    n = len(elemetos)
    t = (sum(arrTiempos) / 3)
    print(f"El tiempo promedio del algoritmo {algoritmo} para {n} elementos es {t} segundos" )
    return t    

def graficas(TQSG, TQSRG, THSG, elementos):
    # Graficar los tiempos de ejecución para Bubble Sort
    plt.plot(elementos, TQSG, label="Quick Sort", color="red", marker='o')
    
    # Graficar los tiempos de ejecución para Bubble Sort Optimizado
    plt.plot(elementos, TQSRG, label="Quick Sort Random", color="blue", marker='x')
    
    # Graficar los tiempos de ejecución para Merge Sort
    plt.plot(elementos, THSG, label="Heap Sort", color="green", marker='s')
    
    # Configurar la gráfica
    plt.xlabel("Número de elementos")
    plt.ylabel("Tiempo de ejecución (s)")
    plt.title("Comparación de tiempos de ejecución entre algoritmos")
    plt.legend()
    plt.grid(True)
    
    # Mostrar la gráfica
    plt.show()

def ejecucion(elementos):       
    A = []   
    #Mejor de los casos
    A.sort
    #Peor de los casos 
    #A.sort(reverse=True)
    
    LlenarArreglo(A,elementos, 0, 10)
    B = A[:] #Funcion splice
    C = A[:] #Funcion splice
    Tiempos_Quick_Sort = []
    Tiempos_Quick_Sort_Random = []
    Tiempos_Heap_Sort = []  
    for i in range(4):
        #print("Desordenado", A)
        medirQuicks(QuickSort, A, 0, len(A)-1, Tiempos_Quick_Sort)
        #print("Ordenado", A)

        #print("Desordenado", B)
        medirQuicks(RandQuickSort, B, 0, len(B)-1, Tiempos_Quick_Sort_Random)
        #print("Ordenado", B)

        #print("Desordenado", C)
        medirHeap(HeapSort, C, Tiempos_Heap_Sort)
        #print("Ordenado", C)
    
    TQSG.append(TimepoPromedio(Tiempos_Quick_Sort, "Quick Sort", A))
    TQSRG.append(TimepoPromedio(Tiempos_Quick_Sort_Random, "Quick Sort Random",B))
    THSG.append(TimepoPromedio(Tiempos_Heap_Sort, "Heap Sort", C))   

def main():
    ejecucion(500)
    ejecucion(1000)
    ejecucion(5000)
    ejecucion(10000)
    ejecucion(20000)
    graficas(TQSG, TQSRG, THSG, valores_X)
    
TQSG = []
TQSRG = []
THSG = []
valores_X = [500, 1000, 5000, 10000, 20000]
main()


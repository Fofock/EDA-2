import time 
import random
import sys
import matplotlib.pyplot as plt
sys.setrecursionlimit(1_000_000)

def BusquedaLineal(A, key):
    for k in range(len(A)):
        if A[k] == key:
            return k
    return -1 
        
#SOLO FUNCIONA BUSQUEDA BINARIA SI EL ARREGLO ESTA ORDENADO , PODEMOS ORDENANDO USANDO ALGUNA DE LAS TECNICAS QUE HEMOS VISTO O USANDO .SORT
def BusquedaBinaria(A, key):
    inicio = 0
    fin = len(A) - 1
    while(inicio <= fin):
        mitad = (inicio + fin ) // 2 ##Redondea hacia abajo 
        if key == A[mitad]:
            return mitad
        elif key < A[mitad]:
            fin = mitad - 1
        else:
            #ESTO POR LO MISMO DE QUE ESTA ORDENADA, SI LA LLAVE NO ES MENOR PUES ENTONCES NO EXISTE Y NOS PROCEDERA A RETORNAR -1
            inicio = mitad + 1
    return -1
#CON EL NONE PODEMOS LLAMARA ESTA FUNCIÓN SOLAMENTE PASANDOLE DOS PARAMETROS EN  LUGAR DE CUATRO, LOS ULTIMOS DOS SON OPCIONALES 
def BusquedaBinariaRecursiva(A, key, inicio = None, fin = None):
    if inicio is None and fin is None:
        inicio = 0 
        fin = len(A)-1
    
    if inicio > fin:
        return -1
    mitad = (inicio + fin)//2
    if key == A[mitad]:
        return mitad 
    elif key < A[mitad]:
        return BusquedaBinariaRecursiva(A, key, inicio, mitad-1)
    else:
        return BusquedaBinariaRecursiva(A, key, mitad+1, fin)

def BusquedaLinealCentinela(A,key):
    n = len(A)
    last = A[n-1]
    A[n-1] = key
    i = 0
    while i < n and A[i] != key: #AQUI ESTA DE MAS LA VERIFICACION DE TAMAÑO DEL WHILE, YA QUE COMO ASIGNAMOS EL VALOR DE LA KEY AL FINAL, EL BUCLE SIEMPRE ACABARÁ
        i += 1
    A[n-1] == last
    if i < n-1 or last == key:
        return i
    return -1

def LlenarArreglo(arreglo,n,LimiteI, LimiteS):
    for i in range(n):
        arreglo.append(random.randint(LimiteI, LimiteS)) 

def TimepoPromedio(arrTiempos, algoritmo, elemetos):
    n = len(elemetos)
    t = (sum(arrTiempos) / 3)
    print(f"El tiempo promedio del algoritmo de busqueda {algoritmo} para encontar la llave en un arreglo de {n} elementos es {t} segundos" )
    return t    

def medirBusquedasLienal(fn, A, arrTiempos, k):
    Ti = time.perf_counter()
    fn(A, k)
    Tf = time.perf_counter()
    Tt = Tf - Ti
    #print(f"El algoritmo tardo {Tt} segundos en ordenar la lista" )
    arrTiempos.append(Tt)

def medirBusquedasBinarias(fn, A, arrTiempos, k):
    B = sorted(A)
    Ti = time.perf_counter()
    fn(B, k)
    Tf = time.perf_counter()
    Tt = Tf - Ti
    #print(f"El algoritmo tardo {Tt} segundos en ordenar la lista" )
    arrTiempos.append(Tt)

def ejecucion(elementos):       
    A = []   
    LlenarArreglo(A,elementos, 0, elementos//2)
    k = random.randint(0, elementos//2 )
    print(f"El valor de la llave es: {k}")
    
    Tiempos_BusquedaLineal = []
    Tiempos_BusquedaLinealCentinela = [] 
    Tiempos_BusquedaBinariaRecursiva = []
    for i in range(4):
        medirBusquedasLienal(BusquedaLineal, A, Tiempos_BusquedaLineal, k)
        
        medirBusquedasLienal(BusquedaLinealCentinela, A, Tiempos_BusquedaLinealCentinela, k)

        medirBusquedasBinarias(BusquedaBinariaRecursiva, A,Tiempos_BusquedaBinariaRecursiva, k)
    
    TBLG.append(TimepoPromedio(Tiempos_BusquedaLineal, "Busqueda Lineal", A))
    TBLCG.append(TimepoPromedio(Tiempos_BusquedaLinealCentinela, "Busqueda Lineal Centinela",A))
    TBBRG.append(TimepoPromedio(Tiempos_BusquedaBinariaRecursiva, "Busqueda Binaria Recursiva", A)) 
    
def graficas(TBLG, TBLCG, TBBRG, elementos):
    # Graficar los tiempos de ejecución 
    plt.plot(elementos, TBLG, label="Busqueda Lineal", color="red", marker='o')
    
    # Graficar los tiempos de ejecución 
    plt.plot(elementos, TBLCG, label="Busqueda Lineal Centinela", color="blue", marker='x')
    
    # Graficar los tiempos de ejecución 
    plt.plot(elementos, TBBRG, label="Busqueda Binaria Recursiva", color="green", marker='s')
    
    # Configurar la gráfica
    plt.xlabel("Número de elementos")
    plt.ylabel("Tiempo de ejecución (s)")
    plt.title("Comparación de tiempos de ejecución entre algoritmos")
    plt.legend()
    plt.grid(True)
    
    # Mostrar la gráfica
    plt.show()

def main():
    #ejecucion(100)
    #ejecucion(200_000)
    #ejecucion(500_000)
    #ejecucion(1_000_000)
    #valores_X = [200_000, 500_000, 1_000_000]
    #graficas(TBLG, TBLCG, TBBRG, valores_X)
    probarRepetidos()
    probarRepetidosLineal()
    
def encontrarRepetidos(A, key):
    indice = BusquedaBinaria(A, key)
    if indice == -1:
        return None  #NO SE ENCONTRÓ LA LLAVE 
    
    #CONTAR HACIA ATRÁS PARA ENCONTRAR EL ÍNDICE INICIAL
    inicio = indice
    while inicio > 0 and A[inicio - 1] == key:
        inicio -= 1
    
    #CONTAR HACIA ADELANTE PARA ENCONTRAR EL ÍNDICE FINAL
    final = indice
    while final < len(A) - 1 and A[final + 1] == key:
        final += 1
    
    #EL NÚMERO DE REPETICIONES ES LA DIFERENCIA ENTRE LOS ÍNDICES + 1
    repeticiones = final - inicio + 1
    
    return repeticiones, inicio, final

#PARA PROBAR LA FUNCION DE ENCONTRAR REPETIDOS
def probarRepetidos():
    A = sorted([random.randint(0, 10) for _ in range(20)])  #CODIGO PYTHONOSO
    key = random.randint(0, 10)  
    print(f"Arreglo: {A}")
    print(f"Buscando la llave: {key}")
    
    resultado = encontrarRepetidos(A, key)
    
    if resultado is None:
        print("La llave no existe en el arreglo.")
    else:
        repeticiones, inicio, final = resultado
        print(f"Repeticiones: {repeticiones}, Índice inicial: {inicio}, Índice final: {final}")
        
def encontrarRepetidosLineal(A, key):
    inicio = -1
    final = -1
    repeticiones = 0
    
    for i in range(len(A)):
        if A[i] == key:
            if inicio == -1:
                inicio = i  #ENCONTRAMOS LA PRIMERA APARICIÓN
            final = i  #ACTUALIZAMOS EL FINAL CON CADA APARICIÓN
            repeticiones += 1
    
    if inicio == -1:  #SI NO ENCURNTRA LA LLAVE 
        return None
    
    return repeticiones, inicio, final

#FUNCIÓN PARA PROBAR EL ALGORITMO CON BÚSQUEDA LINEAL
def probarRepetidosLineal():
    A = [random.randint(0, 10) for _ in range(20)]  #lISTA PYTHONOSA
    key = random.randint(0, 10)  #LLAVE ALEATORIA 
    print(f"Arreglo: {A}")
    print(f"Buscando la llave: {key}")
    
    resultado = encontrarRepetidosLineal(A, key)
    
    if resultado is None:
        print("La llave no existe en el arreglo.")
    else:
        repeticiones, inicio, final = resultado
        print(f"Repeticiones: {repeticiones}, Índice inicial: {inicio}, Índice final: {final}")

if __name__ == "__main__" :
    # TBLG = []
    # TBLCG = []
    # TBBRG = []
    # main()
    A = [8,5,9,7,3] 
    BusquedaLineal(A, 9)
    print(A)
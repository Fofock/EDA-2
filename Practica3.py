import random 
import time
import math
import matplotlib.pyplot as plt

def CountingSort(A):
    #SE CALCULA EL VALOR MAXIMO DEL ARREGLO
    k = max(A)
    C = []
    B = [] 
    #FORMAMOS EL ARREGLO AUXILIAR C, DE TAMAÑO K EN EL CUAL SE ALMACENARÁ LA FRECUENCIA DE APARICIÓN DE UN VALOR EN EL INDICE CON EL MISMO VALOR, ADEMÁS EN ESTE ARREGLO AUXILIAR INICIALIZAMOS TODOS SUS INDICES EN 0
    for i in range (k+1): #ES K+1 POR QUE RECOREDEMOS QUE EL IN RANGE TOMA HASTA EL VALOR N-1 QUE NOSOTROS LE PASAMOS COMO ARGUMENTO 
        C.append(0)
    
    #CREAMOS B, QUE ES EL ARREGLO EN DONDE SE VAN A COLOCAR LOS ELEMENTOS YA ORDENADOS, DE IGUAL MANERA INICIALIZAMOS TODOS SUS INDICES CON 0
    for i in range (len(A)):
        B.append(0)
    
    #PARA OBTENER EL CONTEO
    for j in range(len(A)):
        #TOMAMOS EL VALOR DEL ELEMENTO ALMACENADO EN EL ARREGLO A EN EL INDICE J, ESE VALOR NOS LLEVARA AL INDICE QUE LE CORRESPONDE EN EL ARREGLO C Y CON ESTO SE DETERMINA QUE EL VALOR APARECE EN EL ARREGLO, POR LO QUE LE SUMAMOS UNO AL VALOR QUE SE ENCUENTRA EN ESTE INDICE EN C
        C[A[j]] = C[A[j]] + 1
    
    #SUMA LOS ACUMULADOS 
    for i in range(1,k+1):
        #Empieza en 1 para que no nos de el indie -1 en la primera iteracion
        #SE SUMA EL ANTERIOR CON EL SIGUIENTE 
        C[i] = C[i] + C[i-1]
        #PUEDO COLOCAR VALORES EN B, TOMANDO COMO REFERENCIA EL VALOR QUE CONTIENE ESE INDICE EN C, ES DECIR EL VALOR ME INDICA EN QUE INDICE PUEDO COMENZAR A COLOCAR ELEMETOS CON DE IGUAL VALOR QUE EL INDICE C
        
    for j in range(len(A)-1, -1, -1):
        #SE LE RESTA 1 POR QUE COMO CONTAMOS EL INDICE 0, EL TAMAÑO DEL ARREGLO ES N, PERO TENEMOS N-1 INDICES 
        #VA LEYENDO DE A LOS VALORES, ESOS LOS BUSCA EN EL INDICE C Y DE AHI LOS ORDENA EN B, Y DESPUES DERECEMENTA EL ACOMULADO, EN LA PRIMERA LINEA NO LO DECREMENTA DEFINITIVAMENTE, EN LA SEGUNDA SI
        B[C[A[j]]-1] = A[j]
        C[A[j]] -= 1
    return B

def LlenarArreglo(arreglo,n,LimiteI, LimiteS):
    for i in range(n):
        arreglo.append(random.randint(LimiteI, LimiteS)) #Rango de los numeros
        
def CountigSort_RadixSort(A, b, digito):
    C = []
    B = [] 
#Formamos el arrglo auxiliar que va a almacenar llenandolo de 0
    for i in range (b): #ES DE RANGO 10 POR QUE ESTAMOS USANDO EL SISTEMA DECIMAL
        C.append(0)
    
    for i in range (len(A)):
        B.append(0)

    #Para obtener el CONTEO
    for j in range(len(A)):
        #Tomamos el valor de A en el indice j y con eso vamos a ese indice dentro del arreglo, y como este numero corresponde a cierto indice en C, incrementamos el valor del arreglo C que contiene el contenido de ese valor 
        cifra = ObtenDigito(A[j], digito)
        C[cifra] = C[cifra] + 1
    
    #PARA OBTENER EL ACUMULADO
    for i in range(1, b):
        #Empieza en 1 para que no nos de el indie -1 en la primera iteracion
        C[i] = C[i] + C[i-1]
    
    #PARA ORDENAR EN B 
    for j in range(len(A)-1, -1, -1):
        cifra = ObtenDigito(A[j], digito)
        B[C[cifra]-1] = A[j]
        C[cifra] -= 1

    for j in range(len(A)):
        A[j] = B[j]
    
    return A

def RadixSort(A):
    k = max(A)
    d = math.floor(math.log10(k)) + 1 #D ES LA CANTIDAD DE DIGITOS DEL NUMERO 
    for i in range(d):
        CountigSort_RadixSort(A, 10, i)
    return A
    
def ObtenDigito(num, i):
    return  (num//10 ** i) % 10

def medirSorts(fn, A, arrTiempos):
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

def ejecucion(elementos):       
    A = []   
    
    #Mejor de los casos
    #x = 10 
    
    #Peor de los casos 
    x = elementos * 1000
    
    #Caso Promedio
    #x = elementos
    
    LlenarArreglo(A,elementos, 0, x)
    k = max(A)
    print(f"El valor de k es: {k}")
    
    B = A[:] #Funcion splice
    Tiempos_CountingSort = []
    Tiempos_RandixSort = [] 
    for i in range(4):
        #print("Desordenado", A)
        medirSorts(CountingSort, A, Tiempos_CountingSort)
        #print("Ordenado por Counting Sort", A)

        #print("Desordenado", B)
        medirSorts(RadixSort, B,Tiempos_RandixSort)
        #print("Ordenado por Radix Sort", B)
    
    TCSG.append(TimepoPromedio(Tiempos_CountingSort, "Counting Sort", A))
    TRSG.append(TimepoPromedio(Tiempos_RandixSort, "Randix Sort",B))  
    
def TimepoPromedio(arrTiempos, algoritmo, elemetos):
    n = len(elemetos)
    t = (sum(arrTiempos) / 3)
    print(f"El tiempo promedio del algoritmo {algoritmo} para {n} elementos es {t} segundos" )
    return t    

def graficas(TCSG, TRSG, elementos):
    # Graficar los tiempos de ejecución 
    plt.plot(elementos, TCSG, label="Countig Sort", color="red", marker='o')
    
    # Graficar los tiempos de ejecución 
    plt.plot(elementos, TRSG, label="Radix Sort", color="blue", marker='x')
    
    # Configurar la gráfica
    plt.xlabel("Número de elementos")
    plt.ylabel("Tiempo de ejecución (s)")
    plt.title("Comparación de tiempos de ejecución entre algoritmos")
    plt.legend()
    plt.grid(True)
    
    # Mostrar la gráfica
    plt.show()

def CountigSort_RadixSort_Cadenas(A, b, digito):
    C = []
    B = [] 
    for i in range (b): 
        C.append(0)
    
    for i in range (len(A)):
        B.append(0)
        
    for j in range(len(A)):

        cifra = ord(ObtenerCaracter(A[j], digito)) #Convertimos el valor a ASCII con el ord
        C[cifra] = C[cifra] + 1
        
    for i in range(1, b):
        C[i] = C[i] + C[i-1]
        
    for j in range(len(A)-1, -1, -1):
        cifra = ord(ObtenerCaracter(A[j], digito))
        B[C[cifra]-1] = A[j]
        C[cifra] -= 1

    for j in range(len(A)):
        A[j] = B[j]
    
    return A    

def RadixSort_Cadenas(A):
    k = max(len(s) for s in A) #ENCUENTRA LA CADENA DE TEXTO MAS GRANDE DENTRO DEL ARREGLO DE CADENAS 
    for i in range(k-1, -1, -1): 
        CountigSort_RadixSort_Cadenas(A, 256, i)    
    return A

def ObtenerCaracter(cadena, i):
    if i < len(cadena):
        return cadena[i] #Retorna el caracter en la posiscion i de la cadena, recordar que si bien arriba le pasamos un indice y pdoriasmos pensar que le estamos pasando un solo valor no es asi, le pasamos una cadena, ya que en ese indice tenemos alojada toda una cadena y no solo un caracter
    else:
        return ' ' 
        
def main():
    ejecucion(5000)
    ejecucion(10000)
    ejecucion(20000)
    valores_X = [5000, 10000, 20000]
    graficas(TCSG, TRSG, valores_X)

#EJECUTAR SOLO LAS ACCIONES QUE "ESTAN AL AIRE" DE ESTE MODULO, Y NO DE LAS IMPORTACIONES
if __name__ == "__main__":
    TCSG = []
    TRSG = []
    main()
    """W = ["Paquito","Jonathan","Diego","Adolfo","José","Sandra","Camila","Sofia","Iván","Alejandro"]
    print(">>>> Radix Sort Lexicografico <<<<\n")
    print(f"Arreglo Desordenado: \n{W}\n")
    A = RadixSort_Cadenas(W)
    print(f"Arreglo Ordenado: \n{A}\n") """


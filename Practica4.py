def BusquedaLineal(A, x):
    for k in range(len(A)):
        if A[k] == x:
            return k
    return -1 
        
#SOLO FUNCIONA BUSQUEDA BINARIA SI EL ARREGLO ESTA ORDENADO , PODEMOS ORDENANDO USANDO ALGUNA DE LAS TECNICAS QUE HEMOS VISTO O USANDO .SORT
def BusquedaBinaria(A, key):
    inicio = 0
    fin = len(A) - 1
    while(inicio <= fin):
        mitad = (inicio + fin )
        if key == A[mitad]:
            return mitad
        elif key < A[mitad]:
            fin = mitad - 1
        else: 
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
        return BusquedaBinaria(A, key, inicio, mitad-1)
    else:
        return BusquedaBinaria(A, key, inicio, mitad+1)
        
arr = ['b', 'c', 'e', 'z']
arr2 = arr[:]
key = 'c'
indice = BusquedaLineal(arr, key)
print(f"la llave {key} esta en indice {indice}")

arr2 = arr[:]
indice = BusquedaBinaria(arr2, key)
print(f"la llave {key} esta en indice {indice}")

indice = BusquedaBinaria(arr2, key)
print(f"la llave {key} esta en indice {indice}")


import random
from Database_12K import Usuario
import time

#FUNCIÓN PREHASHING 
def ConvertirLlave(key):
    keyNum = 0
    i = 1
    for char in key:
        keyNum += ord(char) * i #SUMA LOS VALORES DE CADA CARACTER DE LA LLAVE 
        i += 1
    return keyNum
"""
def FormarTabla(m):
    T = [None] * m
    return T
    
#FUNCIÓN HASH METODO DIVISÓN
def ha(key, m):
    hashkey = ConvertirLlave(key)
    return hashkey % m

#INSERTAR USANDO HASH DIVISIÓN Y MANEJO DE COLISIONES OPEN ADRESSING
def InsertarLinearProbing(T, m, key, valor):
    j = 0
    h = ha(key, m)
    while j < m:
        indice = (h+j) % m
        par = (key, valor) #EL VALOR ES 
        if T[indice] is None:
            T[indice] = par 
            return indice
        else:
            j = j+1 #LINEAR PROBING PARA EL MANEJO DE COLISIONES, SI NO ESTA VACIO PASA AL SIGUIENTE INDICE 
    return -1 #SI ESTA LLENO EL ARREGLO DA UN ERROR 

def Buscar(T, key, m):
    j = 0
    h = ha(key, m)
    while j < m:
        indice = (h+j) % m
        if T[indice] is not None:
            if T[indice][0] == key:
                return T[indice][1]
        else:
            j += 1
    return -1

def llenarTabla(T, m, longK):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    randKey = ''.join(random.choice(caracteres) for _ in range(longK))
    randVal = random.randint(0, 15)
    Insertar(T, len(T), randKey, randVal)
    valor = Buscar(T,randKey, len(T))
    print(valor)
"""
def VerificarPrimo(n):
    #SI EL NUMERO ES PRIMO DEVUELVE UN TRUE, SI NO LO ES DEVUELVE FALSE
    if n <= 1:
        return False
    if n <= 3: #COMO 2 Y 3 SON PRIMOS DE AHÍ ESTA CONDICIÓN
        return True
    if n % 2 == 0 or n % 3 == 0:#LOS NUMEROS PRIMOS SOLO PUEDEN SER DIVIDIDOS ENTRE UNO Y SI MISMOS POR ESO SI EL NUMERO SE PUEDE DIVIDIR ENTRE TRES O DOS DE FORMA EXACTA, NO ES PRIMO
        return False
    i = 5 #COMO EL SIGUIENTE NUMERO PRIMO ES 5 VERIFICA CON EL
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: #COMO EL SIGUIENTE NUMERO ES 7 VERIFICA CON EL 
            return False
        i += 6 #EL SIGUIENTE NUMERO ES 11 POR ESO EL +6, Y ESTA FORMULA SE CUMPLE PARA TODOS LOS DEMÁS NUMEROS PRIMOS 
    return True

def PrimosEnRango(inicio, fin):
    #GENERA UNA LISTA DE NUMEROS PRIMOS QUE ESTAN EN ESA LISTA
    primos = []
    for num in range(inicio, fin + 1):#RANGO DE LOS NUMEROS ENTEROS 
        if VerificarPrimo(num):#VERIFICAMOS SI CADA NUMERO DENTRO DE ESE RANGO ES PRIMO
            primos.append(num)#SI ES PRIMO SI AGREGA EL NUMERO AL ARREGLO
    return primos #NOS REGRESA EL ARREGLO DE NUMEROS PRIMOS 

def RandPrimo(start, end):
    #ELEGIMOS UN NUMERO PRIMO DE LA LISTA QUE SE GENERO PREVIAMENTE
    primes = PrimosEnRango(start, end)#ARREGLO DE PRIMOS EN EL RANGO
    if not primes:
        raise ValueError("No se encontraron números primos en el rango dado.")
    return random.choice(primes)#CHOICE NOS PERMITE SELECCIONAR UN VALOR ALEATORIO DE UN ARREGLO

#FUNCIÓN HASH UNIVERSAL
def HashUniversal(key, m, a, b, p):
    hashkey = ConvertirLlave(key)
    return (((a*hashkey)+b)%p)% m

###CLASE PARA EL MANEJO DE COLISONES CON CHAINING
class HashTable:
    #METODO CONSTRUCTOR DEL OBJETO HASHTABLE 
    def __init__(self, size): 
        self.size = size
        self.table = [[] for _ in range(size)]  #CREA UNA LISTA CON UNA LISTA EN CADA INDICE DE FORMA PYTHONOSA
        self.p = RandPrimo(self.size, 2*(self.size))
        self.a = random.randint(1, self.p - 1) #A NO PUEDE SER 0 PARA QUE NO NOS DE PROBLEMAS CON LA OPERACIÓN MATEMATICA
        self.b = random.randint(0, self.p - 1) #B SI PUEDE SER 0 PERO
        
    def hash_function(self, key):
        #HACEMOS USO DE LA FUNCIÓN HASH UNIVERSAL QUE PREVIAMENTE HABIAMOS CREADO
        return HashUniversal(key,self.size, self.a, self.b, self.p) 

    def insert(self, key, value):
        index = self.hash_function(key)
        bucket = self.table[index] #HAY QUE TENER EN CUENTA QUE BUCKET ES UN ARREGLO TAMBIEN
        # Buscar si la clave ya está en el bucket
        for pair in bucket:
            if pair[0] == key:
                # Si la clave existe, añade el nuevo valor a la lista de valores
                pair[1].append(value)
                return
        # Si la clave no está en el bucket, añade un nuevo par con una lista de valores
        bucket.append((key, [value]))  # Aquí se almacena el nuevo par clave-valor

    def search(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]
        for pair in bucket:
            if pair[0] == key:
                return pair[1]  # Retorna la lista de valores
        return None  # Retorna None si la clave no se encuentra

def Login(tablaHash, username, password):
    resultados = tablaHash.search(username)  ### Se usa la función search de la clase HashTable
    print(f"\n########  Login   ########\nUsuario: {username}\nContraseña: {password}\n")
    if not resultados:
        print("Usuario no encontrado.")
    else:
        usuario_encontrado = False
        for usuario in resultados:
            if usuario.password == password:
                print(f"Acceso Autorizado: Bienvenido {usuario.fullname}")
                usuario_encontrado = True
                break
        if not usuario_encontrado:
            print("Acceso Denegado: Contraseña Incorrecta")

# Comparación de tiempos
def busquedaLinealOptimizada(arr, key):
    for usuario in arr:
        if usuario.username == key:
            return usuario
    return None

def puntoDos(tabla, usuarios):
    print('\n###########  Comparación de tiempos  ##############\n')
    usuariosPrueba = random.sample(usuarios, 10)

    tiempos_hash = []
    tiempos_lineal = []

    for usuario in usuariosPrueba:
        username = usuario.username

        #BUSQUEDA EN LA TABLA
        inicio = time.perf_counter()
        tabla.search(username)  ### Uso de la tabla hash para buscar
        fin = time.perf_counter()
        tiempos_hash.append(fin - inicio)

        # Búsqueda lineal
        inicioL= time.perf_counter()
        busquedaLinealOptimizada(usuarios, username)  ### Búsqueda lineal en la lista de usuarios
        finL= time.perf_counter()
        tiempos_lineal.append(finL - inicioL)

        print(f"Tiempo búsqueda en tabla hash para {username}: {fin - inicio} segundos")
        print(f"Tiempo búsqueda lineal para {username}: {finL - inicioL} segundos")

    promedio_hash = sum(tiempos_hash) / len(tiempos_hash)
    promedio_lineal = sum(tiempos_lineal) / len(tiempos_lineal)

    print(f"\nPromedio tiempo búsqueda en Tabla Hash: {promedio_hash:.6f} segundos")
    print(f"Promedio tiempo Búsqueda Lineal: {promedio_lineal:.6f} segundos")

# Ejemplo de uso
if __name__ == "__main__":
    tamaño = 15000
    tabla = HashTable(tamaño) 
    usuarios = Usuario.GetUsuariosDB(12000)  #OBTENEMOS LOS USUARIOS DE LA BASE DE DATOS

    for usuario in usuarios:
        tabla.insert(usuario.username, usuario)  #SE INSERTAN LOS USUARIOS EN LA TABLA

    # Probar la función Login
    Login(tabla, "user10", "pass10")  #CONTRASEÑA CORRECTA
    Login(tabla, "user5000", "wrongpass")  #CONTRASEÑA INCORRECTA
    Login(tabla, "nonexistent", "password")  #USUARIO INEXISTENTE

    #COMPARACIÓN DE TIEMPOS
    puntoDos(tabla, usuarios)  
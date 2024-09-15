import random
import string

def FormarTabla(m):
    T = [None] * m
    return T

#FUNCIÓN PREHASHING
def ConvertirLlave(key):
    keyNum = 0
    i = 1
    for char in key:
        keyNum += ord(char) * i #SUMA LOS VALORES DE CADA CARACTER DE LA LLAVE 
        i += 1
    return keyNum

#FUNCIÓN HASH
def ha(key, m):
    hashkey = ConvertirLlave(key)
    return hashkey % m
    

def Insertar(T, m, key, valor):
    j = 0
    h = ha(key, m)
    while j < m:
        indice = (h+j) % m
        par = (key, valor)
        if T[indice] is None:
            T[indice] = par 
            return indice
        else:
            j = j+1 #LINEAR PROBING, SI NO ESTA VACIO PASA AL SIGUIENTE INDICE 
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
    return -1

def llenarTabla(T, m, longK):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    randKey = ''.join(random.choice(caracteres) for _ in range(longK))
    randVal = random.randint(0, 15)
    Insertar(T, len(T), randKey, randVal)
    valor = Buscar(T,randKey, len(T))
    print(valor)
    
def main():
    Tabla = FormarTabla(11)
    llave = "Pp" #LA LLAVE ES COMO LA CLAVE CON LA QUE ACCEDEMOS A UN VALOR, POR ESO LLAVE 
    Insertar(Tabla, len(Tabla), llave, 500)
    valor = Buscar(Tabla, llave, len(Tabla))
    print(Tabla)
    print(valor)
    llenarTabla(Tabla, len(Tabla, 10))
    
main()
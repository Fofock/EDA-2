import random
import math

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


def RandPrimo(count, start, end):
    #ELEGIMOS UN NUMERO PRIMO DE LA LISTA QUE SE GENERO PREVIAMENTE
    primes = PrimosEnRango(start, end)#ARREGLO DE PRIMOS EN EL RANGO
    if len(primes) < count:#VERIFICA QUE HAYA LOS PRIMOS NECESARIOS PARA LOS QUE LE SOLICITAMOS
        raise ValueError("No hay suficientes números primos en el rango dado.")
    return random.sample(primes, count)#SAMPLE NOS PERMITE SELECCIONAR VARIOS ALEATORIOS SIN REMPLAZO, POR SI QUEREMOS SELECCIONAR MAS DE UN PRIMO

def HashUniversal():
    
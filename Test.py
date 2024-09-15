import math

class HashTable:
    def __init__(self, size):
        """Inicializa la tabla hash con una cierta cantidad de 'buckets' (cubos)."""
        self.size = size
        self.table = [[] for _ in range(size)]  # Crea la tabla con listas vacías para cada bucket

    def _hash_function(self, key):
        """Calcula el hash de una clave dado el tamaño de la tabla usando hash universal."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Inserta un par clave-valor en la tabla hash, permitiendo múltiples valores por clave."""
        index = self._hash_function(key)
        bucket = self.table[index]
        # Buscar si la clave ya está en el bucket
        for pair in bucket:
            if pair[0] == key:
                # Si la clave existe, añade el nuevo valor a la lista de valores
                pair[1].append(value)
                return
        # Si la clave no está en el bucket, añade un nuevo par con una lista de valores
        bucket.append(key, [value])  # ### Aquí se almacena el nuevo par clave-valor

    def search(self, key):
        """Busca los valores asociados a una clave en la tabla hash."""
        index = self._hash_function(key)
        bucket = self.table[index]
        for pair in bucket:
            if pair[0] == key:
                return pair[1]  # Retorna la lista de valores
        return None  # Retorna None si la clave no se encuentra

    def delete(self, key):
        """Elimina todos los pares clave-valor de la tabla hash para una clave dada."""
        index = self._hash_function(key)
        bucket = self.table[index]
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                return True
        return False  # Retorna False si la clave no se encuentra

# Ejemplo de uso
    

"""def HashUniversal(key):
    hashkey = ConvertirLlave(key)
    
    return
#FUNCIÓN PREHASHING
def ConvertirLlave(key):
    keyNum = 0
    i = 1
    for char in key:
        keyNum += ord(char) * i #SUMA LOS VALORES DE CADA CARACTER DE LA LLAVE 
        i += 1
    return keyNum"""


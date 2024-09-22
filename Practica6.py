"Una clase es una plantilla que nos sirve para crear objetos, los cuales son un tipo de dato"
#TODOS LOS OBJETOS TIENEN METODOS YA ESTABLECIDOS POR QUE TODOS LOS OBJETOS HEREDAN DE UNA SUPERCLASE
#EL METODO REPR NOS AYUDA A QUE PODAMOS REGRESAR UNA CADENA CUANDO LLAMAMOS A ESTA FUNCION
#UNA ARISTA SE DEFINE COMO DOS nodoS (ARISTA AB)

class Grafo():
    def __init__(self):
        self.vertices = {} #CREAMOS UN DICCIONARIO PARA ALMACENAR LOS nodoS POR NOMBRE

    def agregarNodo(self, nombre):
        if nombre in self.vertices:
            return print(f"Ya existe un nodo con el nombre {nombre}")
        else:
            nuevo = Nodo(nombre) #SE CREA EL nodo
            self.vertices[nombre] = nuevo #COLOCAMOS EL nodo EN EL INDICE CON EL NOMBRE CON EL QUE SE CREO EL nodo

    #LE PASAMOS EL INDICE DONDE SE ENCUENTRA EL nodo CON ESE NOMBRE
    def agregarArista(self, nombre1, nombre2):
        
        if nombre1 in self.vertices:
            pass
        else:   
            return print(f"Error al agregar arista no existe el nodo {nombre1}")
        if nombre2 in self.vertices:
            pass
        else:   
            return print(f"Error al agregar arista no existe el nodo {nombre2}")
        
        nodo1 = self.vertices[nombre1] 
        nodo2 = self.vertices[nombre2]
        #SE AGREGA EL nodo EN EL ARREGLO DE VECINOS DE CADA nodo
        nodo1.agregarVecino(nodo2) 
        nodo2.agregarVecino(nodo1)     
        
    def Imprimir(self):
        print("##### Lista de Adyacencia del Grafo #####")
        for i in self.vertices:
            Nodo = self.vertices[i]
            NomNodo = Nodo.nombre
            listaAdya = Nodo.vecinos
            print(f"{NomNodo} -> {listaAdya}")
            




class Nodo():
    def __init__(self, nombre):
        self.vecinos = []
        self.nombre = nombre

    def agregarVecino(self,nuevoVecino):
        if nuevoVecino in self.vecinos:
            return print(f"El verice {self.nombre} ya tiene un vecino {nuevoVecino}")
        else:
            self.vecinos.append(nuevoVecino)

    def __repr__(self) -> str:
        s = self.nombre
        return s

grafo = Grafo()
grafo.agregarNodo("A")
grafo.agregarNodo("B")
grafo.agregarNodo("C")
grafo.agregarNodo("D")
grafo.agregarNodo("E")

grafo.agregarArista("A", "X")
grafo.agregarArista("A", "B")
grafo.agregarArista("A", "D")
grafo.agregarArista("A", "C")

grafo.agregarArista("B", "A")
grafo.agregarArista("B", "D")

grafo.agregarArista("C", "D")
grafo.agregarArista("C", "E")
grafo.Imprimir()
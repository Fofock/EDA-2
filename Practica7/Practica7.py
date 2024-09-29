import metro

class Grafo():
    def __init__(self):
        self.vertices = {} #CREAMOS UN DICCIONARIO PARA ALMACENAR LOS nodoS POR NOMBRE
        self.tiempo = 0
    def agregarNodo(self, nombre):
        if nombre in self.vertices:
            #print(f"Ya existe un nodo con el nombre {nombre}")
            return -1
        else:
            nuevo = Nodo(nombre) #SE CREA EL nodo
            self.vertices[nombre] = nuevo #COLOCAMOS EL nodo EN EL INDICE CON EL NOMBRE CON EL QUE SE CREO EL nodo
            
    #LE PASAMOS EL INDICE DONDE SE ENCUENTRA EL nodo CON ESE NOMBRE
    def agregarArista(self, nombre1, nombre2):
        
        if nombre1 in self.vertices:
            pass
        else:   
            #print(f"Error al agregar arista no existe el nodo {nombre1}")
            return -1
        if nombre2 in self.vertices:
            pass
        else:   
            #print(f"Error al agregar arista no existe el nodo {nombre2}")
            return -1
        
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
            
    #### ALGORITMOS PARA RECORRER TODOS LOS NODOS DE UN GRAFO ####
    def BFS(self, nombreS):
        s = self.vertices[nombreS]
        for vertice in self.vertices.values(): #VALUES NO HACE OTRA LISTA, ES UNA REFERENCIA AL ARERGLO ORIGINAL
            vertice.color = "White"
            vertice.d = None
            vertice.p = None
        
        s.color = "Gris"
        s.d = 0
        s.p = None
        Q = []
        Q.append(s)
        while Q: #WHILE PYTHONOSO
            u = Q.pop(0)
            for v in u.vecinos:
                if v.color == "White":
                    v.color = "Gris"
                    v.d = u.d + 1
                    v.p = u
                    Q.append(v)
            u.color = "Negro"
            
    def DFS_VISITAR(self, u):
        self.tiempo += 1
        u.d = self.tiempo
        u.color = "Gris"
        for v in u.vecinos:#REVISA LA LISTA DE VECINOS DE EL VERTICE U
            if v.color == "White":
                v.p = u
                self.DFS_VISITAR(v)#PASA A RALIZAR EL MISMO PROCEDIMIENTO CON EL PRIMER VECINO REGISTRADO EN LA LISAT DE ADYACENCIA DEL VERTICE U
        u.color = "Negro" #COLOCA EL ESTADO EN VISITADO
        self.tiempo += 1
        u.f = self.tiempo #CON ESTA PROPIEDAD PODREMOS CONOCER EL TIEMPO TOTAL QUE SE DEMORÓ EN RECORRER EL VERICE, ES DECIR TODAS SUS CONEXIONES EN EL GRAFO
    
    def DFS(self,nombreS):
        for vertice in self.vertices.values(): #VALUES NO HACE OTRA LISTA, ES UNA REFERENCIA AL ARERGLO ORIGINAL
            vertice.color = "White"
            vertice.p = None
            
        s = self.vertices[nombreS]
        self.DFS_VISITAR(s)
        """for vertice in self.vertices.values():
            if vertice.color == "White":
                self.DFS_VISITAR(vertice)"""
        
    def EncontrarCaminoBFS(self, inicial, final):
        self.BFS(inicial) #COMO CONSECUENCIA DEL BFS OBTENEMOS LA RUTA MAS CORTO DE UN NODO A OTRO NODO, SIN EMBARGO ESTA NO ES LA FINALIDAD DE ESTE ALGORITMO, RECORDEMOS QUE ESTE ES UN ALGORITMO DISEÑADO PARA RECORRER TODOS LOS VERTICES DE UN GRAFO.
        nodoFinal = self.vertices[final]
        actual = nodoFinal
        ruta = []
        while actual != None:
            nodo = actual.nombre
            ruta.append(nodo)
            actual = actual.p
        print("\t\t\t\t\t### Ruta BFS ###")
        print(f"<No. Estaciones: {len(ruta)}>")
        for nodo in range(len(ruta)-1, -1, -1):
            print(f"{ruta[nodo]} ", end="-> " * (nodo > 0)) #NO COLOCAR LA FLECHA EN EL ULTIMO ELEMENTO
            
    def EncontrarCaminoDFS(self, inicial, final):
        self.DFS(inicial)
        nodoFinal = self.vertices[final]
        actual = nodoFinal
        ruta = []
        while actual != None:
            nodo = actual.nombre
            ruta.append(nodo)
            actual = actual.p
        print("\t\t\t\t\t### Ruta DFS ###")
        print(f"<No. Estaciones: {len(ruta)}>")
        for nodo in range(len(ruta)-1, -1, -1):
            print(f"{ruta[nodo]} ", end="-> " * (nodo > 0)) #NO COLOCAR LA FLECHA EN EL ULTIMO ELEMENTO
            
class Nodo():
    def __init__(self, nombre):
        self.vecinos = [] #ALMACENA OBJETOS
        self.nombre = nombre
        self.color = None
        self.d = None
        self.p = None
        self.f = None
        
        
    def agregarVecino(self,nuevoVecino):
        if nuevoVecino in self.vecinos:
            return print(f"Ya existe el vecino {nuevoVecino} en el vertice {self.nombre}")
        else:
            self.vecinos.append(nuevoVecino)

    def __repr__(self) -> str:
        s = self.nombre
        return s

def AgregarEstaciones(grafo):
    for i in metro.lineas:
        linea = i
        for j in linea:
            grafo.agregarNodo(j)
            
def UnirLineaEstaciones(grafo):
    for i in metro.lineas:
        linea = i
        for j in range(len(linea) - 1):
            grafo.agregarArista(linea[j], linea[j+1])
            
def CaminosEstaciones(grafo):
    print("\n\n>Ruta de Aquiles Serdán a Iztapalapa")
    grafo.EncontrarCaminoBFS("Aquiles Serdán", "Iztapalapa")
    grafo.EncontrarCaminoDFS("Aquiles Serdán", "Iztapalapa")
    print("\n\n>Ruta de San Antonio a Aragón")
    grafo.EncontrarCaminoBFS("San Antonio", "Aragón")
    grafo.EncontrarCaminoDFS("San Antonio", "Aragón")
    print("\n\n>Ruta de Vallejo a Insurgentes")
    grafo.EncontrarCaminoBFS("Vallejo", "Insurgentes")
    grafo.EncontrarCaminoDFS("Vallejo", "Insurgentes")
            
grafo = Grafo()
AgregarEstaciones(grafo)
UnirLineaEstaciones(grafo)
CaminosEstaciones(grafo)
    
"""
if __name__ == "__main__":
    grafo = Grafo()
    grafo.agregarNodo("0")
    grafo.agregarNodo("1")
    grafo.agregarNodo("2")
    grafo.agregarNodo("3")
    grafo.agregarNodo("4")
    grafo.agregarNodo("5")
    grafo.agregarNodo("6")
    grafo.agregarNodo("7")


    grafo.agregarArista("1", "8")
    grafo.agregarArista("1", "2")
    grafo.agregarArista("1", "0")
    grafo.agregarArista("1", "0")

    grafo.agregarArista("2", "0")
    grafo.agregarArista("2", "3")

    grafo.agregarArista("3", "4")
    grafo.agregarArista("3", "0")

    grafo.agregarArista("4", "5")
    grafo.agregarArista("4", "6")

    grafo.agregarArista("5", "6")

    grafo.Imprimir()
    grafo.EncontrarCaminoBFS("2", "5")
    grafo.EncontrarCaminoDFS("2", "5") """
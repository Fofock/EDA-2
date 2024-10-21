
class ArbolBB(): #ARBOL BINARIO DE BUSQUEDA
    def __init__(self):
        self.root = None
    
    def Insertar(self, k):
        self.__InsertarRecursivo__(k, self.root)
        
    def __InsertarRecursivo__(self,k,nodo):
        if self.root is None:
            self.root = Nodo(k) #SI EL ARBOL ESTA VACIO INS
        else:
            if k < nodo.valor:
                if nodo.izq is None:
                    nodo.izq = Nodo(k)
                else:
                    self.__InsertarRecursivo__(k, nodo.izq)
                    
            elif k > nodo.valor:
                if nodo.der is None:
                    nodo.der = Nodo(k)
                else:
                    self.__InsertarRecursivo__(k, nodo.der)
                    
            else: 
                print("No se permite insertar valores repetidos")
    
    def Buscar(self, k):
        return self.__BuscarRecursivo__(k, self.root)
    
    def __BuscarRecursivo__(self, k, nodo) -> bool:
        if nodo is not None:
            if k == nodo.valor:
                return True
            elif k < nodo.valor:
                return self.__BuscarRecursivo__(k, nodo.izq) #COMO ES UN CONDICIONAL DEBEMOS DE DARLE RETURN PARA QUE SE CUMPLA LA RECURSIVIDAD 
            elif k > nodo.valor:
                return self.__BuscarRecursivo__(k, nodo.der)
        else:
            return False
    
    def Max(self):
        return self.__MaxRecursivo__(self.root)
        
    def __MaxRecursivo__(self, nodo):
        if nodo.der is not None:
            return self.__MaxRecursivo__(nodo.der)
        return nodo.valor
    
    def Min(self):
        return self.__MinRecursivo__(self.root)
    
    def __MinRecursivo__(self, nodo):
        if nodo.izq is not None:
            return self.__MinRecursivo__(nodo.izq)
        return nodo.valor
    
    def Imprimir(self):
        print("###         InOrder        ###")
        self.InOrder(self.root)
        print("\n###         PreOrder        ###")
        self.PreOrder(self.root)
        print("\n###         PostOrder        ###")
        self.PostOrder(self.root)
        print("\n###         Anchura        ###")
        self.Anchura()
        print()

    def InOrder(self, nodo):
        if nodo is not None:
            self.InOrder(nodo.izq)
            print(nodo.valor, end=", ")
            self.InOrder(nodo.der)
    
    def InO
    
    def PreOrder(self, nodo):
        if nodo is not None:
            print(nodo.valor, end=", ")
            self.PreOrder(nodo.izq)
            self.PreOrder(nodo.der)
            
    def PostOrder(self, nodo):
        if nodo is not None:
            self.PostOrder(nodo.izq)
            self.PostOrder(nodo.der)
            print(nodo.valor, end=", ")
        
    def Anchura(self):
        cola = []
        if self.root is not None:
            cola.append(self.root)
        else: 
            print("El Arbol Binario de Busqueda esta vacio")
        while cola:
            nodo = cola.pop(0)
            print(nodo.valor, end=", ")
            if nodo.izq:
                cola.append(nodo.izq)
            if nodo.der:
                cola.append(nodo.der)
    
    def AchuraPretty(self):
        arrNodos = []
        nodo = self.root
        if nodo is not None:
            self.InOrderPretty(nodo.izq)
            print(nodo.valor, end=", ")
            arrNodos.append(nodo.valor)
            self.InOrder(nodo.der)
        
        numNodos = len(arrNodos)
        
        cola = []
        aux = [[] for _ in range(numNodos+1)]
        if self.root is not None:
            cola.append(self.root)
            aux[0].append(self.root)
        else: 
            print("El Arbol Binario de Busqueda esta vacio")
        while cola:
            i = 1
            nodo = cola.pop(0)
            if nodo.izq:
                cola.append(nodo.izq)
                aux[i].append(nodo.izq)
            if nodo.der:
                cola.append(nodo.der)
                aux[i].append(nodo.izq)
            i += 1
        print(aux)    
        
        
    def Limpiar(self):
        self.root = None
        
    def Eliminar(self, k):
        self.root = self.__EliminarRecursivo__(k, self.root)

    def __EliminarRecursivo__(self, k, nodo):
        if nodo is None:
            return nodo  # El nodo no existe, no hay nada que eliminar

        # Encontrar el nodo a eliminar
        if k < nodo.valor:
            nodo.izq = self.__EliminarRecursivo__(k, nodo.izq)
        elif k > nodo.valor:
            nodo.der = self.__EliminarRecursivo__(k, nodo.der)
        else:
            # Nodo encontrado
            # Caso 1: Nodo con un solo hijo o sin hijos
            if nodo.izq is None:
                return nodo.der  # Si no hay hijo izquierdo, devuelve el hijo derecho
            elif nodo.der is None:
                return nodo.izq  # Si no hay hijo derecho, devuelve el hijo izquierdo

            # Caso 2: Nodo con dos hijos
            # Encuentra el nodo más pequeño en el subárbol derecho
            temp = self.__MinRecursivo__(nodo.der)
            nodo.valor = temp  # Reemplaza el valor del nodo a eliminar
            nodo.der = self.__EliminarRecursivo__(temp, nodo.der)  # Elimina el nodo más pequeño

        return nodo
    
    def PrintPretty(self):
        if not self.root:
            print("El Arbol Binario de Busqueda está vacío")
            return

        niveles = []
        self.Anchura

        # Determinar la altura del árbol
        altura = len(niveles)
        espaciado = 2 ** (altura)  # Espacio inicial entre nodos

        for i, nivel in enumerate(niveles):
            linea = ""
            for j, nodo in enumerate(nivel):
                if nodo is None:
                    linea += " " * espaciado + " "  # Espacio para nodos ausentes
                else:
                    linea += str(nodo.valor).center(espaciado)
            print(linea)

            # Imprimir diagonales
            if i < altura - 1:  # Si no es el último nivel
                diagonal_linea = ""
                for j, nodo in enumerate(nivel):
                    if j % 2 == 0:  # Para evitar saltos innecesarios
                        diagonal_linea += " " * (espaciado // 2 - 1)  # Espacio inicial
                        if nodo and nodo.izq:
                            diagonal_linea += "/"
                        else:
                            diagonal_linea += " "
                        diagonal_linea += " " * (espaciado - 1)  # Espacio entre nodos
                        if nodo and nodo.der:
                            diagonal_linea += "\\"
                        else:
                            diagonal_linea += " "
                    else:
                        diagonal_linea += " " * espaciado  # Espacio para nodos ausentes
                print(diagonal_linea)

            espaciado //= 2  # Reducir espacio para el siguiente nivel



class Nodo():
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.padre = None

if __name__ == "__main__":
    arbolBB = ArbolBB()
    arbolBB.Insertar(8)
    arbolBB.Insertar(3)
    arbolBB.Insertar(10)
    arbolBB.Insertar(1)
    arbolBB.Insertar(6)
    arbolBB.Insertar(14)
    arbolBB.Insertar(4)
    arbolBB.Insertar(7)
    arbolBB.Insertar(13)
    arbolBB.Imprimir()
    arbolBB.Insertar(14)
    arbolBB.Insertar(1)
    print(arbolBB.Max())
    print(arbolBB.Min())
    print("Existe el valor 4: ", arbolBB.Buscar(4))
    print("Existe el valor 8: ", arbolBB.Buscar(8))
    print("Existe el valor 13: ", arbolBB.Buscar(13))
    print("Existe el valor 2: ", arbolBB.Buscar(2))
    print("Existe el valor 15: ", arbolBB.Buscar(15))
    arbolBB.Eliminar(7)
    arbolBB.Imprimir()
    arbolBB.Eliminar(10)
    arbolBB.Imprimir()
    arbolBB.Eliminar(6)
    arbolBB.Imprimir()
    arbolBB.Eliminar(3)
    arbolBB.Imprimir()
    arbolBB.Eliminar(3)
    arbolBB.Imprimir()
    arbolBB.Eliminar(8)
    arbolBB.Imprimir()
    arbolBB.Insertar(100)
    arbolBB.Imprimir()
    arbolBB.AchuraPretty()

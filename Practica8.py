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
        self.PrintPretty()

    def InOrder(self, nodo):
        if nodo is not None:
            self.InOrder(nodo.izq)
            print(nodo.valor, end=", ")
            self.InOrder(nodo.der)
                
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
    
    def PrintPretty(self):
        niveles = self.AnchuraPretty()
        if not niveles:
            return

        altura = len(niveles) - 1
        espaciado_inicial = 2 ** altura  # ESPACIADO INICIAL BASADO EN LA ALTURA DEL ÁRBOL

        for i, nivel in enumerate(niveles):
            linea_nodos = " " * espaciado_inicial
            separador = " " * (2 ** (altura - i + 1))  # ESPACIADO DECRECIENTE PARA CADA NIVEL

            for nodo in nivel:
                if nodo is None:
                    linea_nodos += " " * 3  # ESPACIO PARA NODOS VACÍOS
                else:
                    linea_nodos += f"{str(nodo):^3}" + separador

            print(linea_nodos.rstrip())

            # IMPRIMIR CONEXIONES DIAGONALES
            if i < altura:
                linea_conexiones = " " * (espaciado_inicial // 2)
                for j, nodo in enumerate(nivel):
                    if nodo is not None:
                        if j % 2 == 0:  # NODO IZQUIERDO
                            linea_conexiones += " /" + " " * (len(separador) - 2)
                        else:  # NODO DERECHO
                            linea_conexiones += "\\" + " " * (len(separador) - 1)
                    else:
                        linea_conexiones += " " * len(separador)
                print(linea_conexiones.rstrip())

            espaciado_inicial //= 2  # REDUCIR ESPACIADO PARA EL SIGUIENTE NIVEL

    def AnchuraPretty(self):
        if not self.root:
            return []
        
        niveles = []
        cola = [self.root]

        while cola:
            nivel = []
            for _ in range(len(cola)):
                nodo = cola.pop(0)
                if nodo:
                    nivel.append(nodo.valor)
                    cola.append(nodo.izq)
                    cola.append(nodo.der)
                else:
                    nivel.append(None)
                    cola.append(None)
                    cola.append(None)
            niveles.append(nivel)
            if all(n is None for n in cola):
                break 
        return niveles
        
    def Limpiar(self):
        self.root = None
        
    def Eliminar(self, k):
        self.root = self.__EliminarRecursivo__(k, self.root)

    def __EliminarRecursivo__(self, k, nodo):
        if nodo is None:
            return nodo  #EL NODO NO EXISTE, NO HACEMOS NADA

        #BUSCAR EL NODO A ELIMINAR
        if k < nodo.valor:
            nodo.izq = self.__EliminarRecursivo__(k, nodo.izq)
        elif k > nodo.valor:
            nodo.der = self.__EliminarRecursivo__(k, nodo.der)
        else:

            #NODO SIN HIJOS O CON UN SOLO HIJO 
            if nodo.izq is None:
                return nodo.der  # SI NO HAY HIJO IZQUIERDO, DEVUELVE EL HIJO DERECHO
            elif nodo.der is None:
                return nodo.izq  # SI NO HAY HIJO DERECHO, DEVUELVE EL HIJO IZQUIERDO

            #NODO CON DOS HIJOS
            #ENCUENTRA EL NODO MÁS PEQUEÑO EN EL SUBÁRBOL DERECHO
            temp = self.__MinRecursivo__(nodo.der)
            nodo.valor = temp  #REEMPLAZA EL VALOR DEL NODO A ELIMINAR
            nodo.der = self.__EliminarRecursivo__(temp, nodo.der)  #ELIMINA EL NODO MÁS PEQUEÑO

        return nodo
    

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
    print("El valor maximo es: ", arbolBB.Max())
    print("El valor minimo es: ", arbolBB.Min())
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

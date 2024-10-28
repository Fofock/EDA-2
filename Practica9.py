class Nodo:
    #HACEMOS UNSA SUGERENCIA SOBVRE EL TIPO DE DATO QUE ES t
    def __init__(self, t: int) -> None :
        self.hoja = True
        self.numLlaves = 0 #NUMERO DE LLAVES 
        self.hijos = [None for _ in range(2*t +1)] #CANTIDAD DE NODOS HIJOS QUE PUEDE TENER EL NODO
        self.llaves = [None for _ in range(2*t)] #CANTIDAD DE LLAVES QUE PUEDE ALOJAR UN NODO, CONCIDERAR QUE NO PONEMOS -1 POR QUE EL FOR YA LO HACE 
        
class ArbolB:
    
    def __init__(self, t: int):
        self.t = t
        self.raiz = Nodo(t) #ROOT
        
    def Insertar(self, k):
        r = self.raiz
        if r.numLlaves == 2*self.t -1:
            s = Nodo(self.t) # CREA OTRO NODO QUE AHORA SERÁ LA RAÍZ 
            self.raiz = s
            s.hoja = False
            s.hijos[1] = r # COLOCAMOS A R COMO PRIMER HIJO DE S
            self.SplitChild(s,1)
            self.InsertNonFull(s, k)
        else:
            self.InsertNonFull(r, k)
            
    def SplitChild(self, x, i):
        z = Nodo(self.t) # CREAMOS OTRO NODO 
        y = x.hijos[i] # Y ES EL HIJO DEL NODO PADRE A DIVIDIR EN EL UBICADO EN EL INDICE I
        z.hoja = y.hoja # LE PASAMOS EL VALOR BOOLEANO QUE SI ES HOJA
        z.numLlaves = self.t - 1 # INICIALIZAMOS EL NUMERO MINIMO DE LLAVES PERMITIDO
        
        for j in range(1, self.t): #EMPEZAMOS EN 1 POR CORMEN 
            z.llaves[j] = y.llaves[j + self.t]
            #SE COPIAN LAS LLAVES DE LA MITAD SUPERIOR  (SIN EL ELEMENTO DE LA MITAD "MEDIANA")DEL NODO Y AL NODO Z 
            y.llaves[j + self.t] = None
        
        if not y.hoja: #SI Y NO ES UNA HOJA
            for j in range(1,self.t + 1):#HASTA  SELF.T + 1 POR QUE SON LOS HIJOS CON LOS QUE CUENTA AHORA Y
                # SE COPIAN LOS NODOS HIJOS DE LA MITAD SUPERIOR DE Y A Z (LA MITAD SUPERIOR DE Y)
                z.hijos[j] = y.hijos[j + self.t] 
                y.hijos[j + self.t] = None # UNA VEZ COPIADOS LOS HIJOS, LOS DE Y SE HACEN NONE
        y.numLlaves = self.t - 1
        # SE DESPLAZAN LOS HIJOS DE X PARA HACER ESPACIO AL NUEVO NODO HIJO Z, EMPEZAMOS DESDE EL FINAL PARA NO SOBREESCRIBIR
        for j in range(x.numLlaves + 1, i, -1):
            x.hijos[j+1] = x.hijos[j]
        
        #SE INSERTA EL NUEVO NODO HIJO Z
        x.hijos[i+1] = z
        
        #SE DESPLAZAN LAS LLAVES EN X PARA HACER ESPACIO PARA LA NUEVA LLAVE, EMPEZAMOS DESDE EL FINAL PARA NO SOBREESCRIBIR LLAVES 
        for j in range(x.numLlaves, i-1, -1):
            x.llaves[j+1] = x.llaves[j]
        
            
        x.llaves[i] = y.llaves[self.t] #INSERTAMOS LA NUEVA LLAVE EN X (ES LA ULTIMA LLAVE DE Y POR QUE RECOREDMOS QUE ESTA ANTES ERA LA MEDIA)
        y.llaves[self.t] = None #ELIMINAMOS LA LLAVE QUE INSERTAMOS EN X DE Y
        x.numLlaves += 1 #INCREMENTAMOS LA CANTIDAD DE LLAVES QUE TIENE EL NODO X
        
        
    def InsertNonFull(self, x, k):
        i = x.numLlaves
        if x.hoja: #SI X ES HOJA
            #RECORREMOS TODOS LOS ELEMENOS PARA HACER ESPACIO PARA EL ELEMENTO A INSERTAR 
            while i >= 1 and (x.llaves[i] is None or k < x.llaves[i]):
                x.llaves[i+1] = x.llaves[i]
                i -= 1
            x.llaves[i+1] = k
            x.numLlaves += 1
        else: #SI X NO ES HOJA
            #RECORREMOS HASTA ENCONTRAR EL LUGAR DONDE PODEMOS INSERTAR K
            #COMO LA LISTA DE LLAVES SE LLENA CON NONES, POR ESO PONEMOS ESA SEGUNDA CONDICIÓN, PARA QUE NO NOS ARROJE UNA EXCEPCIÓN
            while i >= 1 and (x.llaves[i] is None or k < x.llaves[i]):
                i -= 1
            i += 1 #PARA NO INSERTAR EN EL INDICE 0
            
            # VEMOS SI EL NODO HIJO DONDE PUEDE IR K ESTA LLENO
            if x.hijos[i] is not None and x.hijos[i].numLlaves == 2 * self.t - 1:
                self.SplitChild(x, i)
                # DETERMINAMOS EN QUE HIJO PODEMOS INSERTAR A K
                if x.llaves[i] is not None and k > x.llaves[i]:
                    i += 1
            #LE PASAMOS EL VALOR DETERMINADO A LA FUCIÓN       
            self.InsertNonFull(x.hijos[i], k)

    def Buscar(self, x, k) -> bool:
        # LA PRIMERA VEZ X ES LA RAÍZ
        i = 1
        # BUSCA EN LAS LLAVES DE X, Y USAMOS EL NUMLLAVES PARA QUE EL BUCLE TENGA UN FIN SI ES QUE NO ENCOTRAMOS EL ELEMENTO 
        while i <= x.numLlaves and (x.llaves[i] is None or k > x.llaves[i]):
            i += 1
            
        if i <= x.numLlaves and k == x.llaves[i]:
            return True
        #SI EL VALOR NO ES ENCONTRADO Y EL NODO ES HOJA, ESTE NO SE ENCUENTRA EN EL ARBOL 
        elif x.hoja:
            return False
        #SI NO ES HOJA PUEDE QUE ESTE EN EL ARBOL EN ALGUNO DE LOS HIJOS, POR ESO LLAMAMOS RECURSIVAMENTE 
        #LE PASAMOS RECURSIVAMENTE AL HIJO I DE X, QUE ES DONDE PODRIA ESTAR EL VALOR DE K
        else: 
            return self.Buscar(x.hijos[i], k)
        
    def ImprimirPreOrder(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz

        # Imprime las llaves del nodo actual con la indentación correspondiente
        print(" " * (4 *nivel) + "|" + "-" * (4 * nivel) + "{" + ", ".join(str(llave) for llave in nodo.llaves if llave is not None) + "}")

        # Llama recursivamente a los hijos
        if not nodo.hoja:
            for hijo in nodo.hijos:
                if hijo is not None:
                    self.ImprimirPreOrder(hijo, nivel + 1)

    def ImprimirInOrder(self, nodo=None, resultado=None):
        if nodo is None:
            nodo = self.raiz
        if resultado is None:
            resultado = []

        # Recorre cada llave en el nodo actual en in-order, comenzando desde el índice 1
        for i in range(1, nodo.numLlaves + 1):
            # Llama recursivamente al hijo izquierdo de la llave actual, si existe
            if nodo.hijos[i] is not None:
                self.ImprimirInOrder(nodo.hijos[i], resultado)

            # Agrega la llave actual al resultado
            resultado.append(str(nodo.llaves[i]))

        # Recorre el último hijo, que está después de la última llave
        if nodo.hijos[nodo.numLlaves + 1] is not None:
            self.ImprimirInOrder(nodo.hijos[nodo.numLlaves + 1], resultado)

        # Imprime el resultado en un solo renglón cuando se procesa la raíz
        if nodo == self.raiz:
            print(", ".join(resultado))

    def PrintPretty(self, nodo=None, espacio=0, separador=" "):
        if nodo is None:
            nodo = self.raiz

        # Espacio de separación entre niveles del árbol
        espacio += 10

        # Recorre de derecha a izquierda para el orden gráfico, omitiendo índice 0
        if not nodo.hoja and nodo.hijos[nodo.numLlaves + 1] is not None:
            self.PrintPretty(nodo.hijos[nodo.numLlaves + 1], espacio)

        # Muestra el nodo actual con el espaciado correspondiente, omitiendo None
        print()
        print(separador * espacio, end="")
        print(", ".join(str(llave) for llave in nodo.llaves[1:nodo.numLlaves + 1] if llave is not None))

        # Recorre el resto de los hijos en preorden, empezando desde el índice 1
        for i in range(1, nodo.numLlaves + 1):
            if not nodo.hoja and nodo.hijos[i] is not None:
                self.PrintPretty(nodo.hijos[i], espacio)


    
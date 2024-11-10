
class ListaOrdenada():
    def __init__(self) -> None:
        self.lista = []
    
    def Insertar(self,valor: int):
        nuevoNodo = Nodo()
        nuevoNodo.valor = valor
        
        if not self.lista: # LA LISTA LIGADA ORDENADA ESTA VACIA
            self.lista.append(nuevoNodo)
            
        elif self.lista[0].valor >= valor: #EL VALOR VA AL INICIO DE LA LISTA LIGADA ORDENADA
            nuevoNodo.hijo = self.lista[0]
            self.lista[0].padre = nuevoNodo
            self.lista.insert(0, nuevoNodo)
            
        else: #EL VALOR NO VA AL INICIO, SE BUSCA SU LUGAR
            for i in range(1, len(self.lista)):
                if self.lista[i].valor >= valor:
                        nuevoNodo.hijo = self.lista[i] # COMO EL VALOR DE ESTE ES MÁS GRADE, SERÁ SU HIJO
                        self.lista[i-1].hijo = nuevoNodo # HACEMOS QUE EL NODO ANTERIOR SEA EL PADRE DE ESTE NODO VOLVIENDO A UNIR TODA LA LISTA
                        self.lista.insert(i, nuevoNodo) # INSERTAMOS EL NODO EN LA LISTA
                        break
            else: #SI EL VALOR ES EL MÁS GRANDE
                self.lista.append(nuevoNodo)
    
    def Longitud(self):
        tamañoLista = len(self.lista)
        return tamañoLista
    
    def Quitar(self):
        valorMax = self.lista.pop()
        return valorMax.valor
    
    def __str__(self):  
        elementos = ""
        for nodo in self.lista:
            elementos += f"{nodo.valor}\n"
        if elementos == "":
            return "Lista vacia..."
        else:
            return elementos
    
class ListaPalabras:
    def __init__(self, cadena):
        # El constructor inicializa la lista con una palabra
        if not cadena or cadena == "":
            raise ValueError("La lista debe iniciarse con una palabra no vacía.")
        self.cabeza = Nodo()
        self.cabeza.cadena = cadena
        # Primer nodo con la palabra proporcionada
        self.cola = self.cabeza # ESTO POR SER EL PRIMER NODO

    def Insertar(self, cadena):
        if not cadena or cadena == "":
            print("Error: No se puede insertar una cadena vacía.")
            return
        if self.buscar(cadena):
            print("Error: La palabra ya está en la lista.")
            return
        
        # Crear el nuevo nodo
        nuevo_nodo = Nodo()
        nuevo_nodo.cadena = cadena
        
        
        # Insertamos el nodo al final de la lista
        self.cola.hijo = nuevo_nodo
        self.cola = nuevo_nodo  # Ahora el tail es el nuevo nodo

    def pop(self):
        if self.cabeza is None:
            return ""
        
        # Si la lista solo tiene un elemento
        if self.cabeza == self.cola:
            cadena = self.cabeza.cadena
            self.cabeza = None
            self.cola = None
            return cadena
        
        # Si hay más de un elemento, vamos hasta el penúltimo
        actual = self.cabeza
        while actual.hijo != self.cola:
            actual = actual.hijo
        
        cadena = self.cola.cadena
        self.cola = actual  # Ahora el penúltimo nodo es el tail
        self.cola.hijo = None  # Desconectamos el último nodo
        return cadena

    def buscar(self, cadena):
        actual = self.cabeza
        while actual is not None:
            if actual.valor == cadena:
                return True
            actual = actual.hijo
        return False

    def __str__(self):
        # Construir la cadena con los valores
        elementos = []
        actual = self.cabeza
        while actual is not None:
            elementos.append(actual.cadena)
            actual = actual.hijo
        return ", ".join(elementos)
        

class Nodo():
    def __init__(self) -> None:
        self.valor = None
        self.cadena = None
        self.hijo = None
        

        
if __name__ == "__main__":
    print("******Lista Ordenada******\n")
    listaLigada = ListaOrdenada()
    print(f"Longitud: {listaLigada.Longitud()}")
    print(listaLigada.__str__())
    listaLigada.Insertar(5)
    listaLigada.Insertar(10)
    listaLigada.Insertar(3)
    listaLigada.Insertar(1)
    listaLigada.Insertar(20)
    listaLigada.Insertar(7)
    listaLigada.Insertar(100)
    listaLigada.Insertar(2)
    print(f"Longitud: {listaLigada.Longitud()}")
    print(listaLigada.__str__())
    print()
    print("******Lista Palabra******")
    listaPal = ListaPalabras("Hola")  
    print(listaPal)  
    listaPal.Insertar("Mundo")
    listaPal.Insertar("Ingenieria")
    listaPal.Insertar("EDA")
    listaPal.Insertar("2")
    print(listaPal.__str__())  
    print(listaPal.buscar("Mundo"))  
    print(listaPal.buscar("UNAM"))  
    print(listaPal.pop())
    print(listaPal.pop())
    print(listaPal.pop())
    print(listaPal.__str__())

    
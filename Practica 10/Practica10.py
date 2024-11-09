import os
from pathlib import Path

# FUNCION ENCARGADA DE LEER Y CARGAR LOS DATOS EN MEMORIA PRIMARIA 
def cargarArchivo():
    directoroPadre = Path(__file__).parent # NOS DEVULVE EL DIRECTORIO PADRE DONDE ESTA CONTENIDO EL ARCHIVO ACTUAL 
    rutaCPs = directoroPadre / "CPdescarga.txt"
    
    # HAREMOS UN TRY-EXCEPT PARA MANEJAR LAS EXCEPCIONES 
    try:
        # CON WITH NOS ASEGURAMOS DE QUE EL ARCHIVO SE CIERRE AUNQUE OCURRA UNA EXCEPXION
        with open(rutaCPs,"r") as archivoCPs: # ABRIMOS EL ARCHIVO CON AYUDA DE LA RUTA GENERADA
            lineas = archivoCPs.readlines() # ARREGLO QUE ALMACENA CADA LINEA EN UN INDICE
            codigosPostalesDiccionario = {} # CREAMOS UN DICCIONARIO PARA ACCEDER EN TIEMPO CONSTANTE, LO USAREMOS COMO SI FUESE UNA TABLAS HASH
            
            for linea in lineas:
                linea = linea.strip().split('|')
                codigoPostal = linea[0] # CODIGO POSTAL
                colonia = linea[1] # COLONIA 
                estado = linea[4] # ESTADO
                municipio = linea[3] # MUNICIPIO
                # VERIFICAMOS QUE EL CODIGO POSTAL YA EXISTE EN EL DICCIONARIO
                if codigoPostal in codigosPostalesDiccionario:
                    # AGREGAMOS UN NUEVO DICCIONARIO EN OTRO INDICE DE LA LISTA QUE SE CREO PREVIAMENTE, ESTE NUEVO DICCIOANRIO NO TENDRÁ UN NOMBRE EN ESPECIFICO
                    codigosPostalesDiccionario[codigoPostal].append({
                        "colonia": colonia,
                        "municipio": municipio,
                        "estado": estado
                    })
                else:
                    # CREAMOS UNA LISTA DENTRO DE LA CLAVE "codigoPostal" Y AÑADIMOS OTRO DICCIONARIO DENTRO DE ESTA
                    codigosPostalesDiccionario[codigoPostal] = [{
                        "colonia": colonia,
                        "municipio": municipio,
                        "estado": estado
                    }]
                # EL DICCIOANRIO TIENE CÓDIGOS POSTALES COMO CLAVES Y LISTAS DE DICCIOANRIOS COMO VALORES
        return codigosPostalesDiccionario
        
    except FileNotFoundError:
        # EL ARCHIVO NO SE ENCONTRÓ
        print("El archivo no fue encontrado, favor de revisar que exista el archivo.")
    except Exception:
        # MANEJA CAULQUIER OTRO TIPO DE EXCEPCIÓN
        print("Error desconocido, favor de contactar a soport tecnico.")

def ObtenerCP():
    
    pass
    


if __name__ == "__main__":
    #nombreCompleto = input("Ingresa tu nombre completo: ")  
    #CP = input("Ingresa tu código postal: ")
    diccionarioCPs = cargarArchivo()
    print(diccionarioCPs)
    
    
    
    
import os
from pathlib import Path

# FUNCION ENCARGADA DE LEER Y CARGAR LOS DATOS EN MEMORIA PRIMARIA 
def cargarArchivo(CP, nombreCompleto):
    directoroPadre = Path(__file__).parent # NOS DEVULVE EL DIRECTORIO PADRE DONDE ESTA CONTENIDO EL ARCHIVO ACTUAL 
    rutaCPs = directoroPadre / "CPdescarga.txt"
    
    # HAREMOS UN TRY-EXCEPT PARA MANEJAR LAS EXCEPCIONES 
    try:
        # CON WITH NOS ASEGURAMOS DE QUE EL ARCHIVO SE CIERRE AUNQUE OCURRA UNA EXCEPXION
        with open(rutaCPs,"r") as archivoCPs: # ABRIMOS EL ARCHIVO CON AYUDA DE LA RUTA GENERADA
            lineas = archivoCPs.readlines() # ARREGLO QUE ALMACENA CADA LINEA EN UN INDICE
            codigosPostalesDiccionario = {} # CREAMOS UN DICCIONARIO PARA ACCEDER EN TIEMPO CONSTANTE, LO USAREMOS COMO SI FUESE UNA TABLAS HASH
            
            # EMPEZAMOS EN LA LINEA DOS, DONDE EMPIEZAN LOS DATOS
            for linea in lineas[2:]:
                linea = linea.strip().split('|')
                codigoPostal = linea[0] # CODIGO POSTAL
                colonia = linea[1] # COLONIA 
                estado = linea[4] # ESTADO
                municipio = linea[3] # MUNICIPIO
                ciudad  =  linea[5]
                # VERIFICAMOS QUE EL CODIGO POSTAL YA EXISTE EN EL DICCIONARIO
                if codigoPostal in codigosPostalesDiccionario:
                    # AGREGAMOS UN NUEVO DICCIONARIO EN OTRO INDICE DE LA LISTA QUE SE CREO PREVIAMENTE, ESTE NUEVO DICCIOANRIO NO TENDRÁ UN NOMBRE EN ESPECIFICO
                    codigosPostalesDiccionario[codigoPostal].append({
                        "colonia": colonia,
                        "municipio": municipio,
                        "estado": estado,
                        "ciudad": ciudad
                    })
                else:
                    # CREAMOS UNA LISTA DENTRO DE LA CLAVE "codigoPostal" Y AÑADIMOS OTRO DICCIONARIO DENTRO DE ESTA
                    codigosPostalesDiccionario[codigoPostal] = [{
                        "colonia": colonia,
                        "municipio": municipio,
                        "estado": estado,
                        "ciudad": ciudad
                    }]
                # EL DICCIOANRIO TIENE CÓDIGOS POSTALES COMO CLAVES Y LISTAS DE DICCIOANRIOS COMO VALORES
        busacarCp(codigosPostalesDiccionario, CP, nombreCompleto)
        
    except FileNotFoundError:
        # EL ARCHIVO NO SE ENCONTRÓ
        print("El archivo no fue encontrado, favor de revisar que exista el archivo.")
        return
    except Exception:
        # MANEJA CAULQUIER OTRO TIPO DE EXCEPCIÓN
        print("Error desconocido, favor de contactar a soport tecnico.")
        return

def busacarCp(diccionarioCPs, CP, nombreCompleto):
    num = 0
    if CP in diccionarioCPs:
        if len(diccionarioCPs[CP]) > 1:
            print("Se encontraron varias colonias con el mismo código postal.")
            print("Inserte el numero de la opción que corresponda a su colonia: ")
            i = 0
            for _ in diccionarioCPs[CP]: # MUESTRA LA LISTA DE COLONIAS
                print(f"{i+1}.- {diccionarioCPs[CP][i]['colonia']}")
                i += 1
            num = input("Opción: ")
            num = int(num) # CASTEO PARA PODER MANEJARLO COMO INT
            # SI SE INGRESA UN VALOR MAYOR O MENOR DA UN ERROR
            if num > len(diccionarioCPs[CP]) or num < 1:
                print("Opción no válida. Por favor, elige un número dentro del rango.")
                return 
            print(f"-> Colonia: {diccionarioCPs[CP][num-1]['colonia']}")
            print(f"-> Estado: {diccionarioCPs[CP][num-1]['estado']}")
            print(f"-> Municipio: {diccionarioCPs[CP][num-1]['municipio']}")
            print(f"-> Ciudad: {diccionarioCPs[CP][num-1]['ciudad']}")
        else: 
            print(f"-> Colonia: {diccionarioCPs[CP][0]['colonia']}")
            print(f"-> Estado: {diccionarioCPs[CP][0]['estado']}")
            print(f"-> Municipio: {diccionarioCPs[CP][0]['municipio']}")
            print(f"-> Ciudad: {diccionarioCPs[CP][0]['ciudad']}")
        guardarInfo(diccionarioCPs, CP, num, nombreCompleto)
    else: 
        print("El Codigo Postal ingresado no existe...")

def guardarInfo(diccionarioCPs, CP, num, nombreCompleto):
    carpetaNom = f"./{CP}"
    if not os.path.exists(carpetaNom):
        os.makedirs(carpetaNom, exist_ok=True)
    archivo = Path(carpetaNom) / f"{nombreCompleto}.eda2"
    # ESCRIBIMOS LA INFORMACIÓN EN EL ARCHIVO CREADO
    with open(archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(f"Nombre: {nombreCompleto}\n")
        archivo.write(f"-> Colonia: {diccionarioCPs[CP][num-1]['colonia']}\n")
        archivo.write(f"-> Estado: {diccionarioCPs[CP][num-1]['estado']}\n")
        archivo.write(f"-> Municipio: {diccionarioCPs[CP][num-1]['municipio']}\n")
        archivo.write(f"-> Ciudad: {diccionarioCPs[CP][num-1]['ciudad']}\n")
    
if __name__ == "__main__":
    nombreCompleto = input("Ingresa tu nombre completo: ")  
    CP = input("Ingresa tu código postal: ")
    cargarArchivo(CP, nombreCompleto)
    

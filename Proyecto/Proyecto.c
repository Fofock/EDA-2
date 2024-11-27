#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb-master/stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb-master/stb_image_write.h"

void splitChannels();

int main(int argc, char *argv[])
{

    // AQUI COMO SOLO LE ESTAMOS PASANDO EL NOMBRE DEL PROGRAMA A EJECUTAR Y NO LE ESTAMOS DANDO NINGUN OTRO PARAMENTRO, EL VALOR QUE TENDRIA ARGC SERIA 1
    if (argc < 2) 
    {
        printf("ERROR: Faltan argumentos para la ejecucion\n\n");
        return -1;
    }
    // EL ARGUMENTO 0 DE UN PROGRAMA ES EL PROPIO NOMBRE DEL EJECUTABLE, POR ESO NOS VAMOS AL INDICE UNO DE ARGV
    char *Img = &argv[1]; 

    
    
    splitChannels(Img);
    return 0;
}

void splitChannels(char *Img)
{
    // OBTENERMOS EL VALOR QUE ALOGA A DONDE APUNTA IMG
    char *srcPath = *Img; 

    int width, height, channels;
    //EL APUNTADOR *SCRIMA APUNTA AUN ARREGLO DE TAMAÑO WIDTH*HEIGHT*CHANNELS DE LOS CANALES QUE TIENE LA IMAGEN
    unsigned char *srcIma = stbi_load(srcPath, &width, &height, &channels, 0);

    if (srcIma == NULL)
    {
        printf("No se pudo cargar la imagen %s :(\n\n\n", srcPath);
        return;
    }
    else
    {
        printf("\nImagen cargada correctamente: %dx%d pixeles con %d canales.\n", width, height, channels);
    }

    if (channels != 3)
    {
        printf("\nERROR: La imágen debe ser de 3 canales.\n", width, height, channels);
        return;
    }

    int imaSize = width * height;

    // SE MULTIPLICA POR EL VALOR DE CHANELS POR QUE AUNQUE SOLO VAMOS A TOMAR EN CUENTA EN CADA UNO DE LOS ARREGLOS EL VALOR CORRESPONDIENTE A CADA COLOR EN CADA PIXEL , CADA PIXEL TRIENE 3 VALORES ES DECIR 3 BYTES Y DOS DE ESTOS LOS ESTABLECEREMOS EN 0 
    unsigned char *imaBlue = malloc(imaSize * channels); 
    unsigned char *imaRed = malloc(imaSize * channels);
    unsigned char *imaGreen = malloc(imaSize * channels);

    for (int i = 0; i < imaSize; i++)
    {
        // CHARS ENTEROS SIN SIGNO 
        unsigned char r = srcIma[i * channels + 0];
        unsigned char g = srcIma[i * channels + 1];
        unsigned char b = srcIma[i * channels + 2];

        imaRed[i * channels + 0] = r;
        imaRed[i * channels + 1] = 0;
        imaRed[i * channels + 2] = 0;

        imaGreen[i * channels + 0] = 0;
        imaGreen[i * channels + 1] = g;
        imaGreen[i * channels + 2] = 0;

        imaBlue[i * channels + 0] = 0;
        imaBlue[i * channels + 1] = 0;
        imaBlue[i * channels + 2] = b;
    }

    // CON EL ARREGLO IMARED YA PODEMOS OBTENER EL HISTOGRAMA APOYANDONOS DEL ALGORITMO COUNTING SORT
    CountingSort(imaRed, width, height);
    // DESPUES DEL COUNTING SORT IMARED (EL ARREGLO), YA ESTA ECUALIZADO



    // Saving image
    stbi_write_jpg("imaBlue.jpg", width, height, 3, imaBlue, 100);
    stbi_write_jpg("imaRed.jpg", width, height, 3, imaRed, 100);
    stbi_write_jpg("imaGreen.jpg", width, height, 3, imaGreen, 100);

    // Liberar la memoria de la imágen
    stbi_image_free(imaBlue);  // free memory
    stbi_image_free(imaRed);   // free memory
    stbi_image_free(imaGreen); // free memory
}


// A LA FUNCION LE PASAMOS EL ARREGLO, RECORDANDO QUE EN C LOS ARREGLOS SIEMPRE SE PASAN POR REFERENCA, ES DECIR EL PUNTERO QUE APUNTA A ESTOS 
void CountingSort(unsigned char A[], int width, int height) {
    // n ES EL TAMAÑO DE A
    // BUSQUEDA DEL MAXIMO, EN ESTE CASO NO ES NECESARIO POR QUE NUESTRSO ARREGLOS SIEMPRE SERAN DE TAMAÑO 256 POR QUE SON LOS VALORES QUE PUEDEN TOMAR LOS ELEMENTOS RGB DE NUESTROS PIXELES

    /* int k = A[0];
    for (int i = 1; i < n; i++) {
        if (A[i] > k) {
            k = A[i];
        }
    }*/

    int arrTam = 255;
    // NO ES NECESARIO UN CATEO POR QUE EN C PODEMOS ASIGNAR PUNTEROS DE TIPO VOID A UN PUNTERO DE TIPO UNSIGNED CHAR SIN NECESIDAD DE UN CASTEO EXPLICITO
    // USAMOS CALLOC PARA INICALIZAR EN 0 LOS ARREGLOS SIN LA NECESIDAD DE TENER QUE HACER UN FOR
    unsigned char *C = calloc(arrTam, sizeof(unsigned char));
    unsigned char *B = calloc(arrTam * sizeof(unsigned char));

    // CONTAMOS LA FRECUENCIA DE CADA VALOR DE A (HISTOGRAMA)
    for (int j = 0; j <= arrTam; j++) {
        C[A[j]] = C[A[j]] + 1;
    }
        GuardarHistograma(C);
    // CALCULAMOS LA FUNCION DE DISTRIBUCION ACUMULADA
    for (int i = 1; i <= arrTam; i++) {
        C[i] = C[i] + C[i - 1];
    }
        // YA CN LA FUNCION DE DISTRIBUCION ACUMULADA ECUALIZAMOS Y GUARDAMOS LOS VALORES
        Ecualizacion(C, width, height);
        GuardarHistograma(C);

    // COLOCAMOS EN B LOS NUEVOS VALORES DEL HISTOGRAMA YA EUCALIZADO
    for (int j = arrTam; j >= 0; j--) {
        B[C[A[j]] - 1] = A[j];
        C[A[j]] = C[A[j]] - 1;
    }

    // COPIAMOS LOS ELEMENTOS DE B -> A
    for (int i = 0; i <= arrTam; i++) {
        A[i] = B[i];
    }

    // LIBERAMOS LA MEMORIA 
    free(C);
    free(B);
}   


void Ecualizacion(unsigned char C[], int width, int height)
{
    int L = 256;
    for(int i = 0; i < L; i++)
    {
        // HACEMOS LA DIVISON CON DECIMALES ASEGURANDO UN CALCULO PRECISO
        C[i] = (unsigned char)round(((float)((C[i] - C[0]) / ((width * height) - C[0])) * (L-1)));
    }
    return;
}

void GuardarHistograma(unsigned char C[])
{
    // ABRIMOS EL ARCHIVO CON PERMISOS DE ESCRITURA
    FILE *fp = fopen("file.csv", "w+"); // FOPEN SI NO EXISTE EL ARCHIVO LO CREA
    
    if (fp == NULL)
    {
        printf("Error al abrir el archivo.\n");
        return;  // Salir de la función si no se pudo abrir el archivo
    }

    // VERIFICAMOS SI EL ARCHIVO ESTA VACIO
    fseek(fp, 0, SEEK_END);  // MOVEMOS EL PUNTERO AL FINAL DEL ARCHIVO 
    long size = ftell(fp);   // OBTENEMOS EL TAMAÑO DEL ARCHIVO EN BYTES
    if (size == 0) {         // SI EL TAMAÑO ES 0 EL ARCHIVO ESTA VACIO
        // VALORES DEL HISTOGRAMA (índices de 0 a 255)
        for (int i = 0; i < 256; i++) {
            fprintf(fp, "%d\n\t", i); 
        }
    }
    
    // DATOS
    for (int i = 0; i < 256; i++)
        fprintf(fp, "%hhu\n", C[i]);
    
    // CERRAMOS EL ARCHIVO 
    fclose(fp); 
    return;
}
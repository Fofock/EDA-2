#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb-master/stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb-master/stb_image_write.h"

void splitChannels();
void CountingSort(unsigned char A[], int width, int height, int channels);
void Ecualizacion(int C[], int width, int height);
void GuardarHistograma(int C[], int B[]);

int main(int argc, char *argv[])
{

    // AQUI COMO SOLO LE ESTAMOS PASANDO EL NOMBRE DEL PROGRAMA A EJECUTAR Y NO LE ESTAMOS DANDO NINGUN OTRO PARAMENTRO, EL VALOR QUE TENDRIA ARGC SERIA 1
    if (argc < 2) 
    {
        printf("ERROR: Faltan argumentos para la ejecucion\n\n");
        return -1;
    }
    // EL ARGUMENTO 0 DE UN PROGRAMA ES EL PROPIO NOMBRE DEL EJECUTABLE, POR ESO NOS VAMOS AL INDICE UNO DE ARGV
    char *Img = argv[1]; 
    splitChannels(Img);
    return 0;
}

void splitChannels(char *Img)
{
    // OBTENERMOS EL VALOR QUE ALOGA A DONDE APUNTA IMG
    char *srcPath = Img; 

    int width, height, channels;
    //EL APUNTADOR *SCRIMA APUNTA AUN ARREGLO DE TAMAÑO WIDTH*HEIGHT*CHANNELS DE LOS CANALES QUE TIENE LA IMAGEN
    unsigned char *srcIma = stbi_load(srcPath, &width, &height, &channels, 0);

    if (srcIma == NULL)
    {
        printf("No se pudo cargar la imagen %s :(\n\n\n", srcPath);
        return;
    }
    else if(channels == 3)
    {
        printf("\nImagen cargada correctamente: %dx%d pixeles con %d canales.\n", width, height, channels);
        int imaSize = width * height;

        // SE MULTIPLICA POR EL VALOR DE CHANELS POR QUE AUNQUE SOLO VAMOS A TOMAR EN CUENTA EN CADA UNO DE LOS ARREGLOS EL VALOR CORRESPONDIENTE A CADA COLOR EN CADA PIXEL , CADA PIXEL TIENE 3 VALORES ES DECIR 3 BYTES Y DOS DE ESTOS LOS ESTABLECEREMOS EN 0 
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
        CountingSort(imaRed, width, height, channels);
        // DESPUES DEL COUNTING SORT IMARED (EL ARREGLO), YA ESTA ECUALIZADO


        // Saving image
        stbi_write_jpg("imaBlue.jpg", width, height, 3, imaBlue, 100);
        stbi_write_jpg("imaRed.jpg", width, height, 3, imaRed, 100);
        stbi_write_jpg("imaGreen.jpg", width, height, 3, imaGreen, 100);

        // Liberar la memoria de la imágen
        stbi_image_free(imaBlue);  // free memory
        stbi_image_free(imaRed);   // free memory
        stbi_image_free(imaGreen); // free memory
        return;
    }
    else if (channels == 1)
    {
        printf("\nImagen cargada correctamente: %dx%d pixeles con %d canales.\n", width, height, channels);

        // CON EL ARREGLO IMARED YA PODEMOS OBTENER EL HISTOGRAMA APOYANDONOS DEL ALGORITMO COUNTING SORT
        CountingSort(srcIma, width, height, channels);
        // DESPUES DEL COUNTING SORT IMARED (EL ARREGLO), YA ESTA ECUALIZADO
        // Saving image
        stbi_write_jpg("eqIma.jpg", width, height, 1, srcIma, 100);

        // Liberar la memoria de la imágen
        stbi_image_free(srcIma);  // free memory
    }
    else{
        printf("\nERROR: La imagen debe de ser de 1 0 3 canales.");
    }


}

// A LA FUNCION LE PASAMOS EL ARREGLO, RECORDANDO QUE EN C LOS ARREGLOS SIEMPRE SE PASAN POR REFERENCA, ES DECIR EL PUNTERO QUE APUNTA A ESTOS 
void CountingSort(unsigned char A[], int width, int height, int channels) {
    // BUSQUEDA DEL MAXIMO, EN ESTE CASO NO ES NECESARIO POR QUE NUESTRSO ARREGLOS SIEMPRE SERAN DE TAMAÑO 256 POR QUE SON LOS VALORES QUE PUEDEN TOMAR LOS ELEMENTOS RGB DE NUESTROS PIXELES
    int arrTam = 256;
    // NO ES NECESARIO UN CATEO POR QUE EN C PODEMOS ASIGNAR PUNTEROS DE TIPO VOID A UN PUNTERO DE TIPO UNSIGNED CHAR SIN NECESIDAD DE UN CASTEO EXPLICITO
    // USAMOS CALLOC PARA INICALIZAR EN 0 LOS ARREGLOS SIN LA NECESIDAD DE TENER QUE HACER UN FOR
    int *C = (int*)calloc(arrTam, sizeof(int));
    int *B = (int*)calloc(arrTam, sizeof(int));
    if(channels == 1)
    {
        // CONTAMOS LA FRECUENCIA DE CADA VALOR DE A (HISTOGRAMA)
        for (int j = 0; j <= (width*height); j++) {
            C[A[j]] = C[A[j]] + 1;
        }
        
        for (int j = 0; j <= arrTam; j++) {
            B[j] = C[j]; // IGUALAMOS B Y C PARA QUE NOS AYUDEN CON EL CSV
        }
        // CALCULAMOS LA FUNCION DE DISTRIBUCION ACUMULADA EN C
        for (int i = 1; i <= arrTam+1; i++) {
            C[i] = C[i] + C[i - 1];
        }
        // YA CON LA FUNCION DE DISTRIBUCION ACUMULADA ECUALIZAMOS Y GUARDAMOS LOS VALORES
        //Ecualizacion(C, width, height);
        Ecualizacion(C, width, height);
        GuardarHistograma(B, C);
        // B ES NUESTRO HISTOGRAMA, C ES NUESTRO ECUALIZADO
        /*
        // COLOCAMOS EN B LOS NUEVOS VALORES DEL HISTOGRAMA YA EUCALIZADO 
        for (int j = arrTam; j >= 0; j--) {
            B[C[A[j]] - 1] = (int)A[j];
            C[A[j]] = C[A[j]] - 1;
        }

        // COPIAMOS LOS ELEMENTOS DE B -> A
        for (int i = 0; i <= arrTam; i++) {
            A[i] = (unsigned char)B[i];
        }
        */
        // ACTUALIZAMOS EL ARREGLO A PARA QUE SE ECUALICE 
        for (int i = 0; i < (width*height); i++) {
            A[i] = (unsigned char)C[A[i]];
        }
        // LIBERAMOS LA MEMORIA 
        free(C);
        free(B);
        return;
    }
    else if (channels == 3)
    {   
        // OBTENDREMOS LOS VALORES DEL CANAL ROJO
        // COMO TENEMOS 3 CANALES LOS VALORES ROJOS SON LOS VALORES MULTIPLOS DE 3
        // CONTAMOS LA FRECUENCIA DE CADA VALOR DE A (HISTOGRAMA)
        // EL RANGO ES WIDHT*HEIGHT YA QUE COMO ESTAMOS LLENDO DE 3 EN TRES, ES COMO SI DIVIDIERAMOS EL TAMAÑO DEL ARREGLO ENTRE 3, POR ESTA RAZON NO DEBEMOS MULTIPLICAR EL RANGO POR CHANNELS 
        for (int j = 0; j < (width*height); j++) {
            C[A[j * channels]] += 1;
        }
        //GuardarHistograma(B, C);
        // AQUI B SOLO ES UNA COPIA QUE NOS AYUDA A REPRESNETAR EL CSV, POR ESO NO MULTIPLICAMOS POR CHANNELS
        for (int j = 0; j < arrTam; j++) {
            B[j] = C[j]; // IGUALAMOS B Y C PARA QUE NOS AYUDEN CON EL CSV
        }
        // CALCULAMOS LA FUNCION DE DISTRIBUCION ACUMULADA EN C
        for (int i = 1; i < arrTam; i++) {
            C[i] = C[i] + C[i - 1];
        }
        Ecualizacion(C, width, height);
        GuardarHistograma(B, C);
        // YA CON LA FUNCION DE DISTRIBUCION ACUMULADA ECUALIZAMOS Y GUARDAMOS LOS VALORES
        //Ecualizacion(C, width, height);
        //GuardarHistograma(C, B);
        //B ES NUESTRO HISTOGRAMA, C ES NUESTRO ECUALIZADO

        /*
        // COLOCAMOS EN B LOS NUEVOS VALORES DEL HISTOGRAMA YA EUCALIZADO 
        // NO HAY NECESIDAD DE CASTEO AQUI
        for (int j = (width*height) - 1 ; j >= 0; j--) {
            B[C[A[j * channels]] - 1] = (int)A[j * channels];
            C[A[j * channels]] -= 1;
        }

        // COPIAMOS LOS ELEMENTOS DE B -> A TENEMOS QUE CASTEAR, NO SON EL MISMO TIPO DE DATO
        for (int i = 0; i < (width*height); i++) {
            A[i * channels] = (unsigned char)B[i];
        }
        */
        // ACTUALIZAMOS EL ARREGLO A PARA QUE SE ECUALICE 
        for (int i = 0; i < (width*height); i++) {
            A[i * channels] = (unsigned char)C[A[i*channels]];
        }
        // LIBERAMOS LA MEMORIA 
        free(C);
        free(B);
        return;
    }
    else 
    {
        printf("No es posible ecualizar imagenes con ese numero de canales");
        free(C);
        free(B);
        return;
    }
    
}   

void Ecualizacion(int C[], int width, int height)
{
    int acumMin = C[0];
    int L = 256;
    for(int i = 0; i < L ; i++)
    {
        // HACEMOS LA DIVISON CON DECIMALES ASEGURANDO UN CALCULO PRECISO
        C[i] = (int)round((((double)(C[i] - acumMin)) / ((double)((width * height) - acumMin))) * (L-2))+1;
    }
    return;
} 

void GuardarHistograma(int B[], int C[])
{
    // ABRIMOS EL ARCHIVO CON PERMISOS DE ESCRITURA
    FILE *fp = fopen("file.csv", "w+"); // FOPEN SI NO EXISTE EL ARCHIVO LO CREA
    
    if (fp == NULL)
    {
        printf("Error al abrir el archivo.\n");
        return;  // Salir de la función si no se pudo abrir el archivo
    }
        // VALORES DEL HISTOGRAMA (índices de 0 a 255)
        fprintf(fp, "valor,histo,eqHisto\n");
        for (int i = 0; i < 256; i++) {
            fprintf(fp, "%d,%d,%d", i, B[i],C[i]);
            fprintf(fp, "\n");
        }
    // CERRAMOS EL ARCHIVO 
    fclose(fp); 
    return;
}
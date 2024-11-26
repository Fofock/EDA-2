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

    // Saving image
    stbi_write_jpg("imaBlue.jpg", width, height, 3, imaBlue, 100);
    stbi_write_jpg("imaRed.jpg", width, height, 3, imaRed, 100);
    stbi_write_jpg("imaGreen.jpg", width, height, 3, imaGreen, 100);

    // Liberar la memoria de la imágen
    stbi_image_free(imaBlue);  // free memory
    stbi_image_free(imaRed);   // free memory
    stbi_image_free(imaGreen); // free memory
}
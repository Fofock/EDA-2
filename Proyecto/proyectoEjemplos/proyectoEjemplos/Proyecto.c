#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb-master/stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb-master/stb_image_write.h"

double splitChannels();
double CountingSort(unsigned char A[], int width, int height, int channels);
void Ecualizacion(int C[], int width, int height);
void GuardarHistograma(int C[], int B[], char nombre_Archivo[]);
double splitChannelsParalel(char *Img);
double CountingSortParalel(unsigned char A[], int width, int height, int channels);
void CountingSortImgComplet(unsigned char A[], int width, int height, int channels);
void Resultados(double tiempoSecuencial, double tiempoParalelo);



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
    printf("-------------Resultados en Paralelo-------------\n");
    double timeEjecParalela = splitChannelsParalel(Img);
    printf("Tiempo de ejecucion en Paralelo: %lfs\n",timeEjecParalela);
    
    printf("-------------Resultados en Secuencial-------------\n");
    double timeEjecSecuencial = splitChannels(Img);
    printf("Tiempo de ejecucion en Secuencial: %lfs\n", timeEjecSecuencial);
    Resultados(timeEjecSecuencial, timeEjecParalela);

    return 0;
}



double splitChannels(char *Img)
{
    // OBTENERMOS EL VALOR QUE ALOGA A DONDE APUNTA IMG
    char *srcPath = Img; 

    int width, height, channels;
    //EL APUNTADOR *SCRIMA APUNTA AUN ARREGLO DE TAMAÑO WIDTH*HEIGHT*CHANNELS DE LOS CANALES QUE TIENE LA IMAGEN
    double tCargaImgIn = omp_get_wtime();
    unsigned char *srcIma = stbi_load(srcPath, &width, &height, &channels, 0);
    double tCargaImgFin = omp_get_wtime();
    printf("El tiempo de carga de la imagen es: %lf\n", tCargaImgFin - tCargaImgIn);
    if (srcIma == NULL)
    {
        printf("No se pudo cargar la imagen %s :(\n\n\n", srcPath);
        return -1;
    }
    else if(channels == 3)
    {
        printf("Imagen cargada correctamente: %dx%d pixeles con %d canales.\n", width, height, channels);
        int imaSize = width * height;

        // SE MULTIPLICA POR EL VALOR DE CHANELS POR QUE AUNQUE SOLO VAMOS A TOMAR EN CUENTA EN CADA UNO DE LOS ARREGLOS EL VALOR CORRESPONDIENTE A CADA COLOR EN CADA PIXEL , CADA PIXEL TIENE 3 VALORES ES DECIR 3 BYTES Y DOS DE ESTOS LOS ESTABLECEREMOS EN 0 
        unsigned char *imaBlue = malloc(imaSize * channels); 
        unsigned char *imaRed = malloc(imaSize * channels);
        unsigned char *imaGreen = malloc(imaSize * channels);
        double tInicial = omp_get_wtime();
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
        double tFinal = omp_get_wtime();
        double tTotal = tFinal - tInicial;
        double tEjecucionSecuencial = CountingSort(imaRed, width, height, channels);
        tEjecucionSecuencial = tEjecucionSecuencial + tTotal;
        stbi_write_jpg("eqImage_secuencial.jpg", width, height, 3, imaRed, 100);


        CountingSortImgComplet(srcIma, width, height, channels);
        stbi_write_jpg("Ecualizacion_completa.jpg", width, height, 3, srcIma, 100);

        // LIBERAMOS LA MENORIA DE LA IMAGEN 
        stbi_image_free(imaRed);
        stbi_image_free(srcIma);
        return tEjecucionSecuencial;
    }
    else if (channels == 1)
    {
        printf("\nImagen cargada correctamente: %dx%d pixeles con %d canales.\n", width, height, channels);

        // CON EL ARREGLO IMARED YA PODEMOS OBTENER EL HISTOGRAMA APOYANDONOS DEL ALGORITMO COUNTING SORT
        double tEjecucionSecuencial = CountingSort(srcIma, width, height, channels);
        // DESPUES DEL COUNTING SORT IMARED (EL ARREGLO), YA ESTA ECUALIZADO
        // Saving image
        stbi_write_jpg("eqImage_secuencial.jpg", width, height, 1, srcIma, 100);

        // Liberar la memoria de la imágen
        stbi_image_free(srcIma);  // free memory
        return tEjecucionSecuencial;
    }
    else{
        printf("\nERROR: La imagen debe de ser de 1 0 3 canales.");
        return -1;
    }


}
// A LA FUNCION LE PASAMOS EL ARREGLO, RECORDANDO QUE EN C LOS ARREGLOS SIEMPRE SE PASAN POR REFERENCA, ES DECIR EL PUNTERO QUE APUNTA A ESTOS 
double CountingSort(unsigned char A[], int width, int height, int channels) {
    // BUSQUEDA DEL MAXIMO, EN ESTE CASO NO ES NECESARIO POR QUE NUESTRSO ARREGLOS SIEMPRE SERAN DE TAMAÑO 256 POR QUE SON LOS VALORES QUE PUEDEN TOMAR LOS ELEMENTOS RGB DE NUESTROS PIXELES
    int arrTam = 256;
    // NO ES NECESARIO UN CATEO POR QUE EN C PODEMOS ASIGNAR PUNTEROS DE TIPO VOID A UN PUNTERO DE TIPO UNSIGNED CHAR SIN NECESIDAD DE UN CASTEO EXPLICITO
    // USAMOS CALLOC PARA INICALIZAR EN 0 LOS ARREGLOS SIN LA NECESIDAD DE TENER QUE HACER UN FOR
    int *C = (int*)calloc(arrTam, sizeof(int));
    int *B = (int*)calloc(arrTam, sizeof(int));
    if(channels == 1)
    {
        double tInicialCsv = 0.0;
        double tFinalCsv = 0.0;
        double tInicial = omp_get_wtime();
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
        tInicialCsv = omp_get_wtime();
        Ecualizacion(C, width, height);
        GuardarHistograma(B, C, "histo_secuencial.csv");
        tFinalCsv = omp_get_wtime();
        // B ES NUESTRO HISTOGRAMA, C ES NUESTRO ECUALIZADO
        // ACTUALIZAMOS EL ARREGLO A PARA QUE SE ECUALICE 
        for (int i = 0; i < (width*height); i++) {
            A[i] = (unsigned char)C[A[i]];
        }
        double tFinal = omp_get_wtime();
        printf("Tiempo de generacion del archivo CSV: %lfs\n", tFinalCsv-tInicialCsv);
        // ELIMINAMOS LOS TIEMPOS DE LA GENERACION DEL ARCHIVO CSV 
        double tTotal = (tFinal - tInicial)-(tFinalCsv- tInicialCsv);
        // LIBERAMOS LA MEMORIA 
        free(C);
        free(B);
        return tTotal;
    }
    else if (channels == 3)
    {   
        double tInicialCsv = 0.0;
        double tFinalCsv = 0.0;
        double tInicial = omp_get_wtime();
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
        tInicialCsv = omp_get_wtime();
        Ecualizacion(C, width, height);
        GuardarHistograma(B, C, "histo_secuencial.csv");
        tFinalCsv = omp_get_wtime();
        // YA CON LA FUNCION DE DISTRIBUCION ACUMULADA ECUALIZAMOS Y GUARDAMOS LOS VALORES
        //B ES NUESTRO HISTOGRAMA, C ES NUESTRO ECUALIZADO
        // ACTUALIZAMOS EL ARREGLO A PARA QUE SE ECUALICE 
        for (int i = 0; i < (width*height); i++) {
            A[i * channels] = (unsigned char)C[A[i*channels]];
        }
        double tFinal = omp_get_wtime();
        printf("Tiempo de generacion del archivo CSV: %lfs\n", tFinalCsv-tInicialCsv);
        // ELIMINAMOS LOS TIEMPOS DE LA GENERACION DEL ARCHIVO CSV 
        double tTotal = (tFinal - tInicial)-(tFinalCsv- tInicialCsv);
        // LIBERAMOS LA MEMORIA 
        free(C);
        free(B);
        return tTotal;
    }
    else 
    {
        printf("No es posible ecualizar imagenes con ese numero de canales");
        free(C);
        free(B);
        return -1;
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
void GuardarHistograma(int B[], int C[], char nombre_Archivo[])
{
    // ABRIMOS EL ARCHIVO CON PERMISOS DE ESCRITURA
    FILE *fp = fopen(nombre_Archivo, "w+"); // FOPEN SI NO EXISTE EL ARCHIVO LO CREA
    
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


//EMPEZAMOS A DESARROLLAR LAS FUNCIONES QUE VAN A USAR EL PARALELISMO
double splitChannelsParalel(char *Img)
{
    // OBTENERMOS EL VALOR QUE ALOGA A DONDE APUNTA IMG
    char *srcPath = Img; 

    int width, height, channels;
    //EL APUNTADOR *SCRIMA APUNTA AUN ARREGLO DE TAMAÑO WIDTH*HEIGHT*CHANNELS DE LOS CANALES QUE TIENE LA IMAGEN
    double tCargaImgIn = omp_get_wtime();
    unsigned char *srcIma = stbi_load(srcPath, &width, &height, &channels, 0);
    double tCargaImgFin = omp_get_wtime();
    printf("El tiempo de carga de la imagen es: %lf\n", tCargaImgFin - tCargaImgIn);

    if (srcIma == NULL)
    {
        printf("No se pudo cargar la imagen %s :(\n\n\n", srcPath);
        return -1;
    }
    else if(channels == 3)
    {
        printf("Imagen cargada correctamente: %dx%d pixeles con %d canales.\n", width, height, channels);
        int imaSize = width * height;

        // SE MULTIPLICA POR EL VALOR DE CHANELS POR QUE AUNQUE SOLO VAMOS A TOMAR EN CUENTA EN CADA UNO DE LOS ARREGLOS EL VALOR CORRESPONDIENTE A CADA COLOR EN CADA PIXEL , CADA PIXEL TIENE 3 VALORES ES DECIR 3 BYTES Y DOS DE ESTOS LOS ESTABLECEREMOS EN 0 
        unsigned char *imaBlue = malloc(imaSize * channels); 
        unsigned char *imaRed = malloc(imaSize * channels);
        unsigned char *imaGreen = malloc(imaSize * channels);
        double tInicial = omp_get_wtime();
        #pragma omp parallel for
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
        double tFinal = omp_get_wtime();
        double tTotal = tFinal - tInicial;
        double timeEjecParalela = CountingSortParalel(imaRed, width, height, channels);
        timeEjecParalela = timeEjecParalela + tTotal;
        
        stbi_write_jpg("eqImage_parallel.jpg", width, height, 3, imaRed, 100);
        stbi_image_free(imaRed);

        return timeEjecParalela;
    }
    else if (channels == 1)
    {
        printf("\nImagen cargada correctamente: %dx%d pixeles con %d canales.\n", width, height, channels);
        double timeEjecParalela = CountingSortParalel(srcIma, width, height, channels);

        stbi_write_jpg("eqImage_parallel.jpg", width, height, 1, srcIma, 100);
        stbi_image_free(srcIma);  

        return timeEjecParalela;
    }
    else{
        printf("\nERROR: La imagen debe de ser de 1 0 3 canales.");
        return -1;
    }


}
double CountingSortParalel(unsigned char A[], int width, int height, int channels) {
    // BUSQUEDA DEL MAXIMO, EN ESTE CASO NO ES NECESARIO POR QUE NUESTRSO ARREGLOS SIEMPRE SERAN DE TAMAÑO 256 POR QUE SON LOS VALORES QUE PUEDEN TOMAR LOS ELEMENTOS RGB DE NUESTROS PIXELES
    int arrTam = 256;
    // NO ES NECESARIO UN CATEO POR QUE EN C PODEMOS ASIGNAR PUNTEROS DE TIPO VOID A UN PUNTERO DE TIPO UNSIGNED CHAR SIN NECESIDAD DE UN CASTEO EXPLICITO
    // USAMOS CALLOC PARA INICALIZAR EN 0 LOS ARREGLOS SIN LA NECESIDAD DE TENER QUE HACER UN FOR
    int *C = (int*)calloc(arrTam, sizeof(int));
    int *B = (int*)calloc(arrTam, sizeof(int));

    if(channels == 1)
    {
        int num_procs = omp_get_num_procs();
        omp_set_num_threads(num_procs);
        printf("Numero de nucleos disponibles: %d\n", num_procs);
        double tInicialCsv = 0.0;
        double tFinalCsv = 0.0;
        double tInicial = omp_get_wtime();
    #pragma omp parallel
    {
        // CONTAMOS LA FRECUENCIA DE CADA VALOR DE A (HISTOGRAMA)
        // NO HAY RIESGO DE CONDICIÓN DE CARRERA
        #pragma omp for 
        for (int j = 0; j <= (width*height); j++) {
            C[A[j]] = C[A[j]] + 1;
        }

        // NO HAY RIESGO DE CONDICIÓN DE CARRERA
        #pragma omp for 
        for (int j = 0; j <= arrTam; j++) {
            B[j] = C[j]; // IGUALAMOS B Y C PARA QUE NOS AYUDEN CON EL CSV
        }
        // CALCULAMOS LA FUNCION DE DISTRIBUCION ACUMULADA EN C
        // NO ES COVENIENTE SU PARALELIZACIÓN, POR LO QUE USAMOS SINGLE, SOLO LO EJECUTA UN HILO ESTE BUCLE
        #pragma omp single
        {
        for (int i = 1; i <= arrTam+1; i++) {
            C[i] = C[i] + C[i - 1];
        }
        //double tFinal = omp_get_wtime();
        //double tTotal = tFinal- tInicial;
        // YA CON LA FUNCION DE DISTRIBUCION ACUMULADA ECUALIZAMOS Y GUARDAMOS LOS VALORES
        //Ecualizacion(C, width, height);
        tInicialCsv = omp_get_wtime();
        Ecualizacion(C, width, height);
        GuardarHistograma(B, C, "histo_parallel.csv");
        tFinalCsv = omp_get_wtime();
        }
        #pragma omp barrier
        // B ES NUESTRO HISTOGRAMA, C ES NUESTRO ECUALIZADO
        // ACTUALIZAMOS EL ARREGLO A PARA QUE SE ECUALICE 
        //tInicial = omp_get_wtime();
        #pragma omp for
        for (int i = 0; i < (width*height); i++) {
            A[i] = (unsigned char)C[A[i]];
        }
    }
        double tFinal = omp_get_wtime();
        printf("Tiempo de generacion del archivo CSV: %lfs\n", tFinalCsv-tInicialCsv);
        // ELIMINAMOS LOS TIEMPOS DE LA GENERACION DEL ARCHIVO CSV 
        double tTotal = (tFinal - tInicial)-(tFinalCsv- tInicialCsv);
        // LIBERAMOS LA MEMORIA 
        free(C);
        free(B);
        return tTotal;

    }
    else if (channels == 3)
    {   
    // OBTENDREMOS LOS VALORES DEL CANAL ROJO
        // COMO TENEMOS 3 CANALES LOS VALORES ROJOS SON LOS VALORES MULTIPLOS DE 3
        // CONTAMOS LA FRECUENCIA DE CADA VALOR DE A (HISTOGRAMA)
        // EL RANGO ES WIDHT*HEIGHT YA QUE COMO ESTAMOS LLENDO DE 3 EN TRES, ES COMO SI DIVIDIERAMOS EL TAMAÑO DEL ARREGLO ENTRE 3, POR ESTA RAZON NO DEBEMOS MULTIPLICAR EL RANGO POR CHANNELS 
        int num_procs = omp_get_num_procs();
        omp_set_num_threads(num_procs);
        printf("Numero de nucleos disponibles: %d\n", num_procs);
        double tInicialCsv = 0.0;
        double tFinalCsv = 0.0;
        double tInicial = omp_get_wtime();
        #pragma omp parallel
    {
    
        #pragma omp for 
        for (int j = 0; j < (width*height); j++) {
            int idx = A[j * channels]; 
            #pragma omp atomic
            C[idx] += 1;
        }
        // AQUI B SOLO ES UNA COPIA QUE NOS AYUDA A REPRESNETAR EL CSV, POR ESO NO MULTIPLICAMOS POR CHANNELS
        #pragma omp for
        for (int j = 0; j < arrTam; j++) {
            B[j] = C[j]; // IGUALAMOS B Y C PARA QUE NOS AYUDEN CON EL CSV
        }
        // CALCULAMOS LA FUNCION DE DISTRIBUCION ACUMULADA EN C
        #pragma omp single //SOLO QUEREMOS QUE SE HAGA ESTO UNA VEZ, POR ESO EL SINGLE
        {
        for (int i = 1; i < arrTam; i++) {
            C[i] = C[i] + C[i - 1];
        }
        //double tFinal = omp_get_wtime();
        //double tTotal = tFinal- tInicial;
        //B ES NUESTRO HISTOGRAMA, C ES NUESTRO ECUALIZADO
        tInicialCsv = omp_get_wtime();
        Ecualizacion(C, width, height);
        GuardarHistograma(B, C, "histo_parallel.csv");
        tFinalCsv = omp_get_wtime();
        }
        // ESPERAMOS A QUE NOS ACABE DE DAR EL ECUALIZADO ESTE HILO
        #pragma omp barrier
        // ACTUALIZAMOS EL ARREGLO A PARA QUE SE ECUALICE 
        // NO HAY RIESGO DE CONDICIÓN DE CARRERA
        //tInicial = omp_get_wtime();
        #pragma omp for 
        for (int i = 0; i < (width*height); i++) {
            A[i * channels] = (unsigned char)C[A[i*channels]];
        }
    }
        double tFinal = omp_get_wtime();
        printf("Tiempo de generacion del archivo CSV: %lfs\n", tFinalCsv-tInicialCsv);
        // ELIMINAMOS LOS TIEMPOS DE LA GENERACION DEL ARCHIVO CSV 
        double tTotal = (tFinal - tInicial)-(tFinalCsv- tInicialCsv);
        // LIBERAMOS LA MEMORIA 
        free(C);
        free(B);
        return tTotal;
    }
    else 
    {
        printf("No es posible ecualizar imagenes con ese numero de canales");
        free(C);
        free(B);
        return -1;
    }
    
}   
void CountingSortImgComplet(unsigned char A[], int width, int height, int channels){
    int arrTam = 256;

    for (int i = 0; i < 3; i++)
    { 
        int *B = (int*)calloc(arrTam, sizeof(int));
        int *C = (int*)calloc(arrTam, sizeof(int));
            for (int j = 0; j < (width*height); j++) {
                C[A[j * channels + i]] += 1;
            }
            for (int j = 0; j < arrTam; j++) {
                B[j] = C[j];
            } 
            for (int j = 1; j < arrTam; j++) {
                C[j] = C[j] + C[j - 1];
            }
            Ecualizacion(C, width, height);
            for (int j = 0; j < (width*height); j++) {
                A[j * channels + i] = (unsigned char)C[A[j *channels + i]];
            }
        free(C);
        free(B);
    }
}

void Resultados(double tiempoSecuencial, double tiempoParalelo)
{
    int num_procs = omp_get_num_procs();
    double speedUp = tiempoSecuencial / tiempoParalelo;
    double Eficiencia = speedUp / (double)num_procs;
    double OverHead = tiempoParalelo - (tiempoSecuencial/(double)num_procs);

    printf("-----------------------------------------------\n");
    printf("Se cuenta con un SpeedUp de: %f \n", speedUp);
    printf("Se presento una Eficiencia del %f%% \n", Eficiencia*100);
    printf("OverHead: %f", OverHead);
}


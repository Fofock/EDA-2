#include <stdio.h> 
#include <stdlib.h>
#include <omp.h>
#include <math.h>
#define n 100000000

void llenaArreglo(int *a); 
void sumaSecuencial(int *a,int *b,int *c);
void sumaParalela(int *A, int *B, int *C);
void sumaPragmaFor(int *A, int *B, int *C);

int main()
{ 
    int max,*a,*b,*c; 
    a=(int *)malloc(sizeof(int)*n); 
    b=(int *)malloc(sizeof(int)*n); 
    c=(int *)malloc(sizeof(int)*n);
    printf("**********************\n** Suma de arreglos **\n**********************\n");
    llenaArreglo(a); 
    llenaArreglo(b); 
    printf("\n------------------------------------------------------------------------------------\n");
    printf("Iniciando Suma...\n\n");
    sumaSecuencial(a,b,c);
    sumaParalela(a,b,c);
    sumaPragmaFor(a,b,c);
    

} 

void llenaArreglo(int *a)
{ 
    int i; 
    for(i=0;i<n;i++) 
    { 
        a[i]=rand()%n; 
        //printf("%d\t", a[i]); 
    }  
}

void sumaSecuencial(int *A, int *B, int *C)
{ 
    int i;
    double Ti = omp_get_wtime();
    for(i=0;i<n;i++)
    { 
        C[i]=A[i]+B[i]; 
        //printf("%d\t", C[i]); 
    }
    double Tf = omp_get_wtime();
    double Tt = Tf - Ti;
    printf("\nTiempo Secuencial: %lf\n\n", Tt);
} 

void sumaParalela(int *A, int *B, int *C)
{
    int i,tid,inicio,fin; 
    omp_set_num_threads(2);
    double Ti = omp_get_wtime();
#pragma omp parallel private(inicio,fin,tid,i) 
    { 
        tid = omp_get_thread_num();
        int size = n; //TAMAÑO DEL ARREGLO
        int mitad = size / 2;
        inicio = (tid * 1) * mitad; 
        fin = (tid+1)*mitad; 
        for(i=inicio;i<fin;i++) 
        {
            C[i]=A[i]+B[i]; 
            //printf("%d\t", C[i]);
        }
    }
    double Tf = omp_get_wtime();
    double Tt = Tf - Ti;
    printf("\nUsando 2 hilos\nTiempo paralelo: %lf\n\n", Tt);
}

void sumaPragmaFor(int *A, int *B, int *C)
{ 
    int i,tid,tnum;
    double Ti = omp_get_wtime();
    omp_set_num_threads(omp_get_max_threads());
#pragma omp parallel private(tid) 
    { 
        tid = omp_get_thread_num();
        
#pragma omp for
        for(i=0;i<n;i++)
        { 
            C[i]=A[i]+B[i]; 
            //printf("%d\t", C[i]); 
        }
    }
    double Tf = omp_get_wtime();
    double Tt = Tf - Ti;
    printf("\nUsando %d hilos\nTiempo paralelo for: %lf\n", omp_get_max_threads(),Tt);
    printf("Nucleos logicos disponibles: %d\n", omp_get_max_threads());
} 

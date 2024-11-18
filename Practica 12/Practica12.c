#include <stdio.h> 
#include <omp.h>

double num_steps = 100000000;
double piSecuencial();
double piParalelo();

int main(int argc, char* argv[])
{
    // RECUPERAMOS LOS VALORES DE TIEMPO QUE CALCULAMOS EN ESTAS FUCNIONES PARA LOS CALCULOS DE SPEED UP
    double tSecuencial = piSecuencial();
    double tPararelo = piParalelo();
    printf("El Speedup es: %8.6lf \n", tSecuencial/tPararelo);
    int num_procs = omp_get_num_procs();
    printf("La Eficiencia es: %8.6lf \n", tSecuencial/(tPararelo * num_procs));
    printf("El tiempo de Overhead es: %8.6lf \n", tPararelo - (tSecuencial / num_procs));

} 

double piSecuencial()
{
    double x, pi, sum=0.0;
    int i;
    double step = 1.0/num_steps;
    double tInicial =omp_get_wtime( );
    for (i=0; i<num_steps; i++)
        {
        x = (i + .5)*step;
        sum = sum + 4.0/(1.+ x*x);
        }
    pi = sum*step;
    double tFinal = omp_get_wtime();
    double tiempo_ejecucion = tFinal - tInicial; 
    printf("El valor de PI es %15.12f\n",pi);
    printf("El tiempo de calculo del numero pi en secuencial es: %lf segundos\n",tiempo_ejecucion);
    return tiempo_ejecucion;
}

double piParalelo()
{
    double pi = 0.0;
    double step = 1.0 / num_steps;

    // Configurar el número de hilos igual a la cantidad de núcleos del procesador
    int num_procs = omp_get_num_procs();
    omp_set_num_threads(num_procs);
    printf("Numero de nucleos disponibles: %d\n", num_procs);

    double tInicial = omp_get_wtime();

    #pragma omp parallel
    {
        double sum = 0.0;
        #pragma omp for
        for (int i = 0; i < (int)num_steps; i++)
        {
            double x = (i + 0.5) * step;
            sum += 4.0 / (1.0 + x * x);
        }

        // CON ESTO EVITAMOS LA CONDICION DE CARRERA, DE ESTA MANERA NO TENEMOS QUE USAR CRITICAL, HACIENDO UN POCO MÁS EFICIENTE EL CÓDIGO 
        #pragma omp atomic 
        pi += sum * step;
    }

    double tFinal = omp_get_wtime();
    double tiempo_ejecucion = tFinal - tInicial; 
    printf("El valor de PI es %15.12f\n", pi);
    printf("El tiempo de calculo del numero pi en paralelo es: %lf segundos\n", tiempo_ejecucion);
    return tiempo_ejecucion;
}
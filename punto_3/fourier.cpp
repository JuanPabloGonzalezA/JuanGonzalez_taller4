#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <cmath>
using namespace std;

int main(int argc, char* argv[])
{
	//obtengo el nombre del archivo que se ingresa en la terminal (SE DEBE EJECUTAR COMO DICE EN EL TALLER: ./fourier datos.txt)
	string archivo;
	archivo= argv[1];
	//LECTURA DE DATOS
	string line;
	ifstream a_entrada(archivo.c_str());
	double tiempo;
	double funcion;
	vector<double> t ;
	vector<double> f ;
	int i;
	int j;
	int k;
	while(a_entrada >> tiempo >> funcion)
	{
		t.push_back(tiempo);
		f.push_back(funcion);
	}
	int N = t.size();
	vector<double>f_inter(N);
	vector<double>t_inter(N);
	vector<double>l(N);
	
	//creo el arreglo de t espaciados igualmente:
	double espacio=(t[N-1]-t[0])/(N-1);
	for(i=0;i<N;i++)
	{
		t_inter[i]=t[0]+(i*espacio);
	}
	//calculo el interpolado de f(t) con el polinomio de lagrange:
	double suma;
	double multiplicatoria;
	for(i=0;i<N;i++)
	{
		f_inter[i]=0;
		for(j=0;j<N;j++)
		{
			multiplicatoria=1;
			for(k=0;k<N;k++)
			{
				if(k==j)
				{
					continue;
				}
				else
				{
					multiplicatoria=multiplicatoria*(t_inter[i]-t[k])/(t[j]-t[k]);
				}
			}
			f_inter[i]+=f[j]*multiplicatoria;
		}
	}
	//YA TENGO LOS DATOS EQUIESPACIADOS EN T, AHORA CALCULO LA TRANSFORMADA
	vector<double>re(N);//parte real de la transformada
	vector<double>im(N);//parte imaginaria de la transformada
	vector<double>freq(N);//frecuencias
	double pi = 3.14159265359;
	
	//transformada
	for(i=0;i<N;i++)
	{
		re[i]=0;
		im[i]=0;
		for(j=0;j<N;j++)
		{
			re[i]+=f_inter[j]*cos(2*pi*j*i/N);
			im[i]+=-1*f_inter[j]*sin(2*pi*j*i/N);
		}
	}
	//frecuencias
	if(N%2==0)
	{
		for(i=0;i<N;i++)
		{
			if(i<(int)(N/2))
			{
				freq[i]=i/(espacio*N);
			}else
			{
				freq[i]=-(N-i)/(espacio*N);
			}
			
		}
	}else
	{
		for(i=0;i<N;i++)
		{
			if(i<=(int)((N-1)/2))
			{
				freq[i]=i/(espacio*N);
			}else
			{
				freq[i]=-(N-i)/(espacio*N);
			}	
		}
	}


	//IMPRIMO EN EL ARCHIVO DE SALIDA
	ofstream a_salida ("transformada.txt");
	
	for(i=0;i<N;i++) {
        	a_salida <<freq[i]<<" "<< re[i]<<" "<<im[i]<< '\n';
	}
    	a_salida.close();

	return 0;
}

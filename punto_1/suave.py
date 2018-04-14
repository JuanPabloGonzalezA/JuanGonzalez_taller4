import numpy as np
import matplotlib.pyplot as plt
import cmath #libreria que me deja ecribir e^(ix) porque es mas corto que escribir cos() + i*sen() en mis funciones de transformada y transformada inversa de la imagen

#datos de entrada: nombre de imagen y ancho del kernel
archivo='imagen.png'
n_pixel_kernel=20

#funcion gaussiana en 2D PARA ARMAR EL KERNEL
def gauss(x,y,sigma=1.0):
	return np.exp(-1.0*(x**2+y**2)/(2.0*sigma**2))/(2.0*np.pi*sigma**2)

#funcion que genera el kernel gaussiano: 
def krn(n):
	ker=np.zeros((n,n))
	x=np.linspace(-(n/2),n/2,n)
	for i in range(0,n):
		for j in range(0,n):
			ker[i,j]=gauss(x[i],x[j],np.sqrt(10))

	return ker

#funcion que retorna la transformada de fourier discreta 2D de la imagen:
def fourier(M):
	l=M.shape[0]
	w=M.shape[1]
	n=M.shape[2]
	fM=np.zeros((l,w,n),dtype=np.complex)
	for a in range(l):
		for b in range(w):
			for c in range(l):
				for d in range(w):
					for e in range(n):
						fM[a,b,e] += M[c,d,e]*cmath.exp(-1.0j*2.0*np.pi*(1.0*a*c/(1.0*l) + 1.0*b*d/(1.0*w)))
			fM[a,b]=fM[a,b]/(1.0*w*l)
	return fM

#funcion que retorna la transformada inversa la imagen
def inversa(M):
	l=M.shape[0]
	w=M.shape[1]
	n=M.shape[2]
	fM=np.zeros((l,w,n),dtype=np.complex)
	for c in range(l):
		for d in range(w):
			for a in range(l):
				for b in range(w):
					for e in range(n):
						fM[c,d,e]+=M[a,b,e]*cmath.exp(1.0j*2.0*np.pi*(1.0*a*c/(1.0*l) + 1.0*b*d/(1.0*w)))
	return fM
#-------------------------------------------------------------------------------------
#mensaje de alerta 
print 'ATENCION: se demora demasiado (1 minuto aprox para imagenes de 32 por 32 pixeles). No intentar con imagenes mas grandes porque el tiempo incrementa a la cuarta potencia'

#cargo mi imagen
original = plt.imread(archivo)

#largo y ancho de mi imagen
largo=original.shape[0]
ancho=original.shape[1]

#creacion de Kernel con las dimensiones dadas por n_pixel_kernel con mi funcion kernel
ker = krn(n_pixel_kernel)
ker=ker/np.sum(ker)

#transformada de la imagen USANDO MI TRANSFORMADA DE FOURIER fourier()
Foriginal=fourier(original)

from scipy import fftpack
Fker = fftpack.fft2(ker, [largo,ancho])#transformada del kernel con dimensiones de la imagen para hacer el producto

#creacion final
convolucion = Fker[:, :, np.newaxis]*Foriginal #multiplico las transformadas del kernel y la imagen elemento a elemento
#me devuelvo al espacio de pixeles original USANDO MI TRANSFORMADA INVERSA inversa() cogiendo los valores reales de la transormada
imagensuave=inversa(convolucion).real


plt.imshow(imagensuave)
plt.axis('off')
plt.savefig('suave.png')

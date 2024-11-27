import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

def f(x):
    return np.sin(np.exp(2*x))


def trapezi(a, b, m):
    h = (b - a) / m

    suma = 0
    for i in range(1, m):
        suma += f(h*i)
    
    return h/2*(f(a) + 2*suma + f(b))

def simpson(a, b, m):
    h = (b - a) / (2*m)
    
    suma = 0
    for i in range(1, m + 1):
        suma += f(h*(2*i-2)) + 4*f(h*(2*i-1)) + f(h*2*i)

    return h/3*suma

real = quad(f, 0, 2)[0] #calcul de la integral
print("Valor exacte: ", real)
print('\nExercici 1 i 2')
print('--------------------\n')

numIntervals = 1
errVecAbs = [[], []]
inici = 0 
fi = 2
espais = 25 # per formatejar els prints
while numIntervals <= 2**14: # segons la nostre predicció en necesitarem 2^12 n'afegim un mes per a que es vegi millor
    
    trap = trapezi(inici, fi, numIntervals)
    simp = simpson(inici, fi, numIntervals)
    
    errVecAbs[0].append(abs(trap-real))
    errVecAbs[1].append(abs(simp-real))
    
    print(f'Trapezi per m = {numIntervals:>5}: {trap:>{espais}}, error absolut = {abs(trap - real):>{espais}}')
    print(f'Simpson per m = {numIntervals:>5}: {simp:>{espais}}, error absolut = {abs(simp - real):>{espais}}')
    print('')
    numIntervals *= 2

x = np.arange(0, len(errVecAbs[0]))
errVecAbsTrap = np.array(np.log10(errVecAbs[0]))
errVecAbsSimp = np.array(np.log10(errVecAbs[1]))
plt.plot(x, errVecAbsTrap, label='Trapezi')
plt.plot(x, errVecAbsSimp, label='Simpson')
plt.xlabel('log_2(nombre intervals)')
plt.ylabel('log_10(error)')
plt.legend()
plt.grid(True)
plt.show()


#Pregunta 4

#Per a obtenir 6 xifres significatives
numIntervalsTrap = 6085
numIntervalsSimp = 317
trap = trapezi(inici, fi, numIntervalsTrap)
simp = simpson(inici, fi, numIntervalsSimp)

print('\nExercici 4')
print('--------------------\n')
print(f'Trapezi amb {numIntervalsTrap:>5} intervals: {trap:>{espais}}, error absolut = {abs(trap - real):>{espais}}')
print(f'Simpson amb {numIntervalsSimp:>5} intervals: {simp:>{espais}}, error absolut = {abs(simp - real):>{espais}}')
print(f'Valor real = {real:>{10+espais}}')


def simpsonSimple(a, b):
    return (b - a)/6*(f(a) + 4*f((a+b)/2) + f(b))

def simpsonRecursiu(f, a, b, tol):
    mid = (a + b) / 2
    S_ab = simpsonSimple(a, b)
    S_amid = simpsonSimple(a, mid)
    S_midb = simpsonSimple(mid, b)
    estimation = abs(S_ab - (S_amid + S_midb))
    if estimation < tol*(b - a): return S_ab
    else: return simpsonRecursiu(f, a, mid, tol) + simpsonRecursiu(f, mid, b, tol)

print(f(0), inici, fi)
S3 = simpsonRecursiu(f, inici, fi, 1e-3)
S6 = simpsonRecursiu(f, inici, fi, 1e-6)
print(f"Valor calculat amb l'algorisme de simpson adaptat amb tolerancia= {1e-3}: {S3} amb error = {abs(real - S3)}")
print(f"Valor calculat amb l'algorisme de simpson adaptat amb tolerancia= {1e-6}: {S6} amb error = {abs(real - S6)}")
print(f'Valor real = {real}')

#Pregunta 5

#fa el mateix que el simpson recursiu pero retorna els punts extrems dels intervals en que ha dividit el (0, 2)
def simpsonRecursiu2(f, a, b, divide_points, tol):
    mid = (a + b) / 2
    S_ab = simpsonSimple(a, b)
    S_amid = simpsonSimple(a, mid)
    S_midb = simpsonSimple(mid, b)
    estimation = abs(S_ab - (S_amid + S_midb))
    if estimation < tol*(b - a):
        divide_points.append(a)
        return S_ab
    else: return simpsonRecursiu2(f, a, mid, divide_points, tol) + simpsonRecursiu2(f, mid, b, divide_points, tol)

divide_points3 = []
divide_points6 = []
S3 = simpsonRecursiu2(f, inici, fi, divide_points3, 1e-3)
S6 = simpsonRecursiu2(f, inici, fi, divide_points6, 1e-6)
divide_points3.sort()
divide_points6.sort()

F3 = f(np.array(divide_points3))
F6 = f(np.array(divide_points6))
plt.plot(divide_points3, F3, 'o-', label='Tolerancia 10**-3')
plt.grid(True)
plt.legend()
plt.show()

plt.plot(divide_points6, F6,'o-', label='Tolerancia 10**-6')
plt.grid(True)
plt.legend()
plt.show()

print(f'Nombre de subintervals amb tolerància 10**-3: {len(divide_points3) - 1}')
print(f'Nombre de subintervals amb tolerància 10**-6: {len(divide_points6) - 1}')
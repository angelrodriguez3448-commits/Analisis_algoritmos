import matplotlib.pyplot as mp #Biblioteca para generar graficas
import time #Biblioteca para medir tiempo
from random import sample # Importamos un Método de la biblioteca random para generar listas aleatorias

lista = list(range(1000)) # Creamos la lista base con números del 1 al 1000

tamannos = list(range(50, 1001, 50)) # Creamos lista de tamaños de 50 a 1000, con incremento de 50
tiempos = {
    "bubble": {tam: [] for tam in tamannos},
    "merge": {tam: [] for tam in tamannos},
    "quick": {tam: [] for tam in tamannos}
} # Creamos un diccionario para guardar los tiempos

def generador(N):
    vectorGen = sample(lista,(N * 50))
    return vectorGen

def grafica():
    fig, ax = mp.subplots()

    tipos = ["bubble", "merge", "quick"] # Lista de tipos de busqueda
    colores = {"bubble": "#FF6500", "merge": "#000B58", "quick": "#000000"} # Colores para cada tipo

    for tipo in tipos:
        valoresY = []
        valoresX = []
        for tam in tamannos:
            tiempo = tiempos[tipo][tam]
            valoresY.append(tiempo)
            valoresX.append(tam)
        ax.plot(valoresX, valoresY, marker="o", label=tipo, color=colores[tipo])
    # Ciclo principal, dibuja la grafica

    ax.set_title("Tiempos de ordenamiento")
    ax.set_xlabel("Tamaño de lista")
    ax.set_ylabel("Tiempo")
    ax.legend()
    ax.grid(True)
    mp.show()

# Creamos una lista aleatoria con sample 
#(8 elementos aleatorios de la lista base)
vectorbs = sample(lista,8) 

def bubblesort(vectorbs):
    """Esta función ordenara el vector que le pases como argumento con el Método de Bubble Sort"""
    
    
    # Imprimimos la lista obtenida al principio (Desordenada)
    #print("El vector a ordenar es:",vectorbs)
    n = 0 # Establecemos un contador del largo del vector
    
    for _ in vectorbs:
        n += 1 #Contamos la cantidad de caracteres dentro del vector
    
    for i in range(n-1): 
    # Le damos un rango n para que complete el proceso. 
        for j in range(0, n-i-1): 
            # Revisa la matriz de 0 hasta n-i-1
            if vectorbs[j] > vectorbs[j+1] :
                vectorbs[j], vectorbs[j+1] = vectorbs[j+1], vectorbs[j]
            # Se intercambian si el elemento encontrado es mayor 
            # Luego pasa al siguiente
    #print ("El vector ordenado es: ",vectorbs)

bubblesort(vectorbs)

# Creamos una lista aleatoria con sample 
#(8 elementos aleatorios de la lista base)
vectormerge = sample(lista,8)

def mergesort(vectormerge): 
    
    """Esta función ordenara el vector que le pases como argumento 
    con el Método Merge Sort"""
    
    # Imprimimos la lista obtenida al principio (Desordenada)
    #print("El vector a ordenar con merge es:", vectormerge)
    
    def merge(vectormerge):
    
        def largo(vec):
                largovec = 0 # Establecemos un contador del largovec
                for _ in vec:
                    largovec += 1 # Obtenemos el largo del vector
                return largovec
        
        
        if largo(vectormerge) >1: 
            medio = largo(vectormerge)//2 # Buscamos el medio del vector
            
            # Lo dividimos en 2 partes 
            izq = vectormerge[:medio]  
            der = vectormerge[medio:]
            
            merge(izq) # Mismo procedimiento a la primer mitad
            merge(der) # Mismo procedimiento a la segunda mitad
            
            i = j = k = 0
            
            # Copiamos los datos a los vectores temporales izq[] y der[] 
            while i < largo(izq) and j < largo(der): 
                if izq[i] < der[j]: 
                    vectormerge[k] = izq[i] 
                    i+= 1
                else: 
                    vectormerge[k] = der[j] 
                    j+= 1
                k += 1
            
            # Nos fijamos si quedaron elementos en la lista
            # tanto derecha como izquierda 
            while i < largo(izq): 
                vectormerge[k] = izq[i] 
                i+= 1
                k+= 1
            
            while j < largo(der): 
                vectormerge[k] = der[j] 
                j+= 1
                k+= 1
    merge(vectormerge)
    
    #print("El vector ordenado con merge es: ", vectormerge)
mergesort(vectormerge)

# Creamos una lista aleatoria con sample 
#(8 elementos aleatorios de la lista base)
vectorquick = sample(lista,8)

def quicksort(vectorquick, start = 0, end = len(vectorquick) - 1 ):
    
    """Esta función ordenara el vector que le pases como argumento 
    con el Método Quick Sort"""
    
    # Imprimimos la lista obtenida al principio (Desordenada)
    #print("El vector a ordenar con quick es:", vectorquick)
    
    def quick(vectorquick, start = 0, end = len(vectorquick) - 1):
        
        
        if start >= end:
            return

        def particion(vectorquick, start = 0, end = len(vectorquick) - 1):
            pivot = vectorquick[start]
            menor = start + 1
            mayor = end

            while True:
                # Si el valor actual es mayor que el pivot
                # está en el lugar correcto (lado derecho del pivot) y podemos 
                # movernos hacia la izquierda, al siguiente elemento.
                # También debemos asegurarnos de no haber superado el puntero bajo, ya que indica 
                # que ya hemos movido todos los elementos a su lado correcto del pivot
                while menor <= mayor and vectorquick[mayor] >= pivot:
                    mayor = mayor - 1

                # Proceso opuesto al anterior            
                while menor <= mayor and vectorquick[menor] <= pivot:
                    menor = menor + 1

                # Encontramos un valor sea mayor o menor y que este fuera del arreglo
                # ó menor es más grande que mayor, en cuyo caso salimos del ciclo
                if menor <= mayor:
                    vectorquick[menor], vectorquick[mayor] = vectorquick[mayor], vectorquick[menor]
                    # Continua el bucle
                else:
                    # Salimos del bucle
                    break

            vectorquick[start], vectorquick[mayor] = vectorquick[mayor], vectorquick[start]
            
            return mayor
        
        p = particion(vectorquick, start, end)
        quick(vectorquick, start, p-1)
        quick(vectorquick, p+1, end)
        
    quick(vectorquick)
    
    #print("El vector ordenado con quick es:", vectorquick)

quicksort(vectorquick)

def ordenador():
    tiempoIni = time.perf_counter()
    longitud = len(vectorbs)
    bubblesort(vectorbs)
    tiempoFin = time.perf_counter()
    tiempoTot = (tiempoFin - tiempoIni)
    tiempos["bubble"][longitud].append(tiempoTot)

    tiempoIni = time.perf_counter()
    longitud = len(vectormerge)
    mergesort(vectormerge)
    tiempoFin = time.perf_counter()
    tiempoTot = (tiempoFin - tiempoIni)
    tiempos["merge"][longitud].append(tiempoTot)

    
    tiempoIni = time.perf_counter()
    longitud = len(vectorquick)
    quicksort(vectorquick)
    tiempoFin = time.perf_counter()
    tiempoTot = (tiempoFin - tiempoIni)
    tiempos["quick"][longitud].append(tiempoTot)

for i in range(20):
    vectorbs = generador(i + 1)
    vectormerge = generador(i + 1)
    vectorquick = generador(i + 1)
    ordenador()

grafica()
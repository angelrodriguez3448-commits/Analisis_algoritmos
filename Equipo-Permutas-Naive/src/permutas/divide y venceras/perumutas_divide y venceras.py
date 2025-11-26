import time
import matplotlib.pyplot as plt
tiempos=[0]
tamanio=[0]

def permutas_fuerza_bruta(lista):
    # Caso base: si la lista tiene un solo elemento, es una permutación.
    if len(lista) == 1:
        return [lista]
    permutas_totales=[]
    # Recorrer cada elemento de la lista
    for i in range(len(lista)):
        elemento_actual = lista[i]
        # Crear una sub-lista con los elementos restantes
        resto_de_la_lista = lista[:i] + lista[i+1:]
        # Llamada recursiva para obtener las permutaciones de la sub-lista
        permutaciones_del_resto = permutas_fuerza_bruta(resto_de_la_lista)
        # Iterar sobre las permutaciones de la sub-lista
        for p in permutaciones_del_resto:
            # Añadir el elemento actual al inicio de cada permutación del resto
            nueva_permutacion = [elemento_actual] + p
            permutas_totales.append(nueva_permutacion)
    return permutas_totales

def medir_tiempo(funcion,lista):
    inicio = time.perf_counter()
    _ = funcion(lista)
    fin = time.perf_counter()
    tiempo_ms = (fin - inicio) * 1000
    return  tiempo_ms

def graficar():
    global tiempos
    global tamanio
    plt.plot(tamanio, tiempos, marker='o', color='r', linestyle='-')
    plt.title('Tiempos de ejecución de permutaciones por divide y vencerás')
    plt.xlabel('Tamaño de la lista (n)')
    plt.ylabel('Tiempo de ejecución (ms)')
    plt.grid()
    plt.show()
    
if __name__ == "__main__":
    for n in range(1,12):
        tiempos.append(medir_tiempo(permutas_fuerza_bruta,list(range(n))))
        tamanio.append(n)
        graficar()
        print(f"Tamaño: {n}, Tiempo: {tiempos[-1]:.4f} ms")
        input("Presiona Enter para continuar...")
        
        
   

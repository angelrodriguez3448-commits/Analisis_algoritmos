import matplotlib.pyplot as plt
import time
tiempos=[0]
tamanios=[0]
def permutas(lista,memoria={}):
    # Verificar si la permutación ya está en la memoria
    if tuple(lista) in memoria:
        # Devolver la permutación almacenada
        return memoria[tuple(lista)]
    # Caso base: si la lista tiene un solo elemento, es una permutación.
    if len(lista) <= 1:
        return [lista]
    # Lista para almacenar todas las permutaciones
    permutas_totales=[]
    # Recorrer cada elemento de la lista
    for i in range(len(lista)):
        elemento_actual = lista[i]
        # Crear una sub-lista con los elementos restantes
        resto_de_la_lista = lista[:i] + lista[i+1:]
        # Llamada recursiva para obtener las permutaciones de la sub-lista
        permutaciones_del_resto = permutas(resto_de_la_lista, memoria)
        # Iterar sobre las permutaciones de la sub-lista
        for p in permutaciones_del_resto:
            # Añadir el elemento actual al inicio de cada permutación del resto
            nueva_permutacion = [elemento_actual] + p
            permutas_totales.append(nueva_permutacion)
    # Almacenar la permutación en la memoria antes de devolverla
    memoria[tuple(lista)] = permutas_totales
    # Devolver todas las permutaciones encontradas
    return permutas_totales
def medir_tiempo(funcion, lista):
    inicio = time.time()
    funcion(lista)
    fin = time.time()
    return (fin - inicio)*1000
def graficar():
    global tiempos
    global tamanios
    plt.plot(tamanios, tiempos, marker='o', linestyle='-', color='green')
    plt.title('Tiempo de ejecución de la función de Permutas por programación dinámica')
    plt.xlabel('Tamaño de la lista')
    plt.ylabel('Tiempo de ejecución (ms)')
    plt.grid()
    plt.show()
if __name__ == "__main__":
    for n in range(1, 9):
        lista = list(range(n))
        tiempo_ejecucion = medir_tiempo(permutas, lista)
        tiempos.append(tiempo_ejecucion)
        tamanios.append(n)
       
        print(f"Tamaño de la lista: {n}, Tiempo de ejecución: {tiempo_ejecucion:.4f} ms")
    graficar()
    

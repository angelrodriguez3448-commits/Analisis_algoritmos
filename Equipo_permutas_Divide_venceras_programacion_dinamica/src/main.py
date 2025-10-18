import time
import random
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Listas globales para almacenar los tiempos y tamaños de entrada
tiempos_prog_din=[0]
tiempos_fuerza_bruta=[0]
tamanios_entrada=[0]
espera_ventana=None
#función para generar todas las permutaciones de una lista 
# con programación dinámica
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

#Función para medir el tiempo de ejecución de una función
def medir_tiempo(funcion,lista):
    #Empieza el conteo de tiempo
    inicio = time.perf_counter()
    resultado = funcion(lista)
    #Termina el conteo de tiempo
    fin = time.perf_counter()
    #Calcula el tiempo en milisegundos
    tiempo_ms = (fin - inicio) * 1000
    #retorna el resultado y el tiempo en milisegundos
    return resultado, tiempo_ms

#Función para calcular el factorial de un número
def factorial(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado

#Función de fuerza bruta para generar permutaciones
def generador_permutas_fuerza_bruta(lista):
    permutas=[]
    n = len(lista)
    permutas.append(list(lista))
    while len(permutas) < factorial(n):
        nueva_lista = list(lista)
        random.shuffle(nueva_lista)
        
        if nueva_lista not in permutas:
            permutas.append(nueva_lista)
    return permutas
#Función para generar una lista de números del 0 al tamaño-1
def generar_lista(tamanio):
    return list(range(tamanio))  

def comparacion_permutas(tamanio):
    # se mencionan las variables globales
    global tiempos_prog_din
    global tiempos_fuerza_bruta
    global tamanios_entrada
    # Muestra la ventana de espera
    ventana_espera()
    # Agrega el tamaño de la entrada a la lista
    tamanios_entrada.append(tamanio)
    # Genera la lista de números
    lista = generar_lista(tamanio)
    # Mide el tiempo de ambas funciones
    _, tiempo_prog_din = medir_tiempo(permutas, lista)
    _, tiempo_fuerza_bruta = medir_tiempo(generador_permutas_fuerza_bruta, lista)
    # Agrega los tiempos a las listas correspondientes
    tiempos_prog_din.append(tiempo_prog_din)
    tiempos_fuerza_bruta.append(tiempo_fuerza_bruta)
    root.geometry("700x600")
    graficar_resultados()
# Función para graficar los resultados
def graficar_resultados():
    # se mencionan las variables globales
    global tiempos_prog_din
    global tiempos_fuerza_bruta
    global tamanios_entrada
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    # Crea la figura y los ejes para la gráfica
    fig, ax = plt.subplots(figsize=(8, 6))
    # grafica los tiempos de ambas funciones
    ax.plot(tamanios_entrada, tiempos_prog_din, marker='o', label='Programación Dinámica', color='blue')
    ax.plot(tamanios_entrada, tiempos_fuerza_bruta, marker='o', label='Fuerza Bruta', color='red')
    ax.set_xlabel('Tamaño de la lista')
    ax.set_ylabel('Tiempo (ms)')
    ax.set_title('Comparación de Tiempos de Permutaciones')
    ax.legend()
    ax.grid(True)
    # Agrega la gráfica al frame de Tkinter
    canvas=FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    # activa el botón para permitir nuevas comparaciones
    ventana_finalizado()

# Función para mostrar una ventana de espera
def ventana_espera():
    global espera_ventana
    espera_ventana = tk.Toplevel(root)
    espera_ventana.title("Procesando...")
    espera_ventana.geometry("200x100")
    etiqueta_espera = tk.Label(espera_ventana, text="Por favor, espere...")
    etiqueta_espera.pack(pady=20)
# Función para mostrar una ventana de finalización
def ventana_finalizado():
    global espera_ventana
    if espera_ventana is not None:
        espera_ventana.destroy()
    finalizado_ventana = tk.Toplevel(root)
    finalizado_ventana.title("Finalizado")
    finalizado_ventana.geometry("200x100")
    etiqueta_finalizado = tk.Label(finalizado_ventana, text="¡Proceso finalizado!")
    etiqueta_finalizado.pack(pady=20)
# Función para cerrar la ventana correctamente
def cerrar_ventana():
    # Detener el bucle principal de Tkinter y cerrar la ventana
    root.quit()
    root.destroy()
    
if __name__=="__main__":
    # Configuración de la ventana principal de Tkinter
    root = tk.Tk()
    root.title("Comparacion Complejidad temporal Permutaciones")
    root.geometry("500x200")
    label = tk.Label(root, text="Comparación de Permutaciones")
    label.pack(pady=10)
    canvas_frame = tk.Frame(root)
    tamanio_entrada =tk.Entry(root, width=20, font=("Arial", 14),justify="center", textvariable=tk.StringVar(value="3"))
    tamanio_entrada.pack(pady=5)
    label_generar = tk.Label(root, text="Generar lista de tamaño seleccionado")
    label_generar.pack(pady=5)
    boton_permutas = tk.Button(root, text="Generar Permutaciones", command=lambda: comparacion_permutas(int(tamanio_entrada.get())))
    boton_permutas.pack(pady=20)
    canvas_frame.pack()
    # Configura la acción al cerrar la ventana
    root.protocol("WM_DELETE_WINDOW",cerrar_ventana)
    root.mainloop()
    
    
    
    
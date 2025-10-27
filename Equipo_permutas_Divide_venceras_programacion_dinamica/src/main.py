import time
import random
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tracemalloc
# Listas globales para almacenar los tiempos y tamaños de entrada
tiempos_prog_din=[0]
tiempos_fuerza_bruta=[0]
tiempos_divide_venceras=[0]
espacio_memoria_prog_din=[0]
espacio_memoria_fuerza_bruta=[0]
espacio_memoria_divide_venceras=[0]
# Tamaños separados para cada algoritmo (para poder graficar con ejes X distintos)
tamanios_prog_din=[0]
tamanios_fuerza_bruta=[0]
tamanios_divide_venceras=[0]
espera_ventana=None

def permutas_divide_venceras(lista):
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
        permutaciones_del_resto = permutas_divide_venceras(resto_de_la_lista)
        # Iterar sobre las permutaciones de la sub-lista
        for p in permutaciones_del_resto:
            # Añadir el elemento actual al inicio de cada permutación del resto
            nueva_permutacion = [elemento_actual] + p
            permutas_totales.append(nueva_permutacion)
    return permutas_totales

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

#Funcion para medir el espacio de memoria utilizado por una función
def medir_espacio_memoria(funcion,lista):
    #Inicia el seguimiento de memoria
    tracemalloc.start()
    #Llama a la función que se desea medir
    resultado = funcion(lista)
    #Obtiene el uso de memoria actual y el pico de uso de memoria
    current, peak = tracemalloc.get_traced_memory()
    #Detiene el seguimiento de memoria
    tracemalloc.stop()
    #Retorna el resultado y el pico de uso de memoria en bytes
    return resultado, peak/1024  # Convertir a KB

#Función para medir el tiempo de ejecución de una función
def medir_tiempo(funcion,lista):
    #Empieza el conteo de tiempo
    inicio = time.perf_counter()
    resultado, peak = medir_espacio_memoria(funcion, lista)
    #Termina el conteo de tiempo
    fin = time.perf_counter()
    #Calcula el tiempo en milisegundos
    tiempo_ms = (fin - inicio) * 1000
    #retorna el resultado y el tiempo en milisegundos
    return resultado, tiempo_ms, peak

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

def medir_prog_din(tamanio):
    # Mide sólo la función de programación dinámica y agrega sus datos
    global tiempos_prog_din, espacio_memoria_prog_din, tamanios_prog_din
    ventana_espera()
    lista = generar_lista(tamanio)
    resultado, tiempo, peak = medir_tiempo(permutas, lista)
    tiempos_prog_din.append(tiempo)
    espacio_memoria_prog_din.append(peak)
    tamanios_prog_din.append(tamanio)
    root.geometry("700x600")
    graficar_tiempos()
    graficar_memoria()
    return resultado

def medir_fuerza_bruta(tamanio):
    # Mide sólo la función de fuerza bruta y agrega sus datos
    global tiempos_fuerza_bruta, espacio_memoria_fuerza_bruta, tamanios_fuerza_bruta
    ventana_espera()
    lista = generar_lista(tamanio)
    resultado, tiempo, peak = medir_tiempo(generador_permutas_fuerza_bruta, lista)
    tiempos_fuerza_bruta.append(tiempo)
    espacio_memoria_fuerza_bruta.append(peak)
    tamanios_fuerza_bruta.append(tamanio)
    root.geometry("700x600")
    graficar_tiempos()
    graficar_memoria()
    return resultado


def medir_divide_venceras(tamanio):
    # Wrapper mínimo para medir la función divide y vencerás (no se modifica la función original)
    global tiempos_divide_venceras, espacio_memoria_divide_venceras, tamanios_divide_venceras
    ventana_espera()
    lista = generar_lista(tamanio)
    resultado, tiempo, peak = medir_tiempo(permutas_divide_venceras, lista)
    tiempos_divide_venceras.append(tiempo)
    espacio_memoria_divide_venceras.append(peak)
    tamanios_divide_venceras.append(tamanio)
    root.geometry("700x600")
    graficar_tiempos()
    graficar_memoria()
    return resultado


def mostrar_permutas_desde_lista(permutaciones, titulo):
    """Abre una ventana con un Listbox y muestra las permutaciones (lista de listas)."""
    # Cerrar ventana de espera si está abierta
    global espera_ventana
    if espera_ventana is not None:
        try:
            espera_ventana.destroy()
        except Exception:
            pass
        espera_ventana = None

    win = tk.Toplevel(root)
    win.title(titulo)
    win.geometry("600x400")

    # Mensaje integrado de finalizado
    etiqueta_finalizado = tk.Label(win, text="¡Proceso finalizado!", fg='green')
    etiqueta_finalizado.pack(pady=5)

    frame = tk.Frame(win)
    frame.pack(fill='both', expand=True)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side='right', fill='y')

    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
    listbox.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=listbox.yview)

    # Insertar permutaciones
    for p in permutaciones:
        listbox.insert('end', str(p))


def medir_y_mostrar_prog_din(tamanio):
    # Mide con Divide y Vencerás y muestra las permutaciones en una listbox
    # Protección por tamaño
    if tamanio >= 9:
        if not messagebox.askyesno('Advertencia', f'Mostrar {tamanio}! permutaciones puede ser muy pesado. ¿Deseas continuar?'):
            return
    perms = medir_prog_din(tamanio)
    mostrar_permutas_desde_lista(perms, f'Permutaciones - Divide y Vencerás (n={tamanio})')


def medir_y_mostrar_fuerza(tamanio):
    # Mide con Fuerza Bruta y muestra las permutaciones en una listbox
    if tamanio >= 9:
        if not messagebox.askyesno('Advertencia', f'Mostrar {tamanio}! permutaciones puede ser muy pesado. ¿Deseas continuar?'):
            return
    perms = medir_fuerza_bruta(tamanio)
    mostrar_permutas_desde_lista(perms, f'Permutaciones - Fuerza Bruta (n={tamanio})')


def medir_y_mostrar_divide(tamanio):
    # Mide con Divide y Vencerás y muestra las permutaciones en una listbox
    if tamanio >= 9:
        if not messagebox.askyesno('Advertencia', f'Mostrar {tamanio}! permutaciones puede ser muy pesado. ¿Deseas continuar?'):
            return
    perms = medir_divide_venceras(tamanio)
    mostrar_permutas_desde_lista(perms, f'Permutaciones - Divide y Vencerás (n={tamanio})')

# Función para graficar los resultados
def graficar_tiempos():
    # se mencionan las variables globales
    global tiempos_prog_din
    global tiempos_fuerza_bruta
    global tiempos_divide_venceras
    for widget in canvas_frame_tiempo.winfo_children():
        widget.destroy()
    # Crea la figura y los ejes para la gráfica
    fig, ax = plt.subplots(figsize=(8, 6))
    # grafica los tiempos de ambas funciones (cada una con su propio eje X / tamaños)
    if len(tamanios_prog_din) > 0 and len(tiempos_prog_din) > 0:
        ax.plot(tamanios_prog_din, tiempos_prog_din, marker='o', label='Programación Dinámica', color='blue')
    if len(tamanios_fuerza_bruta) > 0 and len(tiempos_fuerza_bruta) > 0:
        ax.plot(tamanios_fuerza_bruta, tiempos_fuerza_bruta, marker='o', label='Fuerza Bruta', color='red')
    if len(tamanios_divide_venceras) > 0 and len(tiempos_divide_venceras) > 0:
        ax.plot(tamanios_divide_venceras, tiempos_divide_venceras, marker='o', label='Divide y Vencerás', color='green')
    ax.set_xlabel('Tamaño de la lista')
    ax.set_ylabel('Tiempo (ms)')
    ax.set_title('Comparación de Tiempos de Permutaciones')
    ax.legend()
    ax.grid(True)
    # Agrega la gráfica al frame de Tkinter
    canvas=FigureCanvasTkAgg(fig, master=canvas_frame_tiempo)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Función para graficar los resultados
def graficar_memoria():
    # se mencionan las variables globales
    global espacio_memoria_prog_din
    global espacio_memoria_fuerza_bruta
    global espacio_memoria_divide_venceras
    for widget in canvas_frame_memoria.winfo_children():
        widget.destroy()
    # Crea la figura y los ejes para la gráfica
    fig, ax = plt.subplots(figsize=(8, 6))
    # grafica los tiempos de ambas funciones (cada una con su propio eje X / tamaños)
    if len(tamanios_prog_din) > 0 and len(espacio_memoria_prog_din) > 0:
        ax.plot(tamanios_prog_din, espacio_memoria_prog_din, marker='o', label='Programación Dinámica', color='blue')
    if len(tamanios_fuerza_bruta) > 0 and len(espacio_memoria_fuerza_bruta) > 0:
        ax.plot(tamanios_fuerza_bruta, espacio_memoria_fuerza_bruta, marker='o', label='Fuerza Bruta', color='red')
    if len(tamanios_divide_venceras) > 0 and len(espacio_memoria_divide_venceras) > 0:
        ax.plot(tamanios_divide_venceras, espacio_memoria_divide_venceras, marker='o', label='Divide y Vencerás', color='green')
    ax.set_xlabel('Tamaño de la lista')
    ax.set_ylabel('Memoria (KB)')
    ax.set_title('Comparación de Memoria de Permutaciones')
    ax.legend()
    ax.grid(True)
    # Agrega la gráfica al frame de Tkinter
    canvas=FigureCanvasTkAgg(fig, master=canvas_frame_memoria)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Función para mostrar una ventana de espera
def ventana_espera():
    global espera_ventana
    espera_ventana = tk.Toplevel(root)
    espera_ventana.title("Procesando...")
    espera_ventana.geometry("200x100")
    etiqueta_espera = tk.Label(espera_ventana, text="Por favor, espere...")
    etiqueta_espera.pack(pady=20)
    
# Función para cerrar la ventana correctamente
def cerrar_ventana():
    # Detener el bucle principal de Tkinter y cerrar la ventana
    root.quit()
    root.destroy()
    
if __name__=="__main__":
    # Configuración de la ventana principal de Tkinter
    root = tk.Tk()
    root.title("Comparacion Complejidad temporal Permutaciones")
    root.geometry("900x500")
    label = tk.Label(root, text="Comparación de Permutaciones")
    label.pack(pady=10)
    
    # Entrada única para tamaño
    label_tamanio = tk.Label(root, text="Tamaño de la lista")
    label_tamanio.pack(pady=5)
    tamanio_entry = tk.Entry(root, width=20, font=("Arial", 14), justify="center", textvariable=tk.StringVar(value="3"))
    tamanio_entry.pack(pady=5)

    # Botones: Programación Dinámica, Divide y Vencerás y Fuerza Bruta
    boton_prog_dyn = tk.Button(root, text="Programación Dinámica", command=lambda: medir_y_mostrar_prog_din(int(tamanio_entry.get())))
    boton_prog_dyn.pack(pady=5)
    boton_divide = tk.Button(root, text="Divide y Vencerás", command=lambda: medir_y_mostrar_divide(int(tamanio_entry.get())))
    boton_divide.pack(pady=5)
    boton_fb = tk.Button(root, text="Fuerza Bruta", command=lambda: medir_y_mostrar_fuerza(int(tamanio_entry.get())))
    boton_fb.pack(pady=5)

    frame_left = tk.Frame(root)
    frame_left.pack(side='left', fill='both', expand=True)
    frame_right = tk.Frame(root)
    frame_right.pack(side='right', fill='both', expand=True)
    canvas_frame_tiempo = tk.Frame(frame_left)
    canvas_frame_memoria = tk.Frame(frame_right)
    canvas_frame_tiempo.pack()
    canvas_frame_memoria.pack()
    # Configura la acción al cerrar la ventana
    root.protocol("WM_DELETE_WINDOW",cerrar_ventana)
    root.mainloop()
    
    
    
    
import numpy as np
import tkinter as tk
from tkinter import ttk
import time
import tracemalloc

#Variables globales
ciudades = 0
caminos = 0
origen = 0
MatAdy = None
mejor_peso = float("inf")
mejor_ruta = []

#Funciones
def factorial(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado

def LeerCiudades():
    global ciudades, MatAdy
    ciudades = int(entry_ciudades.get())
    #Crea una matriz de adyacencia inicializada en ceros
    MatAdy = np.zeros((ciudades, ciudades), dtype=int)
    ActualizarMatriz()

def AgregarCamino():
    global MatAdy
    origen = int(entry_origen_camino.get())
    destino = int(entry_destino_camino.get())
    distancia = int(entry_distancia.get())
    MatAdy[origen-1, destino-1] = distancia
    MatAdy[destino-1, origen-1] = distancia
    ActualizarMatriz()

def ActualizarMatriz():
    text_matriz.delete("1.0", tk.END)
    text_matriz.insert(tk.END, str(MatAdy))

def LeerOrigen():
    global origen
    origen = int(entry_origen.get())

def BuscarRutas():
    global mejor_respuesta, mejor_peso, ciudades, origen
    #Variables internas
    pruebas = 0
    valor_uno = 0
    valor_dos = 0
    pruebas_total = factorial(ciudades)

    #Incializacion de variables de analisis
    tracemalloc.start()
    inicio = time.time()

    while(pruebas < pruebas_total):
        pruebas = pruebas + 1
        text_iteracion.config(text=f"Iteraciones: {pruebas}")
        ruta = []
        disponibles = list(range(1, ciudades + 1))
        disponibles.remove(origen)
        ruta.append(origen)
        sub_origen = origen
        respuesta_parcial = 0

        #Explora una ruta de origen hasta la ultima ciudad
        while(len(disponibles) != 0):
            #Selecciona una ciudad al azar
            siguiente_ciudad = np.random.choice(disponibles)
            siguiente_ciudad = int(siguiente_ciudad)
            valor_uno = MatAdy[siguiente_ciudad - 1, sub_origen - 1]
            valor_dos = MatAdy[sub_origen - 1, siguiente_ciudad - 1]
            #Comprobamos que no este en la ruta actual
            if siguiente_ciudad not in ruta:
                if((valor_uno != 0) and (valor_dos != 0)):
                    if (valor_uno < valor_dos):
                        ruta.append(siguiente_ciudad)
                        sub_origen =  siguiente_ciudad
                        #ciudades_visitadas = ciudades_visitadas + 1
                        respuesta_parcial = respuesta_parcial + valor_uno
                    else:
                        ruta.append(siguiente_ciudad)
                        sub_origen =  siguiente_ciudad
                        #ciudades_visitadas = ciudades_visitadas + 1
                        respuesta_parcial = respuesta_parcial + valor_dos
                elif(valor_uno != 0):
                    ruta.append(siguiente_ciudad)
                    sub_origen =  siguiente_ciudad
                    #ciudades_visitadas = ciudades_visitadas + 1
                    respuesta_parcial = respuesta_parcial + valor_uno
                elif(valor_dos != 0):
                    ruta.append(siguiente_ciudad)
                    sub_origen =  siguiente_ciudad
                    #ciudades_visitadas = ciudades_visitadas + 1
                    respuesta_parcial = respuesta_parcial + valor_dos
                disponibles.remove(siguiente_ciudad)

                text_pruebas.insert(tk.END, f" Ruta actual: {ruta} Peso actual: {respuesta_parcial}")
        
        #Revisa que se hayan recorrido todas las ciudades
        if(len(ruta) == ciudades):
            ruta.append(origen)
            valor_uno = MatAdy[sub_origen - 1, origen - 1]
            valor_dos = MatAdy[origen - 1, sub_origen - 1]
            #Comprobar que se puede cerrar el recorrido con la ciudad de origen
            if ((valor_uno != 0) and (valor_dos != 0)):
                if (valor_uno < valor_dos):
                    respuesta_parcial = respuesta_parcial + valor_uno
                else:
                    respuesta_parcial = respuesta_parcial + valor_dos
            elif(valor_uno != 0):
                respuesta_parcial = respuesta_parcial + valor_uno
            elif(valor_dos != 0):
                respuesta_parcial = respuesta_parcial + valor_dos
                    
            if((valor_uno != 0) or (valor_dos != 0)):
                respuesta_parcial = int(respuesta_parcial)
                if (respuesta_parcial < mejor_peso):
                    mejor_peso = respuesta_parcial
                    mejor_ruta = ruta
                    label_mejor.config(text=f"Nueva mejor ruta: {mejor_ruta} Peso: {mejor_peso}") 
            else:
                text_pruebas.insert(tk.END, f" Ruta descartada: {ruta}")
        else:
            text_pruebas.insert(tk.END, f" Ruta descartada: {ruta}")

    #Finalizacion de variables de analisis
    fin = time.time()
    tiempo_total = fin - inicio
    memoria_actual, memoria_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    #Mostrar resultados en GUI
    label_tiempo.config(text=f"Tiempo total: {tiempo_total:.4f} segundos")
    label_memoria.config(text=f"Memoria usada: {memoria_actual/1024:.2f} KB | Máxima: {memoria_max/1024:.2f} KB")


#GUI
root = tk.Tk()
root.title("TSP por Angel Rodriguez")

#Panel de entradas
frame_inputs = ttk.LabelFrame(root, text="Entradas")
frame_inputs.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

ttk.Label(frame_inputs, text="Numero de ciudades: ").grid(row=0, column=0)
entry_ciudades = ttk.Entry(frame_inputs)
entry_ciudades.grid(row=0, column=1)
ttk.Button(frame_inputs, text="Inicializar", command=LeerCiudades).grid(row=0, column=2)

ttk.Label(frame_inputs, text="Origen:").grid(row=1, column=0)
entry_origen = ttk.Entry(frame_inputs)
entry_origen.grid(row=1, column=1)
ttk.Button(frame_inputs, text="Set Origen", command=LeerOrigen).grid(row=1, column=2)

ttk.Label(frame_inputs, text="Camino (origen, destino, distancia): ").grid(row=2, column=0)
entry_origen_camino = ttk.Entry(frame_inputs, width=5)
entry_origen_camino.grid(row=2, column=1)
entry_destino_camino = ttk.Entry(frame_inputs, width=5)
entry_destino_camino.grid(row=2, column=2)
entry_distancia = ttk.Entry(frame_inputs, width=5)
entry_distancia.grid(row=2, column=3)
ttk.Button(frame_inputs, text="Agregar camino", command=AgregarCamino).grid(row=2, column=4)

#Panel matriz
frame_matriz = ttk.LabelFrame(root, text="Matriz de Adyacencia")
frame_matriz.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
text_matriz = tk.Text(frame_matriz, width=40, height=10)
text_matriz.pack()

#Panel pruebas
frame_pruebas = ttk.LabelFrame(root, text="Pruebas en ejecución")
frame_pruebas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
text_iteracion = ttk.Label(frame_pruebas, text="Iteracion: -")
text_iteracion.pack()
text_pruebas = tk.Text(frame_pruebas, width=60, height=10)
text_pruebas.pack()

#Panel mejor respuesta
frame_mejor = ttk.LabelFrame(root, text="Mejor respuesta")
frame_mejor.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
label_mejor = ttk.Label(frame_mejor, text="Mejor ruta: Ninguna aún")
label_mejor.pack()

#Panel de analisis
frame_metricas = ttk.LabelFrame(root, text="Métricas de ejecución")
frame_metricas.grid(row=2, column=0, columnspan=2, padx=10, pady=40, sticky="nsew")
label_tiempo = ttk.Label(frame_metricas, text="Tiempo total: -")
label_tiempo.pack()
label_memoria = ttk.Label(frame_metricas, text="Memoria usada: -")
label_memoria.pack()

#Botón ejecutar
ttk.Button(root, text="Buscar rutas", command=BuscarRutas).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
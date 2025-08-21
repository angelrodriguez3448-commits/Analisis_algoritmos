import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

listaGlo = []
tiempos = {
    "lineal": {100: [], 1000: [], 10000: [], 100000: []},
    "binaria": {100: [], 1000: [], 10000: [], 100000: []}
}

def actualizar_grafica():
    fig.clear()
    ax = fig.add_subplot(111)

    tipos = ["lineal", "binaria"]
    colores = {"lineal": "#FF6500", "binaria": "#000B58"}
    tamannos = [100, 1000, 10000, 100000]
    
    for tipo in tipos:
        promedios = []
        for tam in tamannos:
            if len(tiempos[tipo][tam]) >= 5:
                prom = sum(tiempos[tipo][tam]) / len(tiempos[tipo][tam])
                promedios.append(prom)
            else:
                promedios.append(0)
                #ax.text(0.5, 1, "Esperando al menos 5 ejecuciones de cada combinacion", ha="center", va="center", transform=ax.transAxes)
        ax.plot(tamannos, promedios, marker="o", label=tipo, color=colores[tipo])

    ax.set_title("Promedio de tiempos de busqueda")
    ax.set_xlabel("Tamaño de lista")
    ax.set_ylabel("Tiempo (milisegundos)")
    ax.legend()
    ax.grid(True)
    canvas.draw()

def generador_lista():
    global listaGlo
    longitud = seleccion.get()
    listaGlo = np.random.randint(0, 10000, size=longitud).tolist()
    
def busqueda_lineal():
    tiempoIni = time.perf_counter()
    global listaGlo
    longitud = len(listaGlo)
    if not listaGlo:
        resultados.config(text="Primera genera una lista", bg="#9AA6B2")
        return
    if not entrada.get():
        resultados.config(text="Ingresa un valor", bg="#9AA6B2")
        return
    numBus = int(entrada.get())
    indice = 0
    for indice, numAux in enumerate(listaGlo):
        if numAux == numBus:
            tiempoFin = time.perf_counter()
            tiempoTot = (tiempoFin - tiempoIni) * 1000
            tiempos["lineal"][longitud].append(tiempoTot)
            resultados.config(text=f"Tamaño de lista{longitud}\nEl numero esta en el indice {indice}\nTiempo de ejecucion (ms) {tiempoTot}", bg="#9AA6B2")
            actualizar_grafica()
            return
        indice = indice + 1
    tiempoFin = time.perf_counter()
    tiempoTot = (tiempoFin - tiempoIni) * 1000
    tiempos["lineal"][longitud].append(tiempoTot)
    resultados.config(text=f"Tamaño de lista{longitud}\nEl numero no fue encontrado\nTiempo de ejecucion (ms) {tiempoTot}", bg="#9AA6B2")
    actualizar_grafica()
    return

def busqueda_binaria():
    tiempoIni = time.perf_counter()
    global listaGlo
    longitud = len(listaGlo)
    if not listaGlo:
        resultados.config(text="Primera genera una lista", bg="#9AA6B2")
        return
    if not entrada.get():
        resultados.config(text="Ingresa un valor", bg="#9AA6B2")
        return
    listaGlo.sort()
    limiteIzq = 0
    limiteDer = len(listaGlo) - 1
    medio = len(listaGlo) // 2
    numBus = int(entrada.get())
    while limiteIzq < limiteDer:
        if listaGlo[medio] == numBus:
            tiempoFin = time.perf_counter()
            tiempoTot = (tiempoFin - tiempoIni) * 1000
            tiempos["binaria"][longitud].append(tiempoTot)
            resultados.config(text=f"Tamaño de lista{longitud}\nEl numero esta en el indice {medio}\nTiempo de ejecucion (ms) {tiempoTot}", bg="#9AA6B2")
            actualizar_grafica()
            return
        elif numBus < listaGlo[medio]:
            limiteDer = medio - 1
        else:
            limiteIzq = medio + 1
        medio = (limiteIzq + limiteDer) // 2
    tiempoFin = time.perf_counter()
    tiempoTot = (tiempoFin - tiempoIni) * 1000
    tiempos["binaria"][longitud].append(tiempoTot)
    resultados.config(text=f"Tamaño de lista{longitud}\nEl numero no fue encontrado\nTiempo de ejecucion (ms) {tiempoTot}", bg="#9AA6B2")
    actualizar_grafica()
    return
    
ventaIni = tk.Tk()
ventaIni.title("GUI de busqueda")
ventaIni.geometry("1200x900")
ventaIni.config(background='#D9EAFD')
ventaIni.grid_columnconfigure(0, weight=1)
ventaIni.grid_columnconfigure(1, weight=3)

# --- Definir frames ---
frame_left = tk.Frame(ventaIni, bg="#D9EAFD")
frame_right = tk.Frame(ventaIni, bg="#D9EAFD")

frame_left.grid(row=0, column=0, sticky="nswe", padx=10, pady=5)
frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

# Hacer que se expandan al redimensionar
ventaIni.grid_columnconfigure(0, weight=1)
ventaIni.grid_columnconfigure(1, weight=3)
ventaIni.grid_rowconfigure(0, weight=1)

encabezado = tk.Label(frame_left, text="Programa de busqueda con GUI", fg='#1E3E62', bg="#D9EAFD", font=("Helvetica", 16, "bold"))
encabezado.pack(padx=10, pady=10)

tituloSec = tk.Label(frame_left, text="Generador de datos\nEliga una tamaño para la lista", fg='#1E3E62', bg="#D9EAFD", font=("Helvetica", 12))
tituloSec.pack(padx=5, pady=5)

seleccion = tk.IntVar(value=100)

radioBoton1 = tk.Radiobutton(frame_left, text="100 datos", width=15, cursor="hand2", variable=seleccion, value=100)
radioBoton2 = tk.Radiobutton(frame_left, text="1000 datos", width=15, cursor="hand2", variable=seleccion, value=1000)
radioBoton3 = tk.Radiobutton(frame_left, text="10 000 datos", width=15, cursor="hand2", variable=seleccion, value=10000)
radioBoton4 = tk.Radiobutton(frame_left, text="100 000 datos", width=15, cursor="hand2", variable=seleccion, value=100000)
radioBoton1.pack()
radioBoton2.pack()
radioBoton3.pack()
radioBoton4.pack()


botonGen = tk.Button(frame_left, text="Generar datos", width=19, command=generador_lista, fg="#000000", bg="#9AA6B2")
botonGen.pack(padx=2, pady=2)

tituloSec = tk.Label(frame_left, text="Ingrese un valor numerico entero\nSeleccione el tipo de busqueda", fg='#1E3E62', bg="#D9EAFD", font=("Helvetica", 12))
tituloSec.pack(padx=5, pady=5)

entrada = tk.Entry(frame_left)
entrada.pack(padx=2, pady=2)

botonBusL = tk.Button(frame_left, text="Busqueda lineal", width=19, command=busqueda_lineal, fg="#000000", bg="#9AA6B2")
botonBusL.pack()

botonBusBin = tk.Button(frame_left, text="Busdueda binaria", width=19, command=busqueda_binaria, fg="#000000", bg="#9AA6B2")
botonBusBin.pack()

resultados = tk.Label(frame_left, text="", bg="#D9EAFD")
resultados.pack(padx=2, pady=2)

fig = Figure(figsize=(7, 6), dpi=95)
canvas = FigureCanvasTkAgg(fig, master=frame_right)
canvas.get_tk_widget().pack()

ventaIni.mainloop()
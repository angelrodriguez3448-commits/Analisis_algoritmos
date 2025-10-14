import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#import time

listaGloY = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

def actualizar_grafica():
    fig.clear()
    ax = fig.add_subplot(111)

    tipos = ["#", "##"]
    colores = {"#": "#FF6500", "##": "#000B58"}
    X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    for tipo in tipos:
        """"
        promedios = []
        for tam in tamannos:
            if len(tiempos[tipo][tam]) >= 5:
                prom = sum(tiempos[tipo][tam]) / len(tiempos[tipo][tam])
                promedios.append(prom)
            else:
                promedios.append(0)
        """
        ax.plot(X, listaGloY, marker="o", label=tipo, color=colores[tipo])

    ax.set_title("Grafica")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    ax.grid(True)
    canvas.draw()

ventaIni = tk.Tk()
ventaIni.title("GUI de busqueda")
ventaIni.geometry("1200x900")
ventaIni.config(background='#D9EAFD')

botonAct = tk.Button(ventaIni, text="Actualizar grafica", command=actualizar_grafica)
botonAct.pack()

fig = Figure(figsize=(7, 6), dpi=95)
canvas = FigureCanvasTkAgg(fig, master=ventaIni)
canvas.get_tk_widget().pack()
ventaIni.mainloop()

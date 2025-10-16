import sys
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import tracemalloc

# Diccionarios para almacenar tiempos y espacios
tiempos = {
    "fibonacci_nd": {},
    "fibonacci_d": {}
}
espacios = {
    "fibonacci_nd": {},
    "fibonacci_d": {}
}

# Funciones para actualizar graficas
def actualizar_grafica_tiempo():
    fig.clear()
    ax = fig.add_subplot(111)

    tipos = ["fibonacci_nd", "fibonacci_d"]
    colores = {"fibonacci_nd": "#FF6500", "fibonacci_d": "#000B58"}

    for tipo in tipos:
        ax.plot(tiempos[tipo].keys(), tiempos[tipo].values(), marker="o", label=tipo, color=colores[tipo])

    ax.set_title("Grafica")
    ax.set_xlabel("n_fibonacci")
    ax.set_ylabel("milisegundos")
    ax.legend()
    ax.grid(True)
    canvas.draw()

def actualizar_grafica_espacio():
    fig.clear()
    ax = fig.add_subplot(111)

    tipos = ["fibonacci_nd", "fibonacci_d"]
    colores = {"fibonacci_nd": "#FF6500", "fibonacci_d": "#000B58"}

    for tipo in tipos:
        ax.plot(espacios[tipo].keys(), espacios[tipo].values(), marker="o", label=tipo, color=colores[tipo])

    ax.set_title("Grafica")
    ax.set_xlabel("n_fibonacci")
    ax.set_ylabel("bytes")
    ax.legend()
    ax.grid(True)
    canvas.draw()

# Funciones para calcular Fibonacci y medir tiempos y espacios
def calcular_fibonacci(n):
    if n <= 1:
        return n
    return calcular_fibonacci(n - 1) + calcular_fibonacci(n - 2)

def calcular_fibonacci_d(n):
    dp = [0, 1]
    if n > 2:
        for i in range(2, n):
            dp.append(dp[i-1] + dp[i-2])
    return dp[n-1]

def medir_fibonacci(n):
    
    espacios["fibonacci_nd"][n] = sys.getsizeof(n) * n

    dp = [0, 1]
    for i in range(2, n):
        dp.append(dp[i-1] + dp[i-2])
    espacios["fibonacci_d"][n] = sum(sys.getsizeof(x) for x in dp) + sys.getsizeof(dp)

def comparar_tiempos():
    n_fibo = int(entrada.get())
    
    tiempoIni = time.perf_counter()
    calcular_fibonacci(n_fibo)
    tiempoFin = time.perf_counter()
    tiempos["fibonacci_nd"][n_fibo] = (tiempoFin - tiempoIni) * 1000  # Convertir a milisegundos

    tiempoIni = time.perf_counter()
    calcular_fibonacci_d(n_fibo)
    tiempoFin = time.perf_counter()
    tiempos["fibonacci_d"][n_fibo] = (tiempoFin - tiempoIni) * 1000  # Convertir a milisegundos

    resultado.config(text=f"Tiempo Fibonacci no dinamico: {tiempos['fibonacci_nd'][n_fibo]:.4f} ms\nTiempo Fibonacci dinamico: {tiempos['fibonacci_d'][n_fibo]:.4f} ms", bg="#9AA6B2")

    actualizar_grafica_tiempo()

def comparar_espacios():
    n_fibo = int(entrada.get())
    medir_fibonacci(n_fibo)
    
    resultado.config(text=f"Espacio Fibonacci no dinamico: {espacios['fibonacci_nd'][n_fibo]} bytes\nEspacio Fibonacci dinamico: {espacios['fibonacci_d'][n_fibo]} bytes", bg="#9AA6B2")

    actualizar_grafica_espacio()

# Configuracion de la ventana principal
ventaIni = tk.Tk()
ventaIni.title("GUI de Fibonacci")
ventaIni.geometry("1200x900")
ventaIni.config(background='#D9EAFD')
ventaIni.grid_columnconfigure(0, weight=1)
ventaIni.grid_columnconfigure(1, weight=3)

# Definir frames
frame_left = tk.Frame(ventaIni, bg="#D9EAFD")
frame_right = tk.Frame(ventaIni, bg="#D9EAFD")

frame_left.grid(row=0, column=0, sticky="nswe", padx=10, pady=5)
frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

# Hacer que se expandan al redimensionar
ventaIni.grid_columnconfigure(0, weight=1)
ventaIni.grid_columnconfigure(1, weight=3)
ventaIni.grid_rowconfigure(0, weight=1)

# Frame left para widgets
encabezado = tk.Label(frame_left, text="Programa de comparacion \nFibonacci no dinamico VS dinamico", fg='#1E3E62', bg="#D9EAFD", font=("Helvetica", 16, "bold"))
encabezado.pack(padx=10, pady=10)

tituloSec = tk.Label(frame_left, text="Ingrese el numero de Fibonacci a calcular:", fg='#1E3E62', bg="#D9EAFD", font=("Helvetica", 12))
tituloSec.pack(padx=5, pady=5)

entrada = tk.Entry(frame_left)
entrada.pack(padx=5, pady=5)
resultado = tk.Label(frame_left, text="Resultado", fg='#1E3E62', bg="#9AA6B2", font=("Helvetica", 12))
resultado.pack(padx=5, pady=5)
botonAct = tk.Button(frame_left, text="Comparar tiempo", command=comparar_tiempos)
botonAct.pack(padx=5, pady=5)
botonAct = tk.Button(frame_left, text="Comparar espacio", command=comparar_espacios)
botonAct.pack(padx=5, pady=5)

# Frame right para graficas
fig = Figure(figsize=(7, 6), dpi=95)
canvas = FigureCanvasTkAgg(fig, master=frame_right)
canvas.get_tk_widget().pack()

ventaIni.mainloop()
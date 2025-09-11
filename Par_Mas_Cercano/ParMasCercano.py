#Angel Ariel Rodriguez Arellano
import tkinter as tk
import math
import random
import time

VAL_MIN, VAL_MAX = 1, 40
ListaPuntos = []

def distanciaEcludiana(p1, p2):
    distancia = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    print(distancia)
    return distancia

def generar():
    random.seed(time.time())
    global ListaPuntos
    P1 = [random.randint(VAL_MIN, VAL_MAX) for _ in range(2)]
    P2 = [random.randint(VAL_MIN, VAL_MAX) for _ in range(2)] 
    P3 = [random.randint(VAL_MIN, VAL_MAX) for _ in range(2)]
    P4 = [random.randint(VAL_MIN, VAL_MAX) for _ in range(2)]
    P5 = [random.randint(VAL_MIN, VAL_MAX) for _ in range(2)] 
    ListaPuntos = [P1, P2, P3, P4, P5]
    resultado.config(text="")
    print(ListaPuntos)

def guardarEntradas():
    global ListaPuntos
    
    #Lista para validar
    entradas = [entradaP1X, entradaP1Y,
                entradaP2X, entradaP2Y,
                entradaP3X, entradaP3Y,
                entradaP4X, entradaP4Y,
                entradaP5X, entradaP5Y]
    #lista temporal
    valores = []

    #Validacion de espacios vacios y valores enteros
    for i in entradas:
        texto = i.get().strip()
        if not texto:
            resultado.config(text="Hay campos vacio")
            return
        try:
            valores.append(int(texto))
        except ValueError:
            resultado.config(text=f"Hay un valor invalido: {texto}")
            return
        
    P1 = valores[0:2]
    P2 = valores[2:4]
    P3 = valores[4:6]
    P4 = valores[6:8]
    P5 = valores[8:10]
    ListaPuntos = [P1, P2, P3, P4, P5]
    print(ListaPuntos)

def calcula():
    global ListaPuntos
    if not ListaPuntos:
        guardarEntradas()
    else:
        distanciaMenor = distanciaEcludiana(ListaPuntos[0], ListaPuntos[1])
        P1 = ListaPuntos[0]
        P2 = ListaPuntos[1]
        for i in range(5):
            for j in range(5):
                if i != j:
                    distanciaActual = distanciaEcludiana(ListaPuntos[i], ListaPuntos[j])
                    if distanciaActual < distanciaMenor:
                        distanciaMenor = distanciaActual
                        P1 = ListaPuntos[i]
                        P2 = ListaPuntos[j]
        resultado.config(text=f"El par mas cercano son los puntos {P1} y {P2} con una distancia de {distanciaMenor}")

def limpia():
    global ListaPuntos
    ListaPuntos = []
    resultado.config(text="")

root = tk.Tk()
root.title("Par mas cercano")
root.geometry("400x400")

textCordenadaX = tk.Label(root, text="X")
textCordenadaX.grid(column=1, row=0)
textCordenadaY = tk.Label(root, text="Y")
textCordenadaY.grid(column=2, row=0)

textP1 = tk.Label(root, text="P1")
textP1.grid(column=0, row=1)
entradaP1X = tk.Entry(root)
entradaP1X.grid(column=1, row=1)
entradaP1Y = tk.Entry(root)
entradaP1Y.grid(column=2, row=1)

textP2 = tk.Label(root, text="P2")
textP2.grid(column=0, row=2)
entradaP2X = tk.Entry(root)
entradaP2X.grid(column=1, row=2)
entradaP2Y = tk.Entry(root)
entradaP2Y.grid(column=2, row=2)

textP3 = tk.Label(root, text="P3")
textP3.grid(column=0, row=3)
entradaP3X = tk.Entry(root)
entradaP3X.grid(column=1, row=3)
entradaP3Y = tk.Entry(root)
entradaP3Y.grid(column=2, row=3)

textP4 = tk.Label(root, text="P4")
textP4.grid(column=0, row=4)
entradaP4X = tk.Entry(root)
entradaP4X.grid(column=1, row=4)
entradaP4Y = tk.Entry(root)
entradaP4Y.grid(column=2, row=4)

textP5 = tk.Label(root, text="P5")
textP5.grid(column=0, row=5)
entradaP5X = tk.Entry(root)
entradaP5X.grid(column=1, row=5)
entradaP5Y = tk.Entry(root)
entradaP5Y.grid(column=2, row=5)

calcular = tk.Button(root, text="Calcular", command=calcula)
calcular.grid(column=0, row=6)
llenarRand = tk.Button(root, text="Llenar random", command=generar)
llenarRand.grid(column=1, row=6)
limpiar = tk.Button(root, text="Limpiar", command=limpia)
limpiar.grid(column=2, row=6)

resultado = tk.Label(root, text="")
resultado.grid(column=1, row=7)

root.mainloop()
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import random

base_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(base_dir, "img")

def boton_pulsado():
    text.config(text="Pulsaste el boton")

def piedra_papel_tijeras(opc):
    pc_eleccion = random.randint(1, 3)
    resultado = ""
    if (opc == 1):
        imagen1 = Image.open(os.path.join(img_dir, "Piedra.png"))
        tk_img = ImageTk.PhotoImage(imagen1)
        if (pc_eleccion == 2):
            resultado = "Derrota"
        elif (pc_eleccion == 3):
            resultado = "Victoria"
        else:
            resultado = "Empate"
    elif (opc == 2):
        imagen2 = Image.open(os.path.join(base_dir, "./img/Papel.png"))
        tk_img = ImageTk.PhotoImage(imagen2)
        if (pc_eleccion == 3):
            resultado = "Derrota"
        elif (pc_eleccion == 1):
            resultado = "Victoria"
        else:
            resultado = "Empate"
    elif (opc == 3):
        imagen3 = Image.open(os.path.join(base_dir,"./img/Tijeras.png"))
        tk_img = ImageTk.PhotoImage(imagen3)
        if (pc_eleccion == 1):
            resultado = "Derrota"
        elif (pc_eleccion == 2):
            resultado = "Victoria"
        else:
            resultado = "Empate"
        
    img_juego.config(image= tk_img)
    result_juego.config(text=f"{resultado}")
    img_juego.image = tk_img
    


root = tk.Tk()
root.title("Prueba de ventana TK")

root_ancho = int(root.winfo_screenwidth() / 2)
root_alto = int(root.winfo_screenheight() / 2)

root.geometry(f"{root_ancho}x{root_alto}")

text = ttk.Label(root, text="Esto es un label", background="#FFFFFF")
text.pack()

button = ttk.Button(root, text="Esto es un boton, pulsalo", command=boton_pulsado)
button.pack()

button_piedra = ttk.Button(root, text="Piedra", command=lambda: piedra_papel_tijeras(1))
button_papel = ttk.Button(root, text="Papel", command=lambda: piedra_papel_tijeras(2))
button_tijeras = ttk.Button(root, text="Tijeras", command=lambda: piedra_papel_tijeras(3))
button_piedra.pack()
button_papel.pack()
button_tijeras.pack()
img_juego = ttk.Label(root)
result_juego = ttk.Label(root)
img_juego.pack()
result_juego.pack()

root.mainloop()
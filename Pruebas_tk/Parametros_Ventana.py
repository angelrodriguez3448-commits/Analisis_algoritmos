import tkinter as tk

root = tk.Tk()
root.title("Prueba de ventana TK")

root_ancho = int(root.winfo_screenwidth() / 2)
root_alto = int(root.winfo_screenheight() / 2)

root.geometry(f"{root_ancho}x{root_alto}")

text = tk.Label(root, text="Esto es una venta")
text.pack()

root.mainloop()
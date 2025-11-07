import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import Huffman as huffman
import pickle
from bitstring import BitArray
from bitarray import bitarray

filename = None
contenido = None
contenido_bin = None
diccionario_h = None

def select_file_txt():
    global filename, contenido, filename_label, file_text
    filename = askopenfilename(filetypes=[("Text files", "*.txt")])
    file_label["text"] = filename # Mostrar el nombre del archivo en un label de la GUI
    with open(filename, encoding="utf-8", errors="replace") as file:
        contenido = file.read() # Leer el archivo 
        file_textarea.delete("1.0", tk.END)
        file_textarea.insert(tk.END, contenido)

def select_file_bin():
    global filename, contenido_bin, file_label, diccionario_h
    filename = askopenfilename(filetypes=[("Binary files", "*.bin")])
    if not filename:
        return
    file_label["text"] = filename # Mostrar el nombre del archivo en un label de la GUI
    file_textarea.delete("1.0", tk.END)
    file_textarea.insert(tk.END, "Se a cargado un archivo binario")

    with open(filename, "rb") as file:
        diccionario_h = pickle.load(file) # Recuperar el diccionario
        contenido_bin = bitarray() 
        contenido_bin.fromfile(file) # Leer el archivo binario y guardarlo como un bitarray

def compress_file():
    global filename, contenido

    if filename is None:
        return
    
    # Opcion para aumentar la compresion, siempre y cuando no importe la conversion a minusculas
    # contenido.lower()

    diccionario_h = huffman.huffman_encoding(contenido) # Se genera el diccionario Huffman para la codificacion
    comprimido = huffman.compresion(contenido, diccionario_h) # Se comprime el archivo con el diccionario previamente hecho
    
    savefile = asksaveasfilename(defaultextension=".bin", filetypes=[("Binary files", "*.bin")]) # Configuracion del archivo binario
    if savefile:
        with open(savefile, "wb") as file:
            pickle.dump(diccionario_h, file) # Guardar el diccionario en el archivo binario
            comprimido.tofile(file) # Guardar la cadena binaria en el archivo binario

def descomprimir_archivo():
    global filename, contenido_bin, contenido, diccionario_h

    comprimido = BitArray(bin=contenido_bin.to01()) # Comvertir el bitarray en BitArray, ya que las funciones del modulo huffman trabajan coneste formato
    contenido = huffman.descompresion(comprimido, diccionario_h) # Descomprimir el archivo binario usando el diccionario recuperado del mismo archivo

    savefile = asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")]) # Configuracion del archivo de texto para guardar el contenido descomprimido
    if savefile:
        with open(savefile, "w", encoding="utf-8") as file:
            file.write(f"{contenido}") # Escribir en el archivo de texto creado

root = tk.Tk()
# Botones para cargar archivos
tk.Button(root, text="Selecciona archivo a comprimir (.txt)", command=select_file_txt).pack(pady=5)
tk.Button(root, text="Selecciona archivo a descomprimir (.bin)", command=select_file_bin).pack(pady=5)

# Label para mostrar la direccion y nombre del archivo cargado
file_label = tk.Label(root, text="File name")
file_label.pack(pady=5)

# Label para mostrar el contenido del archivo cargado solo para txt
file_textarea = tk.Text(root, height=12, width=40)
file_textarea.pack(pady=5)

# Botones para comprimir y descomprimir
tk.Button(root, text="Comprimir", command=compress_file).pack(pady=5)
tk.Button(root, text="Descomprimir", command=descomprimir_archivo).pack(pady=5)

root.mainloop()
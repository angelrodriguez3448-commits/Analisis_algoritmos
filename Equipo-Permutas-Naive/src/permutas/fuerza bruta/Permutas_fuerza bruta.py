import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import random
#medidas de las fotos
ANCHO_FOTO=150
ALTO_FOTO=150
#medidas para las fotos pequenas
ANCHO_FOTO_MINIATURA=30
ALTO_FOTO_MINIATURA=30

POSICION_INICIAL=0

NUM_IMAGENES=0
#variable para saber cuando poder invocar 
regreso=False
#lista para las permutas
lista_posiciones = [] 
#guardar las etiquetas
lista_imagenes_etiquetas=[]
#para la ubicacion de las imagenes
lista_imagenes_rutas=[]
#image
lista_imagenes=[]
#image tk
lista_imagenes_tk=[]
# los frames de opciones
lista_frames_opciones=[]

lista_imagenes_etiquetas_principales=[]
permutas = []

def permutas_fuerza_bruta(lista):
    global permutas
    # Caso base: si la lista tiene un solo elemento, es una permutación.
    if len(lista) <= 1:
        return [lista]
    permutas_totales=[]
    # Recorrer cada elemento de la lista
    for i in range(len(lista)):
        # Tomar el elemento actual como pivote
        elemento_actual = lista[i]
        # Crear una sub-lista con los elementos restantes
        resto_de_la_lista = lista[:i] + lista[i+1:]
        # Llamada recursiva para obtener las permutaciones de la sub-lista
        permutaciones_del_resto = permutas_fuerza_bruta(resto_de_la_lista)
        # Iterar sobre las permutaciones de la sub-lista
        for p in permutaciones_del_resto:
            # Añadir el elemento "pivot" al inicio de cada permutación del resto
            nueva_permutacion = [elemento_actual] + p
            permutas_totales.append(nueva_permutacion)
    return permutas_totales

def selecionar_imagen():
    
    global lista_imagenes_etiquetas_principales
    global lista_imagenes
    global lista_imagenes_tk
    global lista_imagenes_rutas
    global lista_posiciones
    global NUM_IMAGENES
    lista_imagenes_rutas.append(filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=(("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif"), ("Todos los archivos", "*.*"))
    ))
    lista_imagenes.append(Image.open(lista_imagenes_rutas[NUM_IMAGENES]))
    lista_imagenes[NUM_IMAGENES]=lista_imagenes[NUM_IMAGENES].resize((ANCHO_FOTO, ALTO_FOTO), Image.LANCZOS)
    lista_imagenes_tk.append(ImageTk.PhotoImage(lista_imagenes[NUM_IMAGENES]))
    lista_imagenes_etiquetas_principales.append(tk.Label(frame_fotos, image=lista_imagenes_tk[NUM_IMAGENES]))
    frame_no_imagenes.pack_forget()
    if NUM_IMAGENES==0:
        lista_imagenes_etiquetas_principales[NUM_IMAGENES].grid(column=[NUM_IMAGENES],row=[NUM_IMAGENES])
        lista_posiciones.append([NUM_IMAGENES,NUM_IMAGENES])
    elif NUM_IMAGENES!=0 and NUM_IMAGENES%2!=0 :
        lista_imagenes_etiquetas_principales[NUM_IMAGENES].grid(column=[NUM_IMAGENES-1],row=[1])
        lista_posiciones.append([NUM_IMAGENES-1,1])
    else:
        lista_imagenes_etiquetas_principales[NUM_IMAGENES].grid(column=[NUM_IMAGENES],row=[0])
        lista_posiciones.append([NUM_IMAGENES,0])
    NUM_IMAGENES=NUM_IMAGENES+1
    boton_permutas.config(state='active')
    
def crear_miniaturas():
    global lista_imagenes_etiquetas
    global lista_frames_opciones
    global NUM_IMAGENES
    for i in range(0,len(lista_frames_opciones)):
        for j in range(NUM_IMAGENES):
            etiqueta=tk.Label(lista_frames_opciones[i], image=lista_imagenes_tk[j], width=ANCHO_FOTO_MINIATURA, height=ALTO_FOTO_MINIATURA)
            lista_imagenes_etiquetas.append(etiqueta)

def generar_posicion_opciones(posicion_inicial):
    global POSICION_INICIAL
    global permutas
    global lista_imagenes_etiquetas
    global lista_frames_opciones
    global lista_imagenes_etiquetas_principales
    global NUM_IMAGENES
    global regreso
    if POSICION_INICIAL ==0:
        lista_frames_opciones[0].grid_forget()
        frame_no_disponible.grid(column=0,row=0, sticky="nsew")
        etiqueta_no_disponible.pack()
        
    else:
        if POSICION_INICIAL==1:
            frame_no_disponible.grid_forget()
            lista_frames_opciones[0].grid(column=0,row=0)
        for i in range (0,NUM_IMAGENES):
            lista_imagenes_etiquetas[i].grid(column=permutas[posicion_inicial-1][i][0],row=permutas[posicion_inicial-1][i][1])
    
    for i in range(0, NUM_IMAGENES):
        lista_imagenes_etiquetas_principales[i].grid(column=permutas[posicion_inicial][i][0],row=permutas[posicion_inicial][i][1])
    j=0   
    for i in range(NUM_IMAGENES,(NUM_IMAGENES*2)):
            
            lista_imagenes_etiquetas[i].grid(column=permutas[posicion_inicial][j][0],row=permutas[posicion_inicial][j][1])
            j=j+1
              

    if POSICION_INICIAL==len(permutas)-1:
        lista_frames_opciones[2].grid_forget()
        frame_no_disponible.grid(column=2,row=0)
        etiqueta_no_disponible.pack()
        regreso=True
        lista_frames_opciones[1].grid(column=1, row=0)
        
    else:
        if regreso!=False and POSICION_INICIAL==(len(permutas)-2):
            frame_no_disponible.grid_forget()
            lista_frames_opciones[2].grid(column=2,row=0)
            regreso=False
        j=0
        for i in range ((NUM_IMAGENES*2),(NUM_IMAGENES*3)):
            lista_imagenes_etiquetas[i].grid(column=permutas[posicion_inicial-1][j][0],row=permutas[posicion_inicial-1][j][1])  
            j=j+1     

def siguiente():
    global POSICION_INICIAL
    if POSICION_INICIAL+1!=len(permutas):
        POSICION_INICIAL=POSICION_INICIAL+1
    generar_posicion_opciones(POSICION_INICIAL-1)
    
def anterior():
    global POSICION_INICIAL
    if POSICION_INICIAL-1>=0:
        POSICION_INICIAL=POSICION_INICIAL-1
    generar_posicion_opciones(POSICION_INICIAL-1)
    
def realizar_permutas():
    global permutas
    global lista_posiciones
    global lista_frames_opciones
    boton_imagen.config(state="disabled")
    boton_permutas.config(state='disabled')
    boton_anterior.grid(column=1, row=0)
    boton_siguiente.grid(column=3, row=0)
    crear_miniaturas()
    permutas=permutas_fuerza_bruta(lista_posiciones)
    label_anterior.grid(column=0,row=0)
    label_siguiente.grid(column=4,row=0)
    lista_frames_opciones[0].grid(column=1, row=0)
    lista_frames_opciones[1].grid(column=2, row=0)
    lista_frames_opciones[2].grid(column=3, row=0)
    generar_posicion_opciones(POSICION_INICIAL)  

#Programa principal
root=tk.Tk()
root.geometry("800x600")
root.title("Permutaciones")
root.config(background='#1b1b32')
#Creacion de Frames
frame_fotos=tk.Frame(highlightbackground="#E0E0E4",highlightthickness=4,width=210,height=200,background="#1d1d36")
frame_no_imagenes=tk.Frame(frame_fotos,width=500,height=400,highlightbackground="#E5E5E8",highlightthickness=4,background="#1d1d36")
etiqueta_agregar_imagenes=tk.Label(frame_no_imagenes,text="AGREGA IMAGENES!!!!!!!!",width=60,height=15,background="#252546",font='sans_serif',fg="#E8E8F9")
frame_opciones_fotos=tk.Frame(pady=10, padx=10,background="#1d1d36",highlightbackground="#353544",highlightthickness=4)
lista_frames_opciones.append(tk.Frame(frame_opciones_fotos, width=210,height=120,padx=10,background="#1d1d36"))
lista_frames_opciones.append(tk.Frame(frame_opciones_fotos,width=210,height=120,padx=30, highlightbackground="#e9e9f2", highlightthickness=3,background="#1d1d36"))
lista_frames_opciones.append(tk.Frame(frame_opciones_fotos,width=210,height=120,padx=20,background="#1d1d36"))
frame_no_disponible=tk.Frame(frame_opciones_fotos,width=210,height=100,padx=10,bg="#1d1d36")
frame_botones=tk.Frame(pady=10,background='#1b1b32')
#Creacion de etiquetas
etiqueta_no_disponible=tk.Label(frame_no_disponible, text="NO DISPONIBLE", height=2, width=12,padx=10,bg="#1d1d36",fg="white",font='sans_serif')
label_anterior=tk.Label(frame_botones,text="Opcion Anterior",fg="white",bg='#1b1b32',font='sans_serif')
label_siguiente=tk.Label(frame_botones,text="Opcion siguiente",fg="white",bg='#1b1b32',font='sans_serif')
#Botones
boton_anterior=tk.Button(frame_botones,text="<<", command=anterior,fg="white",background="#42426c",width=10,height=5)
boton_siguiente=tk.Button(frame_botones,text=">>", command=siguiente,fg="white",background="#42426c",width=10,height=5)
boton_permutas=tk.Button(frame_botones,text="Realizar Permutas", command=realizar_permutas,fg="white",background="#3e3e70",width=15,height=2,font='sans_serif',state="disabled")
boton_imagen=tk.Button(frame_botones,text="Sube una imagen",command=selecionar_imagen,fg="white",background="#3e3e70",font='sans_serif',width=15)
#enpaquetar y presentar botones y etiquetas
frame_fotos.pack(pady=15)
frame_no_imagenes.pack(pady=15)
etiqueta_agregar_imagenes.pack()
frame_opciones_fotos.pack()
frame_botones.pack(pady=5)
boton_permutas.grid(column=2, row=0)
boton_imagen.grid(column=2,row=1)

root.mainloop()

# ------------------------------------------------------
# PROYECTO FINAL
#
# Equipo Permutas Naive
# Materia: Analisis de Algoritmos
# Calendario 2025B
# 
# Integrantes:
#
# Morales García Arturo Uriel
# Flores Garcia Bryan Miguel
# Matinez Rojo Arturo Gael
# Rodriguez Arellano Angel Ariel
# Ortiz Guizar Andres
# ------------------------------------------------------

#Libreria que importan los modulos necesarios
import busqueda
import tkinter as tk
from tkinter import ttk
from Bio import Entrez, SeqIO
# Variables globales

#Variable para guardar los patrones almacenados por el usuario
patrones =[]
#Guardar el item de la tabla para despues almacenar su permutas a nivel de ese item
niveles=[]
# Lista que contiene todas las permutas de cada patron
listasPermutas =[];
listaCombinacionesPatrones=[]
listasCombinacionesNaive=[]
# variable que guarda la secuencia en forma de bits
bitGrande=None;
# diccionario que nos genera la compresion de huffman
diccionario=None;
# id para almacenar los datos en la tabla
id=0;
#Ids para conseguir los patrones principales
idPrincipales=['Patron1','Patron2','Patron3']
idPatron=0;
# Variable gaurdamos la secuencia de ADN en forma de string
cadena_grande=None;
# CONFIGURACIÓN DE NCBI
Entrez.email = "arturo.morales7406@alumnos.udg.mx"
id_secuencia = "NC_045512.2"  # SARS-CoV-2

# ------------------------------------------------------
# FUNCIÓN PARA DESCARGAR SECUENCIA DE ADN DESDE NCBI
# ------------------------------------------------------
def obtener_secuencia_ncbi(id_ncbi):
    """
    Descarga una secuencia de ADN desde NCBI dado su identificador (por ejemplo: 'NC_045512.2').
    Devuelve la secuencia como una cadena (string).
    """
    print(f"Descargando secuencia {id_ncbi} desde NCBI...")
    handle = Entrez.efetch(db="nucleotide", id=id_ncbi, rettype="fasta", retmode="text")
    registro = SeqIO.read(handle, "fasta")
    handle.close()
    print(f"Secuencia descargada: {len(registro.seq)} bases.")
    return str(registro.seq)

# Obtener secuencia de ADN
def establecerCadenaGrande():
    global cadena_grande, id_secuencia;
    cadena_grande = obtener_secuencia_ncbi(id_secuencia)
    
# Metodo de busqueda Naive por Divide y Venceras
def divide_and_conquer_search(text, pattern, start=0):
    """Versión Divide y Vencerás del Naive String Matching."""
    n, m = len(text), len(pattern)
    if n < m:
        return []
    elif n <= 2 * m:
        return [start + i for i in range(n - m + 1) if text[i:i+m] == pattern]
    else:
        mid = n // 2
        left = divide_and_conquer_search(text[:mid + m - 1], pattern, start)
        right = divide_and_conquer_search(text[mid:], pattern, start + mid)
        return left + right

# Compresión Huffman
def huffman_encoding(data):
    if not data:
        return "", None
    frequency = {}
    for char in data:
    # Calculamos la frecuencia de cada caracter
        if char not in frequency:
            frequency[char] = 0
        frequency[char] += 1
    # Create a priority queue
    nodo = [[weight, [char, ""]] for char, weight in frequency.items()]
    while len(nodo) > 1:
        # Ordenamos los nodos por frecuencia
        nodo = sorted(nodo)
        # Tomamos los dos nodos con menor frecuencia
        izquierda = nodo[0]
        derecha = nodo[1]
        for par in izquierda[1:]:
            # agregamos '0' al frente de cada código
            par[1] = '0' + par[1]
        for par in derecha[1:]:
            # agregamos '1' al frente de cada código
            par[1] = '1' + par[1]
        nodo = nodo[2:]
        # combinamos los dos nodo
        nodo.append([izquierda[0] + derecha[0]] + izquierda[1:] + derecha[1:])
    # Creamos la lista de códigos Huffman
    huffman_code = sorted(nodo[0][1:], key=lambda p: (len(p[-1]), p))
    # Lo convertimos en un diccionario
    huffman_diccionario = {char: code for char, code in huffman_code}
    return huffman_diccionario

#Obtener lista de bits para usarlo en C++
def compresion(data, diccionario):
    bin_str = ''.join(diccionario[char] for char in data)
    return [int(b) for b in bin_str]  # lista de bits

# Realizar permutas de una lista de forma dinamica
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
# Mostrar cada patron que ingresa el usuario en un tabla de tk
def mostrarPatron ():
    # Modificar geometria de la ventana para adaptarla a la tabla
    root.geometry("1010x500")
    #Agregamos los patrones a la tabla
    agregarDatoTabla(entradaPatrones.get());
    #Guardamos patrones en una variable global
    patrones.append(entradaPatrones.get());
    #Limpiamos el entry
    entradaPatrones.delete(0, tk.END)
    #Informamos al usuario que se guardo su patron
    etiquetaGuardado =tk.Label(mensajePatronFrame, text="Patron Guardado!");
    etiquetaGuardado.pack();
    #Mostramos el fram de la tabla
    elFrameDeLosFrames.pack();
    mostrarPatronesFrame.grid(column=0,row=0);
    # Permitir hacer permutas hasta que se consigan 3 patrones guardados por el usuario 
    if len(patrones) == 3:
        botonIngresar.config(state="disabled",cursor="X_cursor",bg="gray");
        elFrameDeLosFrames.pack()
        botonPermutas.config(state="active",bg="yellow",cursor="hand2");
    #Desaparecer etiqueta de guardado al pasar un segundo
    root.after(1000, etiquetaGuardado.destroy)
    
# Agregar un patron ingresado por el usuario a la tabla
def agregarDatoTabla(dato):
    global idPatron, idPrincipales
    niveles.append(tabla.insert("","end",iid=idPrincipales[idPatron],text=dato,image=img_adn));
    idPatron=idPatron+1;
    
# Guardamos las permutas generadas por cada patron en niveles
def guardarPermutas(listaPermutas,nivel):
    global id;
    for permuta in listaPermutas:
        tabla.insert(niveles[nivel],tk.END,iid=id,text=permuta,image=img_adn);
        tabla.set(id, column="Estatus", value="No Buscado");
        id=id+1;
    
# Generamos permutas y  las guardamos segun el patron que le pertenezca la permuta
def generarPermutas():
    combinaciones=[]
    for patron in patrones:
        combinaciones.clear();
        listaPatron=list(patron);
        listasPermutas.append(permutas(listaPatron));
        for permuta in listasPermutas[-1]:
            combinaciones.append("".join(permuta));
        
        listaCombinacionesPatrones.append(list(combinaciones));
    i=0;
    for listaPermutas in listaCombinacionesPatrones:
        guardarPermutas(listaPermutas,i);
        i=i+1;
    botonPermutas.config(state="disabled",bg="gray",cursor="X_cursor");
    conseguirDiccionario();
    
# Se muestra una ventana donde se ve la secuencia de ADN y las partes donde la permuta elegida esta en la secuencia
def mostrar_ventana(event):
    global idPrincipales
    seleccion = tabla.selection()
    iid = seleccion[0]  
    if iid in idPrincipales:
        return;
    if seleccion:
        item = tabla.item(iid)
        patron = item["text"] 
        palabra = patron
        if item["values"][3] == "No Buscado":
            realizarBusquedaUnica(iid,patron);
        posiciones=divide_and_conquer_search(cadena_grande,patron);
        # Crear nueva ventana
        nueva_ventana = tk.Toplevel(root)
        nueva_ventana.title(f"Detalles del patrón: {patron}")
        nueva_ventana.geometry("700x700")
        nueva_ventana.configure(bg="#eaeaea")
        # Encabezado
        encabezado = tk.Label(nueva_ventana, text=f"Patrón seleccionado: {patron}",
                              font=("Segoe UI", 16, "bold"), bg="#eaeaea", fg="#333333")
        encabezado.pack(pady=(20, 10))
        # Frame para texto + scrollbar
        frame_texto = tk.Frame(nueva_ventana, bg="#eaeaea")
        frame_texto.pack(fill="both", expand=True, padx=20, pady=10)
        texto = tk.Text(frame_texto, wrap="word", font=("Segoe UI", 12),
                        bg="#fdfdfd", fg="#333333", insertbackground="#333333", relief="flat", borderwidth=0)
        texto.pack(side="left", fill="both", expand=True)
        scroll = tk.Scrollbar(frame_texto, command=texto.yview)
        scroll.pack(side="right", fill="y")
        texto.config(yscrollcommand=scroll.set)
        # Insertar texto completo
        texto.insert("1.0", cadena_grande)
        # Crear tag para subrayar
        texto.tag_configure("subrayado", underline=True, foreground="#007acc",
                            font=("Segoe UI", 12, "bold"))
        for pos in posiciones:
            # Convertir offset a índice válido para Text
            inicio = f"1.{pos}"
            fin = f"{inicio}+{len(palabra)}c"
            texto.tag_add("subrayado", inicio, fin)
            texto.config(state="disabled")
        # Botón cerrar
        cerrar_btn = tk.Button(nueva_ventana, text="Cerrar", command=nueva_ventana.destroy,
                               font=("Segoe UI", 11), bg="#d9534f", fg="white", relief="flat", padx=10, pady=5)
        cerrar_btn.pack(pady=20)
    
# Se consigue el diccionario de la compresion de huffman
def conseguirDiccionario():
    global bitGrande,diccionario;
    diccionario = huffman_encoding(cadena_grande+patrones[0]+patrones[1]+patrones[2]);
    bitGrande = compresion(cadena_grande, diccionario)
    

# Se realiza la busqueda de una sola permuta pasando la permuta (patron) y el iid del patron
def realizarBusquedaUnica(iid,patron):
    global diccionario;
    resultadoNaive=None;
    bitPatron = compresion(patron, diccionario)
    resultadoNaive=busqueda.divide_and_conquer_search(bitGrande,bitPatron,0);
    cadenaNaive=",".join(map(str,resultadoNaive))
    tabla.set(iid, column="No. Encontrados", value=len(resultadoNaive))
    tabla.set(iid, column="Posiciones", value=cadenaNaive)
    tabla.set(iid, column="Estatus", value="Buscado");


#---------------------------------------------------------INICIO DEL PROGRAMA -------------------------------------------------------------------------
#Cargamos la secuencia de ADN
establecerCadenaGrande();
#Iniciamos la interfaz de tk
root = tk.Tk()
#Cargamos imagen de ADN
img_adn = tk.PhotoImage(file="C:/Users/migue/Desktop/proyectoFinal2/adn.png").subsample(20,20);
root.title("Compresión y Búsqueda Huffman con patrones de ADN y permutas");
root.geometry("600x400")
#Establecemos los frames
entradaPatronesFrame = tk.Frame(root, borderwidth=2, relief="groove");
elFrameDeLosFrames =tk.Frame(root,bg="lightblue", borderwidth=2, relief="groove");
mostrarPatronesFrame =tk.Frame(elFrameDeLosFrames, borderwidth=2, relief="groove")
mensajePatronFrame = tk.Frame(root);
#Titutlos y entradas de datos del sistema.
etiquetaTitulo = tk.Label(root, text="Compresión y Búsqueda Huffman con patrones de ADN y permutas", font=("Arial", 14))
etiquetaTitulo.pack(pady=20)
etiquetaIngresarDatos =tk.Label(entradaPatronesFrame, text="Ingrese un patron:")
entradaPatrones = tk.Entry(entradaPatronesFrame,width=25)
botonIngresar = tk.Button(entradaPatronesFrame, text="Guardar patron", command=mostrarPatron,width=20,height=1,cursor="hand2");
entradaPatronesFrame.pack();
etiquetaIngresarDatos.grid(column=0,row=0, sticky="w", pady=5);
entradaPatrones.grid(column=1,row=0,pady=5,padx=10);
botonIngresar.grid(column=2,row=0,pady=5,padx=10);
etiquetaGenerarPermutas= tk.Label(entradaPatronesFrame, text="Generar permutas de patrones");
botonPermutas=tk.Button(entradaPatronesFrame, text="Generar",state="disabled",width=20,height=1,bg="gray",cursor="X_cursor",command=generarPermutas);
etiquetaGenerarPermutas.grid(row=1,column=1,pady=5,sticky="w");
botonPermutas.grid(column=2,row=1);
mensajePatronFrame.pack(pady=5);
#CONFIGURAMOS TABLA
tabla=ttk.Treeview(mostrarPatronesFrame, columns=("Patrones","No. Encontrados","Posiciones","Estatus"), show="tree headings");
tabla.heading("#0", text="Patrones") 
tabla.heading("No. Encontrados", text="No. Encontrados") 
tabla.heading("Posiciones", text="Posiciones");
tabla.heading("Estatus", text="Estatus");
tabla.bind("<<TreeviewSelect>>", mostrar_ventana)
tabla.column("No. Encontrados", anchor="center")
tabla.column("Posiciones", anchor="center")
tabla.column("Estatus", anchor="center")
mostrarPatronesFrame.grid(column=0,row=0)
tabla.pack(fill="both",side="left")
root.mainloop()

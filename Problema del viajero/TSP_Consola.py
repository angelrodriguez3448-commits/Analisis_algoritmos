import numpy as np
import tkinter as tk

ciudades = 0
caminos = 0
origen = 0
MatAdy = None
mejor_respuesta = 0

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
    ciudades = int(input("Ingrese el numero de ciudades: "), 10)
    MatAdy = np.zeros((ciudades, ciudades), dtype=int)

def LeerCaminos():
    global caminos
    caminos = int(input("Ingrese el numero de caminos: "), 10)

def LeerOrigen():
    global origen
    origen = int(input("Ciudad de origen del viaje: "), 10)

def LeerNodosC():
    global caminos, MatAdy, mejor_respuesta
    for i in range(caminos):
        origen = int(input("Ciudad de origen: "), 10)
        destino = int(input("Ciudad de destino: "), 10)
        distancia = int(input("Distancia entre ciudades: "), 10)
        if MatAdy[origen-1, destino-1] != 0:
            if MatAdy[origen-1, destino-1] > distancia:
                MatAdy[origen-1, destino-1] = distancia
                MatAdy[destino-1, origen-1] = distancia
        else:
            MatAdy[origen-1, destino-1] = distancia
            MatAdy[destino-1, origen-1] = distancia
        mejor_respuesta = mejor_respuesta + distancia

#print(MatAdy)

def BuscarRutas():
    global mejor_respuesta, ciudades, origen
    pruebas = 0
    valor_uno = 0
    valor_dos = 0
    mejor_ruta = []
    pruebas_total = factorial(ciudades)
    while(pruebas < pruebas_total):
        ruta = []
        disponibles = list(range(1, ciudades + 1))
        disponibles.remove(origen)
        ruta.append(origen)
        sub_origen = origen
        respuesta_parcial = 0

        while(len(disponibles) != 0):
            #numero_ran = (np.random.randint(1, 101) % ciudades) + 1
            siguiente_ciudad = np.random.choice(disponibles)
            siguiente_ciudad = int(siguiente_ciudad)
            valor_uno = MatAdy[siguiente_ciudad - 1, sub_origen - 1]
            valor_dos = MatAdy[sub_origen - 1, siguiente_ciudad - 1]
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

                print(f"Ruta actual: {ruta} Peso actual: {respuesta_parcial}")
        
        if(len(ruta) == ciudades):
            ruta.append(origen)
            valor_uno = MatAdy[sub_origen - 1, origen - 1]
            valor_dos = MatAdy[origen - 1, sub_origen - 1]
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
                if (respuesta_parcial < mejor_respuesta):
                    mejor_respuesta = respuesta_parcial
                    mejor_ruta = ruta
                    print(f"Nueva mejor ruta: {mejor_ruta} Peso: {mejor_respuesta}") 
            else:
                print(f"Ruta descartada: {ruta}")
        else:
            print(f"Ruta descartada: {ruta}")

        pruebas = pruebas + 1
        print(f"Iteraciones: {pruebas}")
    return mejor_ruta, mejor_respuesta


LeerCiudades()
LeerCaminos()
LeerNodosC()
LeerOrigen()  
mr, mp = BuscarRutas()   
print(f"Mejor ruta: {mr}")
print(f"Con un peso de: {mp}")
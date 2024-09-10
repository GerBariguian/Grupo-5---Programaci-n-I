#Librerias

import random
import os

#Constantes (en este caso el tamaño que tendria tablero)

ALTO = 10
ANCHO = 20

#Funciones

def inicializar_juego():
    #print("test")
    tablero = []
    for i in range(ALTO):
        fila = []  #fila vacia
        for j in range(ANCHO):
            fila.append(" ")  # Agrego un espacio a la fila
        tablero.append(fila)  # Agrego la fila al tablero

    #Para que la serpiente siempre aparezca en el centro, la ubico inicialmente de la siguiente forma:
    serpiente = [(ALTO // 2, ANCHO // 2), (ALTO // 2, ANCHO // 2 - 1), (ALTO // 2, ANCHO // 2 - 2)] #x,y

    for y, x in serpiente: #recorro las posiciones
        tablero[y][x] = "O" #asigno a las posiciones "O"

    bandera=True
    while bandera:
        comida = (random.randint(0, ALTO-1), random.randint(0, ANCHO-1)) #ALTO y ANCHO restando 1 por el range
        comida_no_choca=True #funciona como la bandera para controlar
        for parte in serpiente:
            if comida==parte:
                comida_no_choca=False
        if comida_no_choca:
            bandera=False

    #Teniendo los valores de comida y sabiendo que no choca con la serpiente, coloco la comida en el tablero
    tablero[comida[0]][comida[1]] = "*"

    return tablero, serpiente, comida
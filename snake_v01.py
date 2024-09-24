#Librerias

import random
import os #importamos para limpiar la consola
import re #importamos para trabajar regex 

#Constantes (en este caso el tamaño que tendria tablero)

ALTO = 10
ANCHO = 30

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
    serpiente = [(ALTO // 2, ANCHO // 2), (ALTO // 2, ANCHO // 2 - 1), (ALTO // 2, ANCHO // 2 - 2)] #lista de tuplas (y,x)

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

    direccion = 1 #direccion inicial

    return tablero, serpiente, comida, direccion

def imprimir_tablero(tablero):
    #Aplico la libreria OS para limpiar la consola
    os.system('cls' if os.name=='nt' else 'clear')
    #Impresion del tablero
    print("+" + "-" * ANCHO + "+") #superior
    for fila in tablero: #centro
        print("|" + "".join(fila) + "|")
    print("+" + "-" * ANCHO + "+") #inferior

#----------------------------------------

def cargar_datos_usuario():
    datos_usuario = {} #iniciamos el diccionario

    regex_alias = r'^(?=.*[a-zA-Z]{5,})(?=.*\d{2,})' #condicion a cumplir

    #Nombre
    soloLetras = False
    while soloLetras == False:
        nombre = input("Ingresa tu nombre: ").strip() #elimino espacios en blanco
        if nombre.isalpha(): #todos los caracteres son letras
            soloLetras = True
        else:
            print("El nombre solo debe contener letras.")

    #Edad
    edadValida = False
    while edadValida == False:
        edad = int(input("Ingrese su edad: ").strip())
        if edad>0 and edad<125: #edad tiene que ser digito y mayor que 0
            edadValida = True
        else:
            print("Por favor ingrese una edad valida")

    #Alias
    alias = input("Ingresa tu alias (al menos 5 letras y 2 números): ").strip()
    coincide = False
    while coincide == False: #mientras que el alias no cumpla con la regex, seguira pidiendo ingresar nuevamente
        print("El alias debe contener al menos 5 letras y 2 números.")
        alias = input("Ingresa tu alias: ").strip()
        if re.match(regex_alias, alias): #(patron, cadena):
            coincide=True

    #Diccionario
    datos_usuario["nombre"] = nombre
    datos_usuario["edad"] = edad
    datos_usuario["alias"] = alias

    print("Datos registrados correctamente:", datos_usuario)
    return datos_usuario

#----------------------------------------

def menu():
    opciones=True
    while opciones:
        print("1. Iniciar juego")
        print("2. Salir")
        opcion=int(input("Ingrese una opcion: "))
        if opcion==1:
            main()
        elif opcion==2:
            print("Gracias por jugar!")
            opciones=False
        else:
            print("Opcion no valida")

def main():
    #Pedir que se ingresen datos por teclado
    datos_usuario = cargar_datos_usuario() #datos_usuario es un diccionario

    #Inicio el juego 
    tablero, serpiente, comida, direccion = inicializar_juego() #pongo las variables en el orden del return 

    juego_activo = True
    while juego_activo:
        imprimir_tablero(tablero)
        print(f"Jugador: {datos_usuario['nombre']} | Edad: {datos_usuario['edad']} | Alias: {datos_usuario['alias']}")
        print("Controles: 'w' = Arriba, 's' = Abajo, 'a' = Izquierda, 'd' = Derecha")
        movimiento = input("Introduce tu movimiento: ").lower() #aseguro que la letra ingresada pase a minuscula

        #Direccion
        if movimiento == 'w' and direccion != 2:  #Arriba
            direccion = 0
        elif movimiento == 'd' and direccion != 3:  #Derecha
            direccion = 1
        elif movimiento == 's' and direccion != 0:  #Abajo
            direccion = 2
        elif movimiento == 'a' and direccion != 1:  #Izquierda
            direccion = 3
        #juego_activo = False
        
#inicio el menu
menu()
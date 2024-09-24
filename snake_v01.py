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

def actualizar_tablero(tablero, serpiente, comida):
    # Limpiar el tablero
    for y in range(ALTO):
        for x in range(ANCHO):
            tablero[y][x] = " "

    # Colocar la comida
    tablero[comida[0]][comida[1]] = "*"

    # Colocar el serpiente
    for y, x in serpiente:
        tablero[y][x] = "O"

def mover_serpiente(serpiente, direccion, crece):
    #Obtengo la posicion actual de la cabeza de la serpiente
    cabeza_y, cabeza_x = serpiente[0]

    #Determino la nueva posicion de la cabeza segun la direccion
    if direccion == 0:  # Arriba
        nueva_cabeza = (cabeza_y - 1, cabeza_x)
    elif direccion == 1:  # Derecha
        nueva_cabeza = (cabeza_y, cabeza_x + 1)
    elif direccion == 2:  # Abajo
        nueva_cabeza = (cabeza_y + 1, cabeza_x)
    elif direccion == 3:  # Izquierda
        nueva_cabeza = (cabeza_y, cabeza_x - 1)

    #Agrego la nueva cabeza a la serpiente
    serpiente.insert(0, nueva_cabeza) #(posicion, elemento)
    
    #Elimino la cola si no crece para mantener la longitud constante, a menos que la serpiente coma
    if not crece: #se ejecuta si crece es False
        serpiente.pop()

def comprobar_comida(serpiente, comida):
    # Verifica si la cabeza del serpiente está en la misma posición que la comida
    return serpiente[0] == comida #devuelve True o False

def comprobar_colision(serpiente):
    cabeza = serpiente[0] #posicion de la cabeza -> la asigno a cabeza -> (y,x)
    
    if cabeza[0] < 0 or cabeza[0] >= ALTO or cabeza[1] < 0 or cabeza[1] >= ANCHO: #compruebo si toco alguno de los bordes
        return True
    
    if cabeza in serpiente[1:]: #compruebo si la serpiente se choco consigo misma
        return True
    return False

def generar_comida(serpiente):
    #Se genera una nueva comida en una posicion aleatoria (no puede estar ocupada por la serpiente)
    while True:
        nueva_comida = (random.randint(0, ALTO - 1), random.randint(0, ANCHO - 1))
        if nueva_comida not in serpiente: #si la nueva comida no esta ocupada por la serpiente
            return nueva_comida
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

        #Verifico si la serpiente debe crecer o no (en base a si come la comida)
        crece = comprobar_comida(serpiente, comida)
        
        #Actualizar el movimiento
        mover_serpiente(serpiente, direccion, crece)
        
        #Comprobamos si hay colisiones -> borde o con la misma serpiente
        if comprobar_colision(serpiente): #true o false
            imprimir_tablero(tablero)
            print("¡Colisión! Fin del juego :(")
            juego_activo = False #game over -> sale del while
        else:
            #Si la serpiente obtuvo la comida -> genero otra aleatoria en el tablero
            if crece: 
                comida = generar_comida(serpiente)
            
            #Actualizo el tablero con las nuevas posiciones de la serpiente y la comida
            actualizar_tablero(tablero, serpiente, comida)

    # Código que se ejecuta después de que el juego termina
    print("¡Gracias por jugar!")

#inicio el menu
menu()
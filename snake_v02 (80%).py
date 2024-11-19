import random
import os
import re
import time
import keyboard
import json
from colorama import Fore, Style, init
# Inicializar colorama
init(autoreset=True)
 
# Constantes
ALTO = 20
ANCHO = 60
tiempo_de_retraso_base = 0.1
ARCHIVO_PARTIDAS = "registro_partidas.json"  
 
# Funciones
def cargar_datos_usuario():
    """
    Solicita y valida los datos del usuario (nombre, edad y alias).
   
    Returns:
        dict: Diccionario con los datos del usuario (nombre, edad, alias)
    """
    datos_usuario = {}
    regex_alias = r'^(?=.*[a-zA-Z]{5,})(?=.*\d{2,})'
    soloLetras = False
    while not soloLetras:
        nombre = input("Ingresa tu nombre: ").strip()
        if nombre.isalpha():
            soloLetras = True
        else:
            print("El nombre solo debe contener letras.")
    edadValida = False
    while not edadValida:
        try:
            edad = int(input("Ingrese su edad (0-125, numero entero): ").strip())
            if 0 < edad < 125:
                edadValida = True
        except ValueError:
            print("Por favor ingrese una edad válida.")
    coincide = False
    while not coincide:
        alias = input("Ingresa tu alias: ").strip()
        if re.match(regex_alias, alias):
            coincide = True
        else:
            print("El alias debe contener al menos 5 letras y 2 números.")
    datos_usuario["nombre"] = nombre
    datos_usuario["edad"] = edad
    datos_usuario["alias"] = alias
    print("Datos registrados correctamente:", datos_usuario)
    return datos_usuario
 
def inicializar_juego(nivel):
    """
    Inicializa el estado del juego según el nivel seleccionado.
   
    Args:
        nivel (int): Nivel de dificultad (1-3)
   
    Returns:
        tupla: (tablero, serpiente, comida, obstaculos, direccion)
    """
    tablero = [[" " for _ in range(ANCHO)] for _ in range(ALTO)]
    serpiente = [(ALTO // 2, ANCHO // 2), (ALTO // 2, ANCHO // 2 - 1), (ALTO // 2, ANCHO // 2 - 2)]
    for y, x in serpiente:
        tablero[y][x] = "■"
    comida = generar_posicion_vacia(tablero, serpiente)
    tablero[comida[0]][comida[1]] = "🍏"
    obstaculos = []
    if nivel > 1:
        num_obstaculos = 5 if nivel == 2 else 10
        for _ in range(num_obstaculos):
            obstaculo = generar_posicion_vacia(tablero, serpiente + obstaculos)
            obstaculos.append(obstaculo)
            tablero[obstaculo[0]][obstaculo[1]] = "■"
    return tablero, serpiente, comida, obstaculos, 1
 
def imprimir_tablero(tablero):
    """
    Limpia la pantalla y muestra el estado actual del tablero.
   
    Args:
        tablero (lista): Matriz que representa el estado actual del juego
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + "■" * (ANCHO + 2))
    for fila in tablero:
        print(Fore.RED + "■" + "".join(fila) + "■")
    print(Fore.RED + "■" * (ANCHO + 2))
 
def actualizar_tablero(tablero, serpiente, comida, obstaculos):
    """
    Actualiza el estado del tablero con las posiciones actuales de todos los elementos.
   
    Args:
        tablero (lista): Matriz del juego
        serpiente (lista): Lista de coordenadas de la serpiente
        comida (tupla): Coordenadas de la comida
        obstaculos (lista): Lista de coordenadas de los obstáculos
    """
    for y in range(ALTO):
        for x in range(ANCHO):
            tablero[y][x] = " "
    tablero[comida[0]][comida[1]] = "🍏" #genera que se "rompa" un poco el tablero :/
    for obs in obstaculos:
        tablero[obs[0]][obs[1]] = "■"
    for y, x in serpiente:
        tablero[y][x] = "■"
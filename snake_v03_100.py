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
    tablero[comida[0]][comida[1]] = "⛾"
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
    tablero[comida[0]][comida[1]] = "⛾" 
    for obs in obstaculos:
        tablero[obs[0]][obs[1]] = "■"
    for y, x in serpiente:
        tablero[y][x] = "■"

def mover_serpiente(serpiente, direccion, crece):
    """
    Actualiza la posición de la serpiente según la dirección.
    
    Args:
        serpiente (lista): Lista de coordenadas de la serpiente
        direccion (int): Dirección del movimiento (0:arriba, 1:derecha, 2:abajo, 3:izquierda)
        crece (bool): Indica si la serpiente debe crecer
    """
    cabeza_y, cabeza_x = serpiente[0]
    nueva_cabeza = (
        cabeza_y + (direccion == 2) - (direccion == 0),
        cabeza_x + (direccion == 1) - (direccion == 3)
    )
    serpiente.insert(0, nueva_cabeza)
    if not crece:
        serpiente.pop()
 
def comprobar_comida(serpiente, comida):
    """
    Verifica si la serpiente ha alcanzado la comida.
    
    Args:
        serpiente (lista): Lista de coordenadas de la serpiente
        comida (tupla): Coordenadas de la comida
    
    Returns:
        bool: True si la serpiente alcanzó la comida, False en caso contrario
    """
    return serpiente[0] == comida
 
def comprobar_colision(serpiente, obstaculos):
    """
    Verifica si la serpiente ha colisionado con algo.
    
    Args:
        serpiente (lista): Lista de coordenadas de la serpiente
        obstaculos (lista): Lista de coordenadas de los obstáculos
    
    Returns:
        bool: True si hay colisión, False en caso contrario
    """
    cabeza = serpiente[0]
    fuera_de_limites = cabeza[0] < 0 or cabeza[0] >= ALTO or cabeza[1] < 0 or cabeza[1] >= ANCHO
    choca_con_obstaculo = cabeza in obstaculos
    choca_con_cuerpo = cabeza in serpiente[1:]
    return fuera_de_limites or choca_con_obstaculo or choca_con_cuerpo

def generar_posicion_vacia(tablero, excluidos):
    """
    Genera una posición aleatoria vacía en el tablero.
   
    Args:
        tablero (lista): Matriz del juego
        excluidos (lista): Lista de posiciones que deben evitarse
   
    Returns:
        tupla: Coordenadas (y, x) de la nueva posición
    """
    while True:
        pos = (random.randint(0, ALTO - 1), random.randint(0, ANCHO - 1))
        if pos not in excluidos:
            return pos
 
def guardar_datos_partida(datos_usuario, nivel, puntaje, tiempo_jugado):
    """
    Guarda los datos de la partida en el archivo JSON.
   
    Args:
        datos_usuario (dict): Información del usuario
        nivel (int): Nivel jugado
        puntaje (int): Puntos obtenidos
        tiempo_jugado (int): Duración de la partida en segundos
    """
    nuevo_registro = {
        "nombre": datos_usuario["nombre"],
        "edad": datos_usuario["edad"],
        "alias": datos_usuario["alias"],
        "nivel": nivel,
        "puntaje": puntaje,
        "tiempo_jugado": tiempo_jugado
    }
    
    try:
        with open(ARCHIVO_PARTIDAS, 'r') as archivo:
            registros = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        registros = []
   
    registros.append(nuevo_registro)
    with open(ARCHIVO_PARTIDAS, 'w') as archivo:
        json.dump(registros, indent=4, fp=archivo)
 
def mostrar_top_3():
    """
    Muestra los 3 mejores puntajes almacenados en el archivo JSON usando programación funcional.
    """
    try:
        with open(ARCHIVO_PARTIDAS, 'r') as archivo:
            registros = json.load(archivo)
        
        #lambda para formateo
        obtener_medalla = lambda pos: {1: "🥇", 2: "🥈", 3: "🥉"}.get(pos, "") #buscamos la pos en el diccionario
        formatear_tiempo = lambda t: f"{int(t//60)}m {int(t%60)}s" if t >= 60 else f"{int(t)}s"
        
        #Ordenar y obtener top 3
        top_3 = sorted(registros, key=lambda x: (x['puntaje'], -x['tiempo_jugado']), reverse=True)[:3]
        
        #lambda para formatear cada registro
        formato_registro = lambda r, pos: (
            f"{obtener_medalla(pos)} Alias: {r['alias']}\n"
            f"   Puntaje: {r['puntaje']} pts\n"
            f"   Nivel: {r['nivel']}\n"
            f"   Tiempo: {formatear_tiempo(r['tiempo_jugado'])}"
        )
        
        print("\n" + "="*40)
        print(f"{Fore.YELLOW}🏆 TOP 3 MEJORES PUNTAJES 🏆{Style.RESET_ALL}")
        print("="*40)
        
        #enumerate y map para mostrar registros
        registros_formateados = list(map(
            lambda x: formato_registro(x[1], x[0]), 
            enumerate(top_3, 1)
        ))
        
        for registro in registros_formateados:
            print(f"\n{registro}")
            print("-"*40)
        
        if not registros:
            print("\nAún no hay registros de partidas.")
        
        input("\nPresione Enter para continuar...")
        
    except (FileNotFoundError, json.JSONDecodeError):
        print("\nAún no hay registros de partidas.")
        input("\nPresione Enter para continuar...")

def menu():
    """
    Muestra el menú principal del juego y maneja la selección de opciones.
    """
    # Banner del juego
    banner = f"""
{Fore.GREEN}
╔═══════════════════════════════════════════════╗
║             {Fore.YELLOW}🐍 SNAKE GAME 🐍{Fore.GREEN}              ║
╚═══════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    
    datos_usuario = cargar_datos_usuario()
    opciones_activas = True
    
    while opciones_activas:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        
        # Mostrar información del usuario
        print(f"{Fore.CYAN}┌──── Datos del Jugador ────┐")
        print(f"│ Nombre: {Fore.WHITE}{datos_usuario['nombre']}{Fore.CYAN}")
        print(f"│ Alias:  {Fore.WHITE}{datos_usuario['alias']}{Fore.CYAN}")
        print(f"└─────────────────────────┘{Style.RESET_ALL}\n")

        # Menú de opciones
        print(f"{Fore.YELLOW}═══════ NIVELES DE JUEGO ═══════{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1]{Fore.WHITE} ▸ Nivel 1 {Fore.BLUE}(Básico){Style.RESET_ALL}")
        print(f"{Fore.GREEN}[2]{Fore.WHITE} ▸ Nivel 2 {Fore.YELLOW}(Obstáculos y velocidad moderada){Style.RESET_ALL}")
        print(f"{Fore.GREEN}[3]{Fore.WHITE} ▸ Nivel 3 {Fore.RED}(Más obstáculos y alta velocidad){Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}═══════ OTRAS OPCIONES ═══════{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[4]{Fore.WHITE} ▸ Ver TOP 3 {Fore.YELLOW}🏆{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[5]{Fore.WHITE} ▸ Salir {Fore.RED}⬅{Style.RESET_ALL}")
        
        # Input con color
        print(f"\n{Fore.CYAN}╭─────────────────────╮")
        opcion = input(f"│ Seleccione opción ➤ {Style.RESET_ALL}")
        
        if opcion in ['1', '2', '3']:
            main(int(opcion), datos_usuario)
        elif opcion == '4':
            mostrar_top_3()
        elif opcion == '5':
            print(f"\n{Fore.YELLOW}¡Gracias por jugar! 👋{Style.RESET_ALL}")
            time.sleep(1.5)
            opciones_activas = False
        else:
            print(f"\n{Fore.RED}⚠ Opción no válida, intente de nuevo.{Style.RESET_ALL}")
            time.sleep(1.5)
 
def main(nivel, datos_usuario):
    """
    Función principal que ejecuta el juego.
    
    Args:
        nivel (int): Nivel de dificultad seleccionado
        datos_usuario (dict): Información del usuario
    """
    tiempo_de_retraso = tiempo_de_retraso_base / (nivel * 1.5)
    tablero, serpiente, comida, obstaculos, direccion = inicializar_juego(nivel)
    ultima_pulsacion = time.time()
    tiempo_inicial = time.time()
    puntos = 0  # Contador de puntos
    juego_activo = True
    while juego_activo:
        imprimir_tablero(tablero)
        tiempo_jugado = int(time.time() - tiempo_inicial)
        print(f"Jugador: {datos_usuario['nombre']} | Edad: {datos_usuario['edad']} | Alias: {datos_usuario['alias']}")
        print(f"Tiempo de juego: {tiempo_jugado} segundos | Nivel: {nivel} | Puntos: {puntos}")
        tiempo_actual = time.time()
        if tiempo_actual - ultima_pulsacion >= tiempo_de_retraso:
            if keyboard.is_pressed('w') and direccion != 2:
                direccion = 0
                ultima_pulsacion = tiempo_actual
            elif keyboard.is_pressed('d') and direccion != 3:
                direccion = 1
                ultima_pulsacion = tiempo_actual
            elif keyboard.is_pressed('s') and direccion != 0:
                direccion = 2
                ultima_pulsacion = tiempo_actual
            elif keyboard.is_pressed('a') and direccion != 1:
                direccion = 3
                ultima_pulsacion = tiempo_actual
        crece = comprobar_comida(serpiente, comida)
        mover_serpiente(serpiente, direccion, crece)
        if comprobar_colision(serpiente, obstaculos):
            imprimir_tablero(tablero)
            print(f"¡Colisión! Fin del juego :( | Tiempo total: {tiempo_jugado} segundos | Puntos: {puntos}")
            guardar_datos_partida(datos_usuario, nivel, puntos, tiempo_jugado)
            juego_activo = False
        else:
            if crece:
                puntos += 1  # Incrementar puntos al comer comida
                comida = generar_posicion_vacia(tablero, serpiente + obstaculos)
            actualizar_tablero(tablero, serpiente, comida, obstaculos)
        time.sleep(0.08)
 
# Cambiar la última parte del archivo:
if __name__ == "__main__":
    # Verificar si el archivo de registros existe, sino crea uno
    if not os.path.isfile(ARCHIVO_PARTIDAS):
        with open(ARCHIVO_PARTIDAS, 'w') as archivo:
            json.dump([], fp=archivo)
    
    menu()
## Grupo-5---Programacion-I

# Alumnos: Bariguian, Reboredo Blanco

#Juego: SNAKE

#Funciones: 
# 1. Inicialización del Juego:
#inicializar_juego(): Configura el tablero, inicializa la posición inicial de la serpiente y genera la primera comida.
#imprimir_tablero(tablero): Imprime por pantalla el tablero en base a las especificaciones brindadas y generadas anteriormente.

# 2. Gestión de la Serpiente:
#mover_serpiente(serpiente, direccion): Actualiza la posición de la serpiente según la dirección de movimiento (arriba, abajo, izquierda, derecha).
#crecer_serpiente(serpiente): Añade una nueva unidad al final de la serpiente, usada cuando come la comida.
#colision(serpiente, tablero): Verifica si la serpiente ha colisionado consigo misma o con las paredes.

# 3. Gestión de la Comida:
#generar_comida(tablero, serpiente): Coloca comida en una posición aleatoria del tablero que no esté ocupada por la serpiente.
#comer(serpiente, comida): Verifica si la serpiente ha comido la comida y, si es así, actualiza la serpiente y genera una nueva comida.

# 4. Entrada y Control del Juego:
#obtener_direccion(tecla): Convierte la entrada del usuario en una dirección de movimiento.
#actualizar_pantalla(tablero, serpiente, comida): Refresca la pantalla para mostrar el estado actual del juego.
#manejar_teclas(tecla): Procesa las teclas presionadas por el jugador para cambiar la dirección de la serpiente.

# 5. Archivos:
#guardar_puntaje(puntaje, archivo): Guarda el puntaje actual en un archivo.
#cargar_puntaje(archivo): Carga el puntaje más alto desde un archivo para mostrarlo al inicio del juego.

# 6. Excepciones y Pruebas Unitarias:
#manejar_excepciones(): Maneja posibles errores como índices fuera de rango o errores de archivo.
#pruebas_unitarias(): Implementa pruebas unitarias para funciones como mover_serpiente, colision, y generar_comida.

# 7. Función Principal del Juego:
#jugar(): La función que ejecuta el bucle principal del juego.

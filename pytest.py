import pytest
from snake_v02 (80%) import comprobar_comida, generar_posicion_vacia
 
def test_comprobar_comida():
    serpiente = [(5, 5), (5, 4), (5, 3)]
    comida = (5, 5)
    assert comprobar_comida(serpiente, comida) == True  # Debería detectar que comió
 
    comida = (4, 5)
    assert comprobar_comida(serpiente, comida) == False  # No debería detectar que comió
 
def test_generar_posicion_vacia():
    # Configuración: tablero vacío y posiciones excluidas
    tablero = [[" " for _ in range(10)] for _ in range(5)]  # Tablero 5x10
    excluidos = [(0, 0), (1, 1), (2, 2)]  # Posiciones ocupadas
 
    # Ejecutar la función
    posicion = generar_posicion_vacia(tablero, excluidos)
 
    # Comprobaciones
    assert posicion not in excluidos, "La posición generada no debe estar en las excluidas"
    assert 0 <= posicion[0] < len(tablero), "La fila de la posición debe estar dentro del rango del tablero"
    assert 0 <= posicion[1] < len(tablero[0]), "La columna de la posición debe estar dentro del rango del tablero"
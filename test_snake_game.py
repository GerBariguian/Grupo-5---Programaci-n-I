import pytest
from snake_v03_100 import (
    generar_posicion_vacia,
    comprobar_colision,
    comprobar_comida,
    mover_serpiente
)

# Test para generar_posicion_vacia
def test_generar_posicion_vacia():
    tablero = [[" " for _ in range(60)] for _ in range(20)]
    excluidos = [(0, 0), (1, 1)]
    pos = generar_posicion_vacia(tablero, excluidos)
    
    assert pos not in excluidos
    assert 0 <= pos[0] < 20  # ALTO
    assert 0 <= pos[1] < 60  # ANCHO

# Test para comprobar_colision
def test_comprobar_colision():
    # Caso: Fuera de límites
    serpiente = [(-1, 0)]  # Posición fuera del tablero
    assert comprobar_colision(serpiente, []) == True
    
    # Caso: Colisión con obstáculo
    serpiente = [(5, 5)]
    obstaculos = [(5, 5)]
    assert comprobar_colision(serpiente, obstaculos) == True
    
    # Caso: Sin colisión
    serpiente = [(5, 5)]
    obstaculos = [(6, 6)]
    assert comprobar_colision(serpiente, obstaculos) == False

# Test para comprobar_comida
def test_comprobar_comida():
    serpiente = [(1, 1)]
    # Caso: Serpiente sobre la comida
    assert comprobar_comida(serpiente, (1, 1)) == True
    # Caso: Comida en otra posición
    assert comprobar_comida(serpiente, (2, 2)) == False

# Test para mover_serpiente
@pytest.mark.parametrize("direccion,expected_head", [
    (0, (4, 5)),  # Arriba
    (1, (5, 6)),  # Derecha
    (2, (6, 5)),  # Abajo
    (3, (5, 4))   # Izquierda
])
def test_mover_serpiente(direccion, expected_head):
    serpiente = [(5, 5), (5, 4), (5, 3)]
    serpiente_original = serpiente.copy()
    
    mover_serpiente(serpiente, direccion, False)
    
    # Verificar nueva posición de la cabeza
    assert serpiente[0] == expected_head
    # Verificar que la longitud se mantiene si no crece
    assert len(serpiente) == len(serpiente_original) 
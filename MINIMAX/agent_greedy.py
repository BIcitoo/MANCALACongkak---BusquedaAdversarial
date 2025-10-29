import logic
import math

class AgentGreedy:
    def __init__(self): 
        pass

    def elegir_movimiento(self, board_state, current_player, time_limit=None):
        
        if current_player == 1:
            almacen = 7
        else:
            almacen = 15
        
        movimientos_posibles = []
        if current_player == 1:
            rango_huecos = range(0, 7)
        
        else:
            rango_huecos = range(8, 15)

        for hueco in rango_huecos:
            if board_state[hueco] > 0:
                movimientos_posibles.append(hueco)
        
        if len(movimientos_posibles) == 0:
            return None, {'nodes_expanded': 0, 'depth_reached': 0}
        
        mejor_movimiento = -1
        mejor_puntuacion = -math.inf

        for movimiento in movimientos_posibles:
            tablero_simulado, _ = logic.hacer_movimiento(list(board_state), movimiento, current_player)
            puntuacion_actual = tablero_simulado[almacen]

            if puntuacion_actual > mejor_puntuacion:
                mejor_puntuacion = puntuacion_actual
                mejor_movimiento = movimiento

        return mejor_movimiento, {'nodes_expanded': len(movimientos_posibles), 'depth_reached': 1}

import logic
import math

class AgentWorst:
    def __init__(self): 
        pass

    def elegir_movimiento(self, board_state, current_player, time_limit=None):
        
        # Determinar almacen del oponente
        if current_player == 1:
            almacen_oponente = 15
        else:
            almacen_oponente = 7
        
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
        
        # Buscar el movimiento que maximiza el puntaje del OPONENTE
        peor_movimiento = -1
        max_puntuacion_oponente = -math.inf

        for movimiento in movimientos_posibles:
            tablero_simulado, _ = logic.hacer_movimiento(list(board_state), movimiento, current_player)
            puntuacion_oponente = tablero_simulado[almacen_oponente]

            # Elegir el movimiento que da MAS puntos al oponente (peor decision)
            if puntuacion_oponente > max_puntuacion_oponente:
                max_puntuacion_oponente = puntuacion_oponente
                peor_movimiento = movimiento
        
        # Si todos dan el mismo puntaje, elegir el primero
        if peor_movimiento == -1:
            peor_movimiento = movimientos_posibles[0]

        return peor_movimiento, {'nodes_expanded': len(movimientos_posibles), 'depth_reached': 1}


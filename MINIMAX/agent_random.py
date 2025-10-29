import random

class AgentRandom:
    def __init__(self):
        pass

    def elegir_movimiento(self, board_state: list, current_player: int, time_limit=None):
        """Selecciona un movimiento aleatorio del jugador actual."""
        
        if current_player == 1:
            rango = range(0, 7)
        else:
            rango = range(8, 15)
            
        movimientos_posibles = [h for h in rango if board_state[h] > 0]
        
        if not movimientos_posibles:
            return None, {'nodes_expanded': 0, 'depth_reached': 0}
        
        movimiento_aleatorio = random.choice(movimientos_posibles)
        
        # Retornar con el mismo formato que los otros agentes
        return movimiento_aleatorio, {'nodes_expanded': 1, 'depth_reached': 1}
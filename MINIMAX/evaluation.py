import math
from copy import deepcopy

# Integración con los módulos del proyecto
import rules
import logic


def _get_player_data(player_id: int) -> tuple:
    """Devuelve los índices de almacenes y huecos correspondientes al jugador indicado."""
    if player_id == 1:
        return 7, 15, list(range(0, 7)), list(range(8, 15))
    else:
        return 15, 7, list(range(8, 15)), list(range(0, 7))


# Heurísticas individuales
def _h1_score_differential(board_state: list, player_id: int) -> int:
    """Diferencia entre el puntaje propio y el del oponente."""
    mi_store, op_store, _, _ = _get_player_data(player_id)
    return board_state[mi_store] - board_state[op_store]


def _h2_extra_turns(board_state: list, player_id: int, logic_func) -> int:
    """Cuenta las jugadas que otorgan turno adicional al jugador actual."""
    _, _, mi_holes, _ = _get_player_data(player_id)
    extra_turns = 0

    for pit in [h for h in mi_holes if board_state[h] > 0]:
        tablero_temp = deepcopy(board_state)
        _, result = logic_func(tablero_temp, pit, player_id)
        if result == "TURNO_EXTRA":
            extra_turns += 1

    return extra_turns


def _h3_mobility_control(board_state: list, player_id: int) -> int:
    """Evalúa la cantidad de piedras en los huecos propios."""
    _, _, mi_holes, _ = _get_player_data(player_id)
    return sum(board_state[h] for h in mi_holes)


def _h4_opponent_starvation(board_state: list, player_id: int) -> int:
    """Evalúa las piedras del oponente. Este valor debe penalizarse con un peso negativo."""
    _, _, _, op_holes = _get_player_data(player_id)
    return sum(board_state[h] for h in op_holes)


def _h5_control_key_hole(board_state: list, player_id: int) -> int:
    """Evalúa el control del hueco más cercano al almacén."""
    key_hole = 6 if player_id == 1 else 14
    return board_state[key_hole]


# Función principal de evaluación
def evaluate(board_state: list, player_id: int, weights_config: dict = None) -> float:
    """
    Evalúa el estado actual del tablero para el jugador indicado.
    Devuelve un valor heurístico que pondera distintas métricas del juego.
    """

    # Verificar si el juego ha terminado
    game_status = rules.check_game_over(board_state)
    if game_status != 0:
        tablero_final = rules.final_sweep(deepcopy(board_state), game_status)
        mi_store, op_store, _, _ = _get_player_data(player_id)

        if tablero_final[mi_store] > tablero_final[op_store]:
            return math.inf
        elif tablero_final[mi_store] < tablero_final[op_store]:
            return -math.inf
        else:
            return 0.0

    # Calcular las heurísticas
    h1 = _h1_score_differential(board_state, player_id)
    h2 = _h2_extra_turns(board_state, player_id, logic.hacer_movimiento)
    h3 = _h3_mobility_control(board_state, player_id)
    h4 = _h4_opponent_starvation(board_state, player_id)
    h5 = _h5_control_key_hole(board_state, player_id)

    # Pesos configurables
    if weights_config is None:
        weights_config = {}
    w1 = weights_config.get('w1', 10.0)
    w2 = weights_config.get('w2', 50.0)
    w3 = weights_config.get('w3', 0.8)
    w4 = weights_config.get('w4', -0.5)
    w5 = weights_config.get('w5', 1.5)

    # Combinación ponderada
    score = (w1 * h1) + (w2 * h2) + (w3 * h3) + (w4 * h4) + (w5 * h5)
    return score

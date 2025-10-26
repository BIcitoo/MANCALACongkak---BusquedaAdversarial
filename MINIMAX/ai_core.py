import math
import time
import logic
import rules

def minimax_search(board_state, player_id, depth, alpha, beta, is_maximizing, time_limit, start_time, evaluation_func, logic_func, rules_func, weights_config=None):
    
    if time.time() - start_time > time_limit:
        return "TIMEOUT", None
    
    # Límite máximo de profundidad para evitar recursión infinita
    if depth <= 0 or depth > 20: 
        return evaluation_func(board_state, player_id, weights_config), None
    
    if rules_func.check_game_over(board_state) != 0:
        return evaluation_func(board_state, player_id, weights_config), None
    
    movimientos_posibles = []
    if is_maximizing:
        current_turn_player_id = player_id
    else:
        current_turn_player_id = 2 if player_id == 1 else 1

    if current_turn_player_id == 1:
        rango_huecos = range(0, 7)
    else:
        rango_huecos = range(8, 15)

    for hueco in rango_huecos:
        if board_state[hueco] > 0:
            movimientos_posibles.append(hueco)

    # Si no hay movimientos posibles, evaluar el estado actual
    if not movimientos_posibles:
        return evaluation_func(board_state, player_id, weights_config), None

    if is_maximizing:
        best_score, best_move = -math.inf, None
        for move in movimientos_posibles:
            new_board, turn_result = logic_func(list(board_state), move, current_turn_player_id)
            if turn_result == "TURNO_EXTRA":
                score, _ = minimax_search(
                    new_board, player_id, depth, alpha, beta, True, 
                    time_limit, start_time, evaluation_func, logic_func, rules_func, weights_config
                )
            elif turn_result == "FIN_TURNO":
                score, _ = minimax_search(
                    new_board, player_id, depth - 1, alpha, beta, False, 
                    time_limit, start_time, evaluation_func, logic_func, rules_func, weights_config
                )
            if score == "TIMEOUT":
                return "TIMEOUT", None

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # ¡Poda!
        return best_score, best_move
    
    else:
        best_score, best_move = math.inf, None
        for move in movimientos_posibles:
            new_board, turn_result = logic_func(list(board_state), move, current_turn_player_id)
            if turn_result == "TURNO_EXTRA":
                score, _ = minimax_search(
                    new_board, player_id, depth, alpha, beta, False, 
                    time_limit, start_time, evaluation_func, logic_func, rules_func, weights_config
                )
            elif turn_result == "FIN_TURNO":
                score, _ = minimax_search(
                    new_board, player_id, depth - 1, alpha, beta, True, 
                    time_limit, start_time, evaluation_func, logic_func, rules_func, weights_config
                )
            if score == "TIMEOUT":
                return "TIMEOUT", None

            if score < best_score:
                best_score = score
                best_move = move

            beta = min(beta, best_score)
            if beta <= alpha:
                break  # ¡Poda!
        return best_score, best_move
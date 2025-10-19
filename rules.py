def check_game_over(board_state: list) -> int:
    sum_huecos_J1 = sum(board_state[0:7])
    sum_huecos_J2 = sum(board_state[8:15])
    
    if sum_huecos_J1 == 0:
        valor = 1
    elif sum_huecos_J2 == 0:
        valor = 2
    else:
        valor = 0
    return valor

def final_sweep(board_state: list, side_empty:int)->list:
    
    if side_empty == 1:
        board_state[15] += sum(board_state[8:15])
        board_state[8:15] = [0] * 7     
    
    if side_empty == 2:
        board_state[7] += sum(board_state[0:7])
        board_state[0:7] = [0] * 7   

    return board_state

def declare_winner(score_p1: int, score_p2: int) -> str:
    
    if score_p1 > score_p2:
        mensaje = "¡Jugador 1 Gana!"
    
    elif score_p2 > score_p1:
        mensaje = "¡Jugador 2 Gana!"
    
    else:
        mensaje = "¡Es un Empate!"

    return mensaje

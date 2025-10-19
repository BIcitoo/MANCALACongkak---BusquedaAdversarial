import logic
import rules
from board import MancalaBoard

def get_player_input(current_player: int, board_state: list) -> int:
    while True:
        try:
            if current_player == 1:
                print("Jugador 1, elige un hueco (0-6):")
                chosen_pit = int(input())
                if chosen_pit < 0 or chosen_pit > 6:
                    print("Error: Debe elegir un hueco entre 0 y 6")
                    continue
            else:
                print("Jugador 2, elige un hueco (8-14):")
                chosen_pit = int(input())
                if chosen_pit < 8 or chosen_pit > 14:
                    print("Error: Debe elegir un hueco entre 8 y 14")
                    continue
            
            if board_state[chosen_pit] == 0:
                print("Error: El hueco elegido esta vacio")
                continue
            
            return chosen_pit
            
        except ValueError:
            print("Error: Debe ingresar un numero valido")

def play_game():
    mi_tablero = MancalaBoard(piedras_iniciales=7)
    current_player = 1
    
    while True:
        print("\n" * 50)
        mi_tablero.imprimir_tablero_ascii()
        
        game_status = rules.check_game_over(mi_tablero.board)
        if game_status != 0:
            break
        
        print(f"Turno del Jugador {current_player}")
        chosen_pit = get_player_input(current_player, mi_tablero.board)
        
        new_board, move_result = logic.hacer_movimiento(mi_tablero.board, chosen_pit, current_player)
        mi_tablero.board = new_board
        
        if move_result == "TURNO_EXTRA":
            print("Turno extra! Continua el mismo jugador")
            continue
        
        current_player = 2 if current_player == 1 else 1
    
    print("Juego Terminado!")
    final_board = rules.final_sweep(mi_tablero.board, game_status)
    mi_tablero.board = final_board
    
    score_p1 = final_board[7]
    score_p2 = final_board[15]
    
    print(rules.declare_winner(score_p1, score_p2))
    print(f"Puntaje final - Jugador 1: {score_p1}, Jugador 2: {score_p2}")

if __name__ == "__main__":
    play_game()

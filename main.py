import logic
import rules
from board import MancalaBoard
import sys
import os

# Agregar el directorio Minimax al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'Minimax'))

from MINIMAX.agent_ai import AgentMinimax

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

def get_game_mode():
    """Solicita al usuario que elija el modo de juego."""
    print("=" * 50)
    print("MODOS DE JUEGO DISPONIBLES")
    print("=" * 50)
    print("1. Humano vs Humano")
    print("2. Humano vs IA")
    print("3. IA vs IA")
    print("=" * 50)
    
    while True:
        try:
            modo = int(input("Selecciona el modo de juego (1-3): "))
            if modo in [1, 2, 3]:
                return modo
            else:
                print("Error: Debe seleccionar un modo entre 1 y 3")
        except ValueError:
            print("Error: Debe ingresar un numero valido")

def get_ai_difficulty():
    """Solicita al usuario que elija la dificultad de la IA."""
    print("\n" + "=" * 30)
    print("DIFICULTAD DE LA IA")
    print("=" * 30)
    print("1. Facil (2 segundos)")
    print("2. Medio (5 segundos)")
    print("3. Dificil (10 segundos)")
    print("=" * 30)
    
    while True:
        try:
            dificultad = int(input("Selecciona la dificultad (1-3): "))
            if dificultad == 1:
                return 2.0
            elif dificultad == 2:
                return 5.0
            elif dificultad == 3:
                return 10.0
            else:
                print("Error: Debe seleccionar una dificultad entre 1 y 3")
        except ValueError:
            print("Error: Debe ingresar un numero valido")

def play_game():
    # Seleccionar modo de juego
    modo = get_game_mode()
    
    # Configurar IA si es necesario
    ai_player1 = None
    ai_player2 = None
    time_limit = 5.0
    
    if modo == 2:  # Humano vs IA
        time_limit = get_ai_difficulty()
        ai_player2 = AgentMinimax({
            'w1': 10.0,  # Diferencial de puntuacion
            'w2': 50.0,  # Turnos extra
            'w3': 0.8,   # Movilidad
            'w4': -0.5,  # Hambre del oponente
            'w5': 1.5    # Control del hueco clave
        })
        print(f"\nJugador 1: Humano")
        print(f"Jugador 2: IA (Dificultad: {time_limit}s)")
        
    elif modo == 3:  # IA vs IA
        time_limit = get_ai_difficulty()
        ai_player1 = AgentMinimax({
            'w1': 10.0, 'w2': 50.0, 'w3': 0.8, 'w4': -0.5, 'w5': 1.5
        })
        ai_player2 = AgentMinimax({
            'w1': 10.0, 'w2': 50.0, 'w3': 0.8, 'w4': -0.5, 'w5': 1.5
        })
        print(f"\nJugador 1: IA")
        print(f"Jugador 2: IA")
        print(f"Tiempo por movimiento: {time_limit}s")
    
    # Inicializar juego
    mi_tablero = MancalaBoard(piedras_iniciales=7)
    current_player = 1
    
    while True:
        print("\n" * 50)
        mi_tablero.imprimir_tablero_ascii()
        
        game_status = rules.check_game_over(mi_tablero.board)
        if game_status != 0:
            break
        
        print(f"Turno del Jugador {current_player}")
        
        # Determinar si el jugador actual es IA
        if current_player == 1 and ai_player1 is not None:
            print("IA pensando...")
            chosen_pit = ai_player1.elegir_movimiento(mi_tablero.board, current_player, time_limit)
            if chosen_pit is None:
                print("Error: IA no pudo encontrar un movimiento valido")
                # Buscar cualquier movimiento válido como fallback
                valid_moves = [h for h in range(0, 7) if mi_tablero.board[h] > 0]
                if valid_moves:
                    chosen_pit = valid_moves[0]
                    print(f"Usando movimiento de emergencia: {chosen_pit}")
                else:
                    print("No hay movimientos válidos disponibles")
                    break
            print(f"IA eligio el hueco: {chosen_pit}")
            
        elif current_player == 2 and ai_player2 is not None:
            print("IA pensando...")
            chosen_pit = ai_player2.elegir_movimiento(mi_tablero.board, current_player, time_limit)
            if chosen_pit is None:
                print("Error: IA no pudo encontrar un movimiento valido")
                # Buscar cualquier movimiento válido como fallback
                valid_moves = [h for h in range(8, 15) if mi_tablero.board[h] > 0]
                if valid_moves:
                    chosen_pit = valid_moves[0]
                    print(f"Usando movimiento de emergencia: {chosen_pit}")
                else:
                    print("No hay movimientos válidos disponibles")
                    break
            print(f"IA eligio el hueco: {chosen_pit}")
            
        else:
            # Jugador humano
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

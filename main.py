import logic
import rules
from board import MancalaBoard
import sys
import os
import time
import datetime
import csv

# Agregar el directorio MINIMAX al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'MINIMAX'))

from MINIMAX.agent_ai import AgentMinimax
from MINIMAX.agent_greedy import AgentGreedy
from MINIMAX.agent_random import AgentRandom
from MINIMAX.agent_worst import AgentWorst

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
    print("4. IA (Greedy) vs IA (Minimax)")
    print("5. IA (Random) vs IA (Minimax)")
    print("6. IA (Worst) vs IA (Minimax)")
    print("=" * 50)
    
    while True:
        try:
            modo = int(input("Selecciona el modo de juego (1-6): "))
            if modo in [1, 2, 3, 4, 5, 6]:
                return modo
            else:
                print("Error: Debe seleccionar un modo entre 1 y 6")
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

def save_benchmark(stats: dict):
    """Guarda el benchmark directamente en __pycache__/ por modo de juego"""
    
    # Obtener el directorio base donde esta main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cache_dir = os.path.join(script_dir, '__pycache__')
    
    # Mapear modo de juego a nombre de archivo
    modo_map = {
        1: 'humano_vs_humano',
        2: 'humano_vs_ia',
        3: 'ia_vs_ia',
        4: 'greedy_vs_minimax',
        5: 'random_vs_minimax',
        6: 'worst_vs_minimax'
    }
    
    modo_nombre = modo_map.get(stats['mode'], f'modo_{stats["mode"]}')
    csv_file = os.path.join(cache_dir, f'benchmark_{modo_nombre}.csv')
    
    # Crear directorio si no existe
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    # Si el archivo no existe, crear con headers en espanol
    if not os.path.exists(csv_file):
        headers = [
            'timestamp', 'modo_juego', 'jugador1_tipo', 'jugador2_tipo', 'dificultad',
            'ganador_del_juego',
            'cantidad_de_puntos_obtenidos_ganador', 'cantidad_de_puntos_obtenidos_perdedor',
            'cantidad_de_nodos_expandidos_j1', 'cantidad_de_nodos_expandidos_j2',
            'promedio_de_profundidad_j1', 'promedio_de_profundidad_j2',
            'profundidad_total_del_arbol_de_busqueda_j1', 'profundidad_total_del_arbol_de_busqueda_j2',
            'tiempo_de_ejecucion'
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    
    # Calcular datos adicionales
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tipos_jugadores = {
        1: ('Humano', 'Humano'),
        2: ('Humano', 'IA (Minimax)'),
        3: ('IA (Minimax)', 'IA (Minimax)'),
        4: ('IA (Greedy)', 'IA (Minimax)'),
        5: ('IA (Random)', 'IA (Minimax)'),
        6: ('IA (Worst)', 'IA (Minimax)')
    }
    
    j1_tipo, j2_tipo = tipos_jugadores.get(stats['mode'], ('Desconocido', 'Desconocido'))
    
    # Calcular metricas por jugador
    profundidad_promedio_j1 = stats['p1_depth_total'] / stats['p1_moves'] if stats['p1_moves'] > 0 else 0
    profundidad_promedio_j2 = stats['p2_depth_total'] / stats['p2_moves'] if stats['p2_moves'] > 0 else 0
    profundidad_total_j1 = stats['p1_depth_total']
    profundidad_total_j2 = stats['p2_depth_total']
    nodos_expandidos_j1 = stats.get('p1_nodes', 0)
    nodos_expandidos_j2 = stats.get('p2_nodes', 0)
    tiempo_ejecucion = stats.get('total_duration', 0)
    
    # Determinar ganador y puntos
    winner_string = stats.get('winner_string', 'Empate')
    score_p1 = stats.get('score_p1', 0)
    score_p2 = stats.get('score_p2', 0)
    
    # Determinar quien gano
    if 'Jugador 1' in winner_string:
        puntos_ganador = score_p1
        puntos_perdedor = score_p2
        ganador = "Jugador 1"
    elif 'Jugador 2' in winner_string:
        puntos_ganador = score_p2
        puntos_perdedor = score_p1
        ganador = "Jugador 2"
    else:
        puntos_ganador = max(score_p1, score_p2)
        puntos_perdedor = min(score_p1, score_p2)
        ganador = "Empate"
    
    # Mapear time_limit a dificultad
    time_map = {
        2.0: 'Facil',
        5.0: 'Intermedio',
        10.0: 'Dificil'
    }
    dificultad = time_map.get(stats.get('time_limit', 5.0), 'Intermedio')
    
    # Escribir datos en CSV con nombres en espanol
    row = [
        timestamp,
        stats.get('mode', 0),
        j1_tipo,
        j2_tipo,
        dificultad,
        ganador,
        puntos_ganador,  # cantidad_de_puntos_obtenidos_ganador
        puntos_perdedor,  # cantidad_de_puntos_obtenidos_perdedor
        nodos_expandidos_j1,  # cantidad_de_nodos_expandidos_j1
        nodos_expandidos_j2,  # cantidad_de_nodos_expandidos_j2
        profundidad_promedio_j1,  # promedio_de_profundidad_j1
        profundidad_promedio_j2,  # promedio_de_profundidad_j2
        profundidad_total_j1,  # profundidad_total_del_arbol_de_busqueda_j1
        profundidad_total_j2,  # profundidad_total_del_arbol_de_busqueda_j2
        tiempo_ejecucion  # tiempo_de_ejecucion
    ]
    
    # Append al archivo
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    
    print(f"\n{'='*60}")
    print(f"✓ Benchmark guardado en:")
    print(f"  {csv_file}")
    print(f"✓ Tiempo total de partida: {stats.get('total_duration', 0):.2f} segundos")
    print(f"{'='*60}")

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
        print(f"\n✓ Modo seleccionado: Humano vs IA")
        print(f"  Jugador 1: Humano")
        print(f"  Jugador 2: IA (Minimax) - Tiempo: {time_limit}s")
        
    elif modo == 3:  # IA vs IA
        time_limit = get_ai_difficulty()
        ai_player1 = AgentMinimax({
            'w1': 10.0, 'w2': 50.0, 'w3': 0.8, 'w4': -0.5, 'w5': 1.5
        })
        ai_player2 = AgentMinimax({
            'w1': 10.0, 'w2': 50.0, 'w3': 0.8, 'w4': -0.5, 'w5': 1.5
        })
        print(f"\n✓ Modo seleccionado: IA vs IA")
        print(f"  Jugador 1: IA (Minimax)")
        print(f"  Jugador 2: IA (Minimax)")
        print(f"  Tiempo por movimiento: {time_limit}s")

    elif modo == 4:
        time_limit = get_ai_difficulty()
        ai_player1 = AgentGreedy()
        ai_player2 = AgentMinimax({
            'w1': 10.0,  # Diferencial de puntuacion
            'w2': 50.0,  # Turnos extra
            'w3': 0.8,   # Movilidad
            'w4': -0.5,  # Hambre del oponente
            'w5': 1.5    # Control del hueco clave
        })
        print(f"\n✓ Modo seleccionado: Greedy vs Minimax")
        print(f"  Jugador 1: IA (Greedy)")
        print(f"  Jugador 2: IA (Minimax)")
        print(f"  Tiempo para Minimax: {time_limit}s")
    
    elif modo == 5:
        time_limit = get_ai_difficulty()
        ai_player1 = AgentRandom()
        ai_player2 = AgentMinimax({
            'w1': 10.0,  # Diferencial de puntuacion
            'w2': 50.0,  # Turnos extra
            'w3': 0.8,   # Movilidad
            'w4': -0.5,  # Hambre del oponente
            'w5': 1.5    # Control del hueco clave
        })
        print(f"\n✓ Modo seleccionado: Random vs Minimax")
        print(f"  Jugador 1: IA (Random)")
        print(f"  Jugador 2: IA (Minimax)")
        print(f"  Tiempo para Minimax: {time_limit}s")
    
    elif modo == 6:
        time_limit = get_ai_difficulty()
        ai_player1 = AgentWorst()
        ai_player2 = AgentMinimax({
            'w1': 10.0,  # Diferencial de puntuacion
            'w2': 50.0,  # Turnos extra
            'w3': 0.8,   # Movilidad
            'w4': -0.5,  # Hambre del oponente
            'w5': 1.5    # Control del hueco clave
        })
        print(f"\n✓ Modo seleccionado: Worst vs Minimax")
        print(f"  Jugador 1: IA (Worst)")
        print(f"  Jugador 2: IA (Minimax)")
        print(f"  Tiempo para Minimax: {time_limit}s")
    
    # Guardar configuracion para mostrar tipos de jugadores
    if ai_player1 is None:
        jugador1_tipo = "Humano"
    elif isinstance(ai_player1, AgentMinimax):
        jugador1_tipo = "IA (Minimax)"
    elif isinstance(ai_player1, AgentGreedy):
        jugador1_tipo = "IA (Greedy)"
    elif isinstance(ai_player1, AgentRandom):
        jugador1_tipo = "IA (Random)"
    elif isinstance(ai_player1, AgentWorst):
        jugador1_tipo = "IA (Worst)"
    else:
        jugador1_tipo = "IA (Desconocido)"
    
    if ai_player2 is None:
        jugador2_tipo = "Humano"
    elif isinstance(ai_player2, AgentMinimax):
        jugador2_tipo = "IA (Minimax)"
    elif isinstance(ai_player2, AgentGreedy):
        jugador2_tipo = "IA (Greedy)"
    elif isinstance(ai_player2, AgentRandom):
        jugador2_tipo = "IA (Random)"
    elif isinstance(ai_player2, AgentWorst):
        jugador2_tipo = "IA (Worst)"
    else:
        jugador2_tipo = "IA (Desconocido)"
    
    # Mostrar configuracion final
    print("\n" + "="*50)
    print("CONFIGURACION DE PARTIDA")
    print("="*50)
    print(f"Jugador 1: {jugador1_tipo}")
    print(f"Jugador 2: {jugador2_tipo}")
    if ai_player1 is not None or ai_player2 is not None:
        print(f"Tiempo por movimiento: {time_limit}s")
    print("="*50)
    
    # Inicializar juego
    mi_tablero = MancalaBoard(piedras_iniciales=7)
    current_player = 1

    game_start_time = time.time()
    game_stats = {
        'p1_nodes': 0, 'p1_depth_total': 0, 'p1_moves': 0,
        'p2_nodes': 0, 'p2_depth_total': 0, 'p2_moves': 0,
        'mode': modo, 'time_limit': time_limit
    }
    
    while True:
        # Limpiar pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Mostrar quien esta jugando
        if current_player == 1:
            jugador_actual = jugador1_tipo
        else:
            jugador_actual = jugador2_tipo
        
        print(f"\n{'='*60}")
        print(f"Turno del Jugador {current_player} ({jugador_actual})")
        print(f"{'='*60}\n")
        
        # Imprimir tablero
        mi_tablero.imprimir_tablero_ascii()
        
        game_status = rules.check_game_over(mi_tablero.board)
        if game_status != 0:
            break
        
        # Determinar si el jugador actual es IA
        if current_player == 1 and ai_player1 is not None:
            # Determinar tipo de agente
            if isinstance(ai_player1, AgentMinimax):
                print("IA (Minimax) pensando...")
            elif isinstance(ai_player1, AgentGreedy):
                print("IA (Greedy) pensando...")
            elif isinstance(ai_player1, AgentRandom):
                print("IA (Random) pensando...")
            elif isinstance(ai_player1, AgentWorst):
                print("IA (Worst) pensando...")
            else:
                print("IA pensando...")
            
            chosen_pit, move_stats = ai_player1.elegir_movimiento(mi_tablero.board, current_player, time_limit)
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
            # Determinar tipo de agente
            if isinstance(ai_player2, AgentMinimax):
                print("IA (Minimax) pensando...")
            elif isinstance(ai_player2, AgentGreedy):
                print("IA (Greedy) pensando...")
            elif isinstance(ai_player2, AgentRandom):
                print("IA (Random) pensando...")
            elif isinstance(ai_player2, AgentWorst):
                print("IA (Worst) pensando...")
            else:
                print("IA pensando...")
            
            chosen_pit, move_stats = ai_player2.elegir_movimiento(mi_tablero.board, current_player, time_limit)
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
            print(f"Humano {current_player} pensando...")
            chosen_pit = get_player_input(current_player, mi_tablero.board)
            move_stats = {}  # No hay estadísticas para humanos
        
        new_board, move_result = logic.hacer_movimiento(mi_tablero.board, chosen_pit, current_player)
        mi_tablero.board = new_board
        
        # Actualizar estadisticas ANTES de cambiar de jugador
        if current_player == 1:
            game_stats['p1_nodes'] += move_stats.get('nodes_expanded', 0)
            game_stats['p1_depth_total'] += move_stats.get('depth_reached', 0)
            if move_stats: # Solo cuenta si fue un movimiento de IA
                game_stats['p1_moves'] += 1
        else: # current_player == 2
            game_stats['p2_nodes'] += move_stats.get('nodes_expanded', 0)
            game_stats['p2_depth_total'] += move_stats.get('depth_reached', 0)
            if move_stats: # Solo cuenta si fue un movimiento de IA
                game_stats['p2_moves'] += 1
        
        if move_result == "TURNO_EXTRA":
            print("Turno extra! Continua el mismo jugador")
            continue
        
        # Cambiar de jugador SOLO si no hay turno extra
        current_player = 2 if current_player == 1 else 1
    
    print("Juego Terminado!")
    final_board = rules.final_sweep(mi_tablero.board, game_status)
    mi_tablero.board = final_board
    
    score_p1 = final_board[7]
    score_p2 = final_board[15]
    
    print(rules.declare_winner(score_p1, score_p2))
    print(f"Puntaje final - Jugador 1: {score_p1}, Jugador 2: {score_p2}")

    game_stats['total_duration'] = time.time() - game_start_time
    game_stats['winner_string'] = rules.declare_winner(score_p1, score_p2)
    game_stats['score_p1'] = score_p1
    game_stats['score_p2'] = score_p2

    # Guardar benchmark
    save_benchmark(game_stats)

if __name__ == "__main__":
    play_game()

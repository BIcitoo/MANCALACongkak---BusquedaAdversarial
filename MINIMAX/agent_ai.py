"""
agent_ai.py

AgentMinimax: envoltorio que aplica IDS (Iterative Deepening Search) y
gestiona el límite de tiempo global para la búsqueda.
"""

import time
import math
from typing import Any, Optional

from ai_core import minimax_search
from evaluation import evaluate
import logic
import rules

class AgentMinimax:
    """
    Agente que selecciona movimientos usando Minimax + Alpha-Beta y IDS.

    weights_config: dict con parámetros que se pasarán a la función de evaluación.
    """
    def __init__(self, weights_config: dict):
        self.weights = weights_config
        self.eval_func = evaluate
        self.logic_func = logic.hacer_movimiento
        self.rules_func = rules

    def elegir_movimiento(self, board_state: Any, current_player: int, time_limit: float) -> Optional[int]:
        """
        Ejecuta Iterative Deepening y devuelve el mejor movimiento encontrado
        antes de que el tiempo expire.

        Parámetros:
            board_state: estado actual del tablero (tipo libre, p.ej. lista/tupla)
            current_player: id del jugador que mueve (1 o 2)
            time_limit: tiempo máximo en segundos para la decisión

        Devuelve:
            final_move: el movimiento seleccionado, o None si no se encontró ninguno.
        """
        start_time = time.time()
        final_move = None

        # IDS: profundidades crecientes (límite máximo de 15)
        for depth in range(1, 16):
            try:
                print(f"Buscando a profundidad: {depth}")

                result = minimax_search(
                    board_state,
                    current_player,
                    depth,
                    -math.inf,
                    math.inf,
                    True,  # asumimos que iniciamos con maximizing player
                    time_limit,
                    start_time,
                    self.eval_func,
                    self.logic_func,
                    self.rules_func,
                    self.weights,
                )

                # Normalizamos la respuesta esperada
                if isinstance(result, tuple) and len(result) == 2:
                    score, move = result
                else:
                    score, move = result, None

                if score == "TIMEOUT":
                    print(f"Tiempo agotado. Usando mejor movimiento de profundidad {depth-1}")
                    break

                # Guardar la mejor jugada encontrada en esta profundidad
                if move is not None:
                    final_move = move

                # Comprobación de seguridad: si ya se excedió el tiempo, salir.
                elapsed = time.time() - start_time
                if elapsed >= time_limit:
                    print(f"Tiempo total ({elapsed:.3f}s) >= límite ({time_limit}s). Terminando IDS.")
                    break

            except TimeoutError:
                print(f"TimeoutError capturado en profundidad {depth}. Usando mejor movimiento de profundidad {depth-1}")
                break
            except Exception as e:
                # Registrar excepción y devolver la mejor jugada disponible
                print(f"Excepción durante minimax_search a profundidad {depth}: {e}")
                break

        return final_move

if __name__ == "__main__":
    # Ejemplo de uso rápido (no funcional sin el resto del motor)
    ejemplo_pesos = {"peso_material": 1.0, "peso_posicional": 0.5}
    agente = AgentMinimax(ejemplo_pesos)
    tablero_ejemplo = [0] * 15  # ejemplo mínimo; rellena según tu representación
    jugador_actual = 1
    print("Agent creado. Llamada de ejemplo (no funcional sin lógica completa).")

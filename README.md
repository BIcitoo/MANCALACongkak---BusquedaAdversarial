# Juego de Mancala - Variante Congkak

Un juego de Mancala implementado en Python con interfaz de consola y colores, siguiendo las reglas de la variante Congkak.

## Descripcion del Juego

Congkak es una variante de Mancala donde dos jugadores compiten por recolectar la mayor cantidad de piedras en sus almacenes (llamados "rumah" o casa). Cada jugador tiene 7 huecos con piedras y debe distribuir las piedras de un hueco seleccionado en sentido anti-horario, saltando el almacen del oponente.

## Reglas de Congkak

### Preparacion
- El tablero tiene 2x7 huecos (7 por jugador) y 2 almacenes, sumando 16 posiciones totales
- Cada uno de los 14 huecos de juego comienza con 7 piedras (configurable)
- Los almacenes inician vacios

### Movimiento
1. El jugador elige un hueco de su lado que no este vacio (>0 piedras)
2. Recoge todas las piedras de ese hueco
3. Las siembra una por una en sentido anti-horario
4. La siembra incluye el almacen propio, pero salta siempre el almacen del oponente

### Reglas de Aterrizaje
- **Turno Extra**: Si la ultima piedra cae en tu propio almacen, obtienes un turno extra
- **Turno Normal**: Si la ultima piedra cae en cualquier otro hueco (vacio, lleno, tuyo o del rival), tu turno termina
- **Nota Importante**: No existe la "Captura". Si caes en un hueco vacio de tu lado, simplemente termina el turno

### Fin del Juego
- El juego termina inmediatamente cuando, al inicio de su turno, un jugador no tiene piedras en ninguno de sus 7 huecos
- En ese momento, el otro jugador recoge todas las piedras que queden en su lado y las añade a su propio almacen

### Ganador
- El jugador con mas piedras en su almacen al final del juego gana

## Estructura del Tablero

El tablero es una lista de 16 enteros con la siguiente distribucion:

```
Indices 0-6:   Huecos del Jugador 1 (7 huecos)
Indice 7:      Almacen (Casa) del Jugador 1
Indices 8-14:  Huecos del Jugador 2 (7 huecos)
Indice 15:     Almacen (Casa) del Jugador 2
```

## Archivos del Proyecto

### board.py - El Arquitecto del Tablero
Contiene la clase `MancalaBoard` que maneja la representacion visual del tablero.

**Funciones principales:**
- `__init__(piedras_iniciales=7)`: Inicializa el tablero con el numero especificado de piedras por hueco
- `imprimir_tablero_ascii(mostrar_indices=True)`: Muestra el tablero en consola con colores y formato ASCII

**Caracteristicas implementadas:**
- Tablero de 16 posiciones siguiendo la estructura de indices especificada
- Visualizacion con colores usando colorama (verde para J1, magenta para J2, amarillo para huecos)
- Indices numericos para facilitar la seleccion de huecos
- Constantes P1_STORE = 7 y P2_STORE = 15 para referencia rapida

### logic.py - El Ingeniero de Logica
Implementa la logica principal del movimiento de piedras siguiendo las reglas de Congkak.

**Funciones principales:**
- `hacer_movimiento(board_state, pit_index, current_player)`: Ejecuta un movimiento completo

**Logica del movimiento implementada:**
1. Identifica el almacen a saltar segun el jugador actual
2. Toma todas las piedras del hueco seleccionado y lo vacia
3. Distribuye una piedra por hueco en sentido anti-horario
4. Salta el almacen del oponente usando continue
5. Determina si el jugador obtiene un turno extra (si la ultima piedra cae en su almacen)
6. Retorna el tablero actualizado y el estado del movimiento ("TURNO_EXTRA" o "FIN_TURNO")

### rules.py - El Guardian de las Reglas
Maneja las reglas del juego y condiciones de finalizacion.

**Funciones principales:**
- `check_game_over(board_state)`: Verifica si el juego ha terminado
  - Retorna 1 si el jugador 1 se quedo sin piedras (suma de indices 0-6 = 0)
  - Retorna 2 si el jugador 2 se quedo sin piedras (suma de indices 8-14 = 0)
  - Retorna 0 si el juego continua
- `final_sweep(board_state, side_empty)`: Realiza el barrido final de piedras
  - Si side_empty == 1: recoge piedras del J2 (indices 8-14) y las suma al almacen del J2 (indice 15)
  - Si side_empty == 2: recoge piedras del J1 (indices 0-6) y las suma al almacen del J1 (indice 7)
- `declare_winner(score_p1, score_p2)`: Determina y anuncia el ganador

### main.py - El Director del Juego
Archivo principal que integra todos los modulos y ejecuta el juego.

**Funciones principales:**
- `get_player_input(current_player, board_state)`: Solicita y valida la entrada del jugador
  - Valida que la entrada sea un numero entero
  - Verifica el rango correcto (0-6 para J1, 8-14 para J2)
  - Comprueba que el hueco elegido no este vacio
  - Maneja errores con mensajes claros
- `play_game()`: Bucle principal del juego
  - Crea el tablero y establece el jugador inicial
  - Muestra el tablero y verifica condiciones de fin de juego
  - Maneja turnos extra correctamente
  - Ejecuta el barrido final y declara el ganador

**Caracteristicas de la interfaz:**
- Validacion completa de entrada del usuario
- Manejo de errores con mensajes claros
- Limpieza de pantalla entre turnos
- Informacion detallada del estado del juego

## Como Jugar

1. Ejecuta el juego: `python main.py`
2. El tablero se muestra con colores y numeros de posicion
3. En tu turno, elige un hueco de tu lado (0-6 para jugador 1, 8-14 para jugador 2)
4. Las piedras se distribuyen automaticamente en sentido anti-horario
5. Si tu ultima piedra cae en tu almacen, obtienes un turno extra
6. El juego termina cuando un jugador se queda sin piedras en sus huecos
7. Se realiza un barrido final y se declara el ganador

## Estrategias y Heuristicas

Para desarrollar una IA o mejorar el juego, estas son las 5 heuristicas mas efectivas:

### 1. Maximizacion de Puntuacion (Diferencial de Almacen)
**Objetivo**: Tener mas piedras en tu almacen que el oponente
**Implementacion**: `puntuacion = (mi_almacen) - (almacen_oponente)`
**Decision**: Preferir jugadas que maximicen este diferencial

### 2. Prioridad de Turno Extra (Aceleracion)
**Objetivo**: Obtener turnos extra para mantener la iniciativa
**Implementacion**: Simular cada movimiento y dar gran bono a jugadas que devuelvan "TURNO_EXTRA"
**Decision**: A menudo elegir turno extra sobre pequeñas ganancias de puntos

### 3. Movilidad y Control del Tablero (Evitar Quedarse Seco)
**Objetivo**: Mantener opciones de movimiento futuras
**Implementacion**: `movilidad = sum(piedras_en_mis_7_huecos)`
**Decision**: Intentar mantener un buen numero de piedras en juego en tu lado

### 4. Control del Hueco Clave (El Lanzador)
**Objetivo**: Acumular piedras en el hueco mas a la derecha para grandes movimientos
**Implementacion**: `valor_clave = piedras_en_mi_hueco_6` (o 14 para J2)
**Decision**: Preferir jugadas que muevan piedras hacia ese hueco estrategico

### 5. Hambre del Oponente (Juego Defensivo)
**Objetivo**: Reducir las opciones del oponente
**Implementacion**: `hambre = (total_piedras_oponente_antes) - (total_piedras_oponente_despues)`
**Decision**: Realizar jugadas que vacien el lado del rival o reduzcan sus opciones futuras

## Requisitos

- Python 3.6 o superior
- colorama (para colores en consola)

## Instalacion

```bash
pip install colorama
```

## Visualizacion del Tablero

```
   J2    (14)   (13)   (12)   (11)   (10)    (9)    (8)
| 00 | [ 7 ] [ 7 ] [ 7 ] [ 7 ] [ 7 ] [ 7 ] [ 7 ] | 00 |
 ⟳—————————————————————————————————————————————————⟲
|    | [ 7 ] [ 7 ] [ 7 ] [ 7 ] [ 7 ] [ 7 ] [ 7 ] |    |
   J1     (0)    (1)    (2)    (3)    (4)    (5)    (6)
```

**Leyenda:**
- Los numeros entre parentesis son los indices que debes usar para seleccionar huecos
- Los numeros en corchetes muestran las piedras en cada hueco
- Los numeros en las barras verticales son los almacenes (puntuacion)
- La flecha indica la direccion de movimiento (anti-horario)

## Desarrollo del Proyecto

Este proyecto fue desarrollado siguiendo una arquitectura modular donde cada archivo tiene una responsabilidad especifica:

- **board.py**: Arquitecto del tablero - maneja la representacion visual
- **logic.py**: Ingeniero de logica - implementa las reglas de movimiento
- **rules.py**: Guardian de las reglas - maneja condiciones de fin de juego
- **main.py**: Director del juego - integra todos los modulos

Esta separacion permite trabajo en paralelo y facilita el mantenimiento del codigo.

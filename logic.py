def hacer_movimiento(board_state, pit_index, current_player):
        P1_Store = 7
        P2_Store = 15
        almacen_saltar = None

        if current_player == 1:
            almacen_saltar = P2_Store
        elif current_player == 2:
            almacen_saltar = P1_Store
        
        piedras = board_state[pit_index]

        board_state[pit_index] = 0

        while piedras > 0:
            pit_index +=1
            
            if pit_index > 15:
                pit_index = 0
            
            if pit_index == almacen_saltar:
                continue 

            board_state[pit_index] += 1
            piedras -=1

        last_stone = pit_index

        if last_stone == P1_Store and current_player == 1:
            estado = "TURNO_EXTRA"
        elif last_stone == P2_Store and current_player == 2:
            estado = "TURNO_EXTRA"
        else:
            estado = "FIN_TURNO"

        return board_state, estado
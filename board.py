from colorama import Fore, Style, init
init(autoreset=True)

class MancalaBoard:
    def __init__(self, piedras_iniciales=7):
        self.board = [piedras_iniciales] * 16
        self.P1_STORE = 7
        self.P2_STORE = 15
        self.board[self.P1_STORE] = 0
        self.board[self.P2_STORE] = 0

    def imprimir_tablero_ascii(self, mostrar_indices=True):
        huecos_p2 = self.board[8:15][::-1]
        huecos_p1 = self.board[0:7]
        almacen_p1 = self.board[self.P1_STORE]
        almacen_p2 = self.board[self.P2_STORE]

        formato_hueco = lambda n: f" [ {n:^2}] "
        formato_almacen = lambda n, color: f"{color}| {n:02d} |{Style.RESET_ALL}"

        if mostrar_indices:
            print(Fore.CYAN + "   J2    (14)   (13)   (12)   (11)   (10)    (9)    (8)" + Style.RESET_ALL)

        linea_p2 = f" {formato_almacen(almacen_p2, Fore.MAGENTA)} "
        linea_p2 += "".join([Fore.YELLOW + formato_hueco(c) + Style.RESET_ALL for c in huecos_p2])
        linea_p2 += f" {formato_almacen(almacen_p1, Fore.GREEN)}"
        print(linea_p2)

        print(" " * 6 + Fore.CYAN + "⟳" + "—" * 51 + "⟲" + Style.RESET_ALL)

        linea_p1 = " |    | "
        linea_p1 += "".join([Fore.YELLOW + formato_hueco(c) + Style.RESET_ALL for c in huecos_p1])
        linea_p1 += " |    |"
        print(linea_p1)

        if mostrar_indices:
            print(Fore.CYAN + "          (0)    (1)    (2)    (3)    (4)    (5)    (6)     J1" + Style.RESET_ALL)

        print("\n" + "=" * 50)
        print(f"{Fore.GREEN}Puntajes:{Style.RESET_ALL}  J1 (Almacén 7): {almacen_p1}  |  J2 (Almacén 15): {almacen_p2}")

if __name__ == "__main__":
    tablero = MancalaBoard(piedras_iniciales=7)
    tablero.board[15] = 12
    tablero.board[7] = 5


    print("\n" + "=" * 50)
    print("TABLERO DE MANCALA (VARIANTE CONGKAK)")
    tablero.imprimir_tablero_ascii()

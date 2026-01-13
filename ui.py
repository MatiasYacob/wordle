from rich.console import Console
from rich.prompt import Prompt
from config import TITULO_ASCII
from render import armar_panel
from storage import texto_estadisticas
from game import jugar


# ============================================================
#                    INTERFAZ
# ============================================================

# Muestra un mensaje dentro de un panel y espera que el usuario presione Enter
def pantalla(consola, titulo, mensaje):
    consola.clear()
    consola.print(armar_panel(titulo, mensaje))
    input("Enter para volver...")


# Muestra el menu principal y maneja las opciones del juego
def menu():
    consola = Console()

    while True:
        consola.clear()
        consola.print(TITULO_ASCII, style="green")

        consola.print(
            armar_panel(
                "Wordle",
                "1) Jugar\n2) Ver estadisticas\n3) Salir",
            )
        )

        opcion = Prompt.ask("Elegir una opcion", choices=["1", "2", "3"])

        if opcion == "1":
            resultado = jugar(consola)
            pantalla(consola, "Resultado", resultado)
        elif opcion == "2":
            pantalla(consola, "Estadisticas", texto_estadisticas())
        else:
            consola.print("Chau")
            break

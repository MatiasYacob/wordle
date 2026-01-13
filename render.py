# Utilidades de renderizado (colores y paneles)

from rich.panel import Panel


# Devuelve una letra con el color correspondiente segun el resultado
def pintar_letra(letra, color):
    estilos = {
        "verde": "bold green",
        "amarillo": "bold yellow",
        "rojo": "bold red",
    }
    return f"[{estilos[color]}]{letra}[/]"


# Devuelve un Panel ya armado para mostrar mensajes
def armar_panel(titulo, mensaje, borde="green"):
    return Panel(str(mensaje), title=titulo, border_style=borde)

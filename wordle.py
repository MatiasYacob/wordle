# ============================================================
#                    IMPORTACIONES
# ============================================================

import requests              # Para consultar la API de la RAE
import csv                   # Para guardar partidas en CSV
from pathlib import Path     # Para manejar archivos
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt


# ============================================================
#                CONFIGURACION DE CONSOLA
# ============================================================

consola = Console()


# ============================================================
#                    ASCII ART
# ============================================================

TITULO_ASCII = """
░██╗░░░░░░░██╗░█████╗░██████╗░██████╗░██╗░░░░░███████╗██╗
░██║░░██╗░░██║██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔════╝██║
░╚██╗████╗██╔╝██║░░██║██████╔╝██║░░██║██║░░░░░█████╗░░██║
░░████╔═████║░██║░░██║██╔══██╗██║░░██║██║░░░░░██╔══╝░░╚═╝
░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║██████╔╝███████╗███████╗██╗
░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝╚═════╝░╚══════╝╚══════╝╚═╝
Powered by RAE
""".strip("\n")



# ============================================================
#            MANEJO DE PARTIDAS (CSV)
# ============================================================

# Lee todas las partidas guardadas en el archivo CSV y las devuelve como una lista
def leer_partidas():
    ARCHIVO_DATOS = "wordle_data.csv"
    ruta = Path(ARCHIVO_DATOS)
    if not ruta.exists():
        return []
    with ruta.open("r", newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))

# Agrega una fila con una partida nueva al archivo CSV
def guardar_fila_partida(fila):
    CAMPOS_CSV = [
    "timestamp",
    "palabra",
    "largo",
    "gano",
    "intentos",
    "racha_actual",
    "mejor_racha"
                ]
    ARCHIVO_DATOS = "wordle_data.csv"
    ruta = Path(ARCHIVO_DATOS)
    existe = ruta.exists()

    with ruta.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_CSV)
        if not existe:
            escritor.writeheader()
        escritor.writerow(fila)

# Calcula cuantas partidas se jugaron, cuantas se ganaron y las rachas
def calcular_estadisticas(partidas):
    estadisticas = {
        "jugadas": 0,
        "ganadas": 0,
        "racha_actual": 0,
        "mejor_racha": 0
    }

    for partida in partidas:
        estadisticas["jugadas"] += 1

        if partida["gano"] == "1":
            estadisticas["ganadas"] += 1
            estadisticas["racha_actual"] += 1
            if estadisticas["racha_actual"] > estadisticas["mejor_racha"]:
                estadisticas["mejor_racha"] = estadisticas["racha_actual"]
        else:
            estadisticas["racha_actual"] = 0

    return estadisticas

# Guarda una partida nueva y actualiza la racha actual y la mejor racha
def registrar_partida(palabra, gano, intentos_usados):
    partidas = leer_partidas()
    stats = calcular_estadisticas(partidas)

    nueva_racha = stats["racha_actual"] + 1 if gano else 0
    mejor_racha = max(stats["mejor_racha"], nueva_racha)

    fila = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "palabra": palabra,
        "largo": len(palabra),
        "gano": "1" if gano else "0",
        "intentos": intentos_usados,
        "racha_actual": nueva_racha,
        "mejor_racha": mejor_racha
    }

    guardar_fila_partida(fila)

# Devuelve un texto con todas las estadisticas formateadas para mostrar en pantalla
def texto_estadisticas():
    partidas = leer_partidas()
    stats = calcular_estadisticas(partidas)
    porcentaje = (stats["ganadas"] / stats["jugadas"] * 100) if stats["jugadas"] else 0

    return (
        f"Jugadas: {stats['jugadas']}\n"
        f"Ganadas: {stats['ganadas']}\n"
        f"Porcentaje: {porcentaje:.1f}%\n"
        f"Racha actual: {stats['racha_actual']}\n"
        f"Mejor racha: {stats['mejor_racha']}"
    )


# ============================================================
#              COLORES PARA LAS LETRAS
# ============================================================

# Devuelve una letra con el color correspondiente segun el resultado
def pintar_letra(letra, color):
    estilos = {
        "verde": "bold green",
        "amarillo": "bold yellow",
        "rojo": "bold red"
    }
    return f"[{estilos[color]}]{letra}[/]"


# ============================================================
#               API DE LA RAE
# ============================================================

class RAEApi:
    URL_RANDOM = "https://rae-api.com/api/random"
    URL_WORDS = "https://rae-api.com/api/words"
    
    # Quita los acentos de una palabra para poder compararla correctamente
    def quitar_acentos(self, texto):
        return texto.translate(str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU"))

    # Obtiene una palabra aleatoria de la RAE segun el largo pedido
    def obtener_palabra(self, largo=None, minimo=None, maximo=None):
        
        parametros = {}

        if largo is not None:
            parametros["min_length"] = largo
            parametros["max_length"] = largo
        else:
            if minimo is not None:
                parametros["min_length"] = minimo
            if maximo is not None:
                parametros["max_length"] = maximo

        respuesta = requests.get(self.URL_RANDOM, params=parametros, timeout=10)
        datos = respuesta.json()

        return self.quitar_acentos(datos["data"]["word"]).lower()

    # Obtiene una palabra aleatoria de la RAE y su significado
    def obtener_palabra_y_significado(self, largo):
        # 1) pedir palabra random
        r = requests.get(
            self.URL_RANDOM,
            params={"min_length": largo, "max_length": largo},
            timeout=10
        )
        palabra = r.json()["data"]["word"]

        # 2) pedir definicion
        r = requests.get(f"{self.URL_WORDS}/{palabra}", timeout=10)
        datos = r.json()

        try:
            significado = datos["data"]["meanings"][0]["senses"][0]["description"]
        except Exception:
            significado = "No hay definicion disponible"

        # Normalizar palabra para el juego
        palabra = self.quitar_acentos(palabra).lower()

        return palabra, significado


rae = RAEApi()


# ============================================================
#               LOGICA DEL JUEGO
# ============================================================

# Le pregunta al jugador cuantas letras quiere y obtiene una palabra con ese largo
def elegir_largo_palabra():
    largo = IntPrompt.ask("Cuantas letras debe tener la palabra", default=6)
    if largo < 2:
        largo = 2
    return rae.obtener_palabra_y_significado(largo)

# Controla toda la logica de una partida de Wordle
def jugar():
    MAX_INTENTOS = 6
    palabra, significado = elegir_largo_palabra()
    largo = len(palabra)

    gano = False
    intento_actual = 0

    tablero = [["◻" for _ in range(largo)] for _ in range(MAX_INTENTOS)]

    while not gano and intento_actual < MAX_INTENTOS:
        intento = input(f"Ingrese una palabra de {largo} letras: ").strip().lower()

        while len(intento) != largo:
            print(f"La palabra debe tener {largo} letras")
            intento = input(f"Ingrese una palabra de {largo} letras: ").strip().lower()

        if intento == palabra:
            tablero[intento_actual] = [pintar_letra(l, "verde") for l in intento]
            gano = True
        else:
            fila = []
            for i in range(largo):
                if intento[i] == palabra[i]:
                    fila.append(pintar_letra(intento[i], "verde"))
                elif intento[i] in palabra:
                    fila.append(pintar_letra(intento[i], "amarillo"))
                else:
                    fila.append(pintar_letra(intento[i], "rojo"))
            tablero[intento_actual] = fila

        consola.clear()
        for fila in tablero:
            consola.print(" ".join(fila))

        intento_actual += 1

    intentos_usados = intento_actual if gano else 0
    registrar_partida(palabra, gano, intentos_usados)

    if gano:
        return f"Ganaste\n\nSignificado: {significado}"
    else:
        return f"Perdiste. La palabra era: {palabra}\n\nSignificado: {significado}"


# ============================================================
#                    INTERFAZ
# ============================================================

# Muestra un mensaje dentro de un panel y espera que el usuario presione Enter
def pantalla(titulo, mensaje):
    consola.clear()
    consola.print(Panel(str(mensaje), title=titulo, border_style="green"))
    input("Enter para volver...")

# Muestra el menu principal y maneja las opciones del juego
def menu():
    while True:
        consola.clear()
        consola.print(TITULO_ASCII, style="green")

        consola.print(
            Panel(
                "1) Jugar\n"
                "2) Ver estadisticas\n"
                "3) Salir",
                title="Wordle",
                border_style="green"
            )
        )

        opcion = Prompt.ask("Elegir una opcion", choices=["1", "2", "3"])

        if opcion == "1":
            resultado = jugar()
            pantalla("Resultado", resultado)
        elif opcion == "2":
            pantalla("Estadisticas", texto_estadisticas())
        else:
            consola.print("Chau")
            break




# Este bloque hace que el programa se ejecute solo cuando se corre este archivo directamente
# y no cuando se importa desde otro archivo

if __name__ == "__main__":
    menu()


import csv
from datetime import datetime
from pathlib import Path
from config import ARCHIVO_DATOS, CAMPOS_CSV




# Lee todas las partidas guardadas en el archivo CSV y las devuelve como una lista
def leer_partidas():
    ruta = Path(ARCHIVO_DATOS)
    if not ruta.exists():
        return []
    with ruta.open("r", newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


# Agrega una fila con una partida nueva al archivo CSV
def guardar_fila_partida(fila):
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
        "mejor_racha": 0,
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
        "mejor_racha": mejor_racha,
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

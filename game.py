from rich.prompt import IntPrompt

from config import MAX_INTENTOS
from rae_api import RAEApi
from render import pintar_letra
from storage import registrar_partida


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
def jugar(consola):
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

import requests


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
        respuesta.raise_for_status()
        datos = respuesta.json()

        return self.quitar_acentos(datos["data"]["word"]).lower()

    # Obtiene una palabra aleatoria de la RAE y su significado
    def obtener_palabra_y_significado(self, largo):
        # 1) pedir palabra random
        r = requests.get(
            self.URL_RANDOM,
            params={"min_length": largo, "max_length": largo},
            timeout=10,
        )
        r.raise_for_status()
        palabra = r.json()["data"]["word"]

        # 2) pedir definicion
        r = requests.get(f"{self.URL_WORDS}/{palabra}", timeout=10)
        r.raise_for_status()
        datos = r.json()

        try:
            significado = datos["data"]["meanings"][0]["senses"][0]["description"]
        except Exception:
            significado = "No hay definicion disponible"

        # Normalizar palabra para el juego
        palabra = self.quitar_acentos(palabra).lower()

        return palabra, significado

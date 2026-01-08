import requests

class RAEApi:
    URL = "https://rae-api.com/api/random"

    #==== Función para obtener una palabra aleatoria ====#
    def get_random_word(self, length=None, min_length=None, max_length=None):
        params = {}

        if length is not None:
            params["min_length"] = length
            params["max_length"] = length
        else:
            if min_length is not None:
                params["min_length"] = min_length
            if max_length is not None:
                params["max_length"] = max_length

        response = requests.get(self.URL, params=params)
        data = response.json()
        return self._quitar_acentos(data["data"]["word"])

    #==== Función para quitar acentos ====#
    def _quitar_acentos(self, texto):
        return texto.translate(
            str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU")
        )

rae = RAEApi()

print(rae.get_random_word(length=7))   # exactamente 7 letras



# wordle
# wordle es un juego de palabras que se juega con una palabra aleatoria
#===iniciar el tablero===#
board = []
for i in range(6):
    board.append(["◻" for _ in range(6)])

#===imprimir el tablero===#
for i in range(6):
    board.append(["◻" for _ in range(6)])
    print (" ".join(board[i]))

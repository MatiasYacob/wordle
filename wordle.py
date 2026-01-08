import requests

#=diccionario de colores==#
colors = {
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'ENDC': '\033[0m',
}
def color_letter(letter, color):
    return colors[color] + letter + colors ['ENDC']


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
win = False
word = "trineo"
board = []
for i in range(6):
    board.append(["◻" for _ in range(6)])
glc = 0
while not win:
    text = input("Introduce una palabra: ")
    while len(text) != len(word):
        if len(text) != len(word):
            print(f"La palabra debe tener {len(word)} letras")
        text = input("Introduce una palabra: ")

    #win logic
    if word == text:
        board[glc] = [l for l in text]
        win = True
    #letter in word
    else:
        test_line = []
        for j in range(len(text)):
            if text[j] == word[j]:
                test_line.append(text[j])
            elif text [j] in word: 
                test_line.append(color_letter(text[j],'yellow'))
            else:
                test_line.append(color_letter(text[j],'red'))
        board[glc] = test_line      
       
    #===imprimir el tablero===#trinio
    for i in range(6):
        board.append(["◻" for _ in range(6)])
        print (" ".join(board[i]))
    glc += 1
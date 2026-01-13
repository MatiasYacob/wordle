# Wordle in Spanish with RAE

A console Wordle game written in Python that uses the Real Academia Espanola (RAE) to fetch real Spanish words and display their meaning at the end of each round.

> Este proyecto fue desarrollado como un desafio propuesto por un companero de la UTN, con el objetivo de poner en practica el uso de APIs, el manejo de datos y la organizacion de un proyecto real en Python.

## Features

- Real Spanish words fetched from the RAE (Real Academia Española)
- Configurable word length
- Wordle-style colored feedback
- CSV-based statistics system
- Shows the real meaning of the word after each round

## Requirements

Install the dependencies:

```bash
pip install requests rich
```

You need Python 3.10 or higher.

## How to run

From the project folder:

```bash
python main.py
```



## How it works

1. A random word is requested from the RAE  
2. Its definition is requested using another endpoint  
3. The player tries to guess the word  
4. At the end of the round the game shows:

```text
The word was: amar
Meaning: Tener amor a alguien o algo
```

## Project structure

```text
main.py
config.py
game.py
ui.py
render.py
rae_api.py
storage.py
wordle_data.csv
.gitignore
README.md
```

## Useful links

- RAE API: https://rae-api.com  
- Rich (console formatting): https://rich.readthedocs.io  
- Python: https://www.python.org 
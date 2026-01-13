# Wordle en Espanol con RAE

Un Wordle en consola hecho en Python que usa la Real Academia Espanola (RAE) para obtener palabras reales y mostrar su significado al final de cada partida.

> La diferencia entre el maestro y el alumno no es el talento: es que el maestro ya se equivoco mas veces de las que el alumno siquiera se atrevio a intentar.

## Caracteristicas

- Palabras reales obtenidas desde la RAE
- Longitud de palabra configurable
- Colores estilo Wordle
- Sistema de estadisticas en CSV
- Muestra el significado real de la palabra al finalizar la ronda

## Requisitos

Instala las dependencias:

```bash
pip install requests rich
```

Necesitas Python 3.10 o superior.

## Como ejecutar

Desde la carpeta del proyecto:

```bash
python wordle.py
```

## Probar la API de la RAE

Podes ejecutar:

```bash
python test_rae.py
```

Eso imprime el JSON crudo que devuelve la RAE, incluyendo definiciones, sinonimos y conjugaciones.

## Como funciona

1. Se pide una palabra aleatoria a la RAE
2. Se consulta su definicion
3. El jugador intenta adivinarla
4. Al final se muestra:

```text
La palabra era: amar
Significado: Tener amor a alguien o algo
```

## Estructura del proyecto

```text
wordle.py
test_rae.py
wordle_data.csv
.gitignore
README.md
```

## Enlaces utiles

- API RAE: https://rae-api.com
- Python: https://www.python.org

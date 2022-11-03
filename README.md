# Clippings

Python module to manipulate Amazon Kindle clippings files.

It allows you to:

* Parse your existing clippings file into a structured representation;
* Generate clippings file programmatically.

[![Latest version released on PyPI](https://img.shields.io/pypi/v/clippings.svg)](https://pypi.org/pypi/clippings)
[![Build status](https://github.com/samueldg/clippings/workflows/Run%20tests/badge.svg)](https://github.com/samueldg/clippings/actions)

## Installation

```sh
pip install clippings
```

## Usage

### Command-line Usage

```sh
# Parse a clippings file
clippings -o json ./clippings.txt

# or from stdin:
cat clippings.txt | clippings -
```

### Programmatic Usage

```py
from clippings import parse_clippings

my_clippings_file = ...
parse_clippings(my_clippings_file)
```

### Want to parse non-English clippings?

Here's a highlight clipping taken from a Kindle that speaks Spanish::

```txt
El Principe de la Niebla (Carlos Ruiz Zafón)
- La subrayado en la página 4 | posición 60-60 | Añadido el miércoles, 6 de julio de 2022 06:54:57

asintiendo a una pregunta que Max no había llegado a formular.
```

`parse_clippings` won't parse this by default but you can write your own parser for 
the second line and pass it to the parameter `metadata_parser`.

You can take a look at an example [here](./examples/bilingual_spanish_english_kindle/main.py).

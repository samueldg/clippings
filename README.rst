Clippings
=========

Python module to manipulate Amazon Kindle clippings files.

It allows you to:

-  Parse your existing clippings file into a structured representation;
-  Generate clippings file programmatically.

|pypi| |build| |coverage|

Installation
------------

.. code:: shell

    pip install clippings

Usage
-----

Command-line Usage
^^^^^^^^^^^^^^^^^^
.. code:: shell

    # Parse a clippings file
    clippings -o dict ./clippings.txt
    
    # or from stdin:
    cat clippings.txt | clippings -

Programmatic Usage
^^^^^^^^^^^^^^^^^^

.. code:: py

    from clippings import parse_clippings

    my_clippings_file = ...
    parse_clippings(my_clippings_file)

Want to parse non-English clippings?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here's a highlight clipping taken from a Kindle that speaks Spanish::

    El Principe de la Niebla (Carlos Ruiz Zafón)
    - La subrayado en la página 4 | posición 60-60 | Añadido el miércoles, 6 de julio de 2022 06:54:57

    asintiendo a una pregunta que Max no había llegado a formular.

``parse_clippings`` won't parse this by default but you can write your own parser for 
the second line and pass it to the parameter ``metadata_parser``. 
You can take a look at an example `here <examples/bilingual_spanish_english_kindle/main.py>`_.




.. |pypi| image:: https://img.shields.io/pypi/v/clippings.svg
    :target: https://pypi.org/pypi/clippings
    :alt: Latest version released on PyPI

.. |build| image:: https://github.com/samueldg/clippings/workflows/Run%20tests/badge.svg
    :target: https://github.com/samueldg/clippings/actions
    :alt: Build status

.. |coverage| image:: https://coveralls.io/repos/github/samueldg/clippings/badge.svg?branch=master
    :target: https://coveralls.io/github/samueldg/clippings?branch=master
    :alt: Test coverage

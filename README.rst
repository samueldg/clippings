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

.. code:: shell

    # Parse a clippings file
    clippings -o dict ./clippings.txt
    
    # or from stdin:
    cat clippings.txt | clippings -


.. |pypi| image:: https://img.shields.io/pypi/v/clippings.svg
    :target: https://pypi.org/pypi/clippings
    :alt: Latest version released on PyPI

.. |build| image:: https://github.com/samueldg/clippings/workflows/Run%20tests/badge.svg
    :target: https://github.com/samueldg/clippings/actions
    :alt: Build status

.. |coverage| image:: https://coveralls.io/repos/github/samueldg/clippings/badge.svg?branch=master
    :target: https://coveralls.io/github/samueldg/clippings?branch=master
    :alt: Test coverage

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
    :target: https://pypi.python.org/pypi/clippings
    :alt: Latest version released on PyPI

.. |build| image:: https://api.travis-ci.org/samueldg/clippings.svg?branch=master
    :target: http://travis-ci.org/samueldg/clippings
    :alt: Build status

.. |coverage| image:: https://coveralls.io/repos/github/samueldg/clippings/badge.svg?branch=master
    :target: https://coveralls.io/github/samueldg/clippings?branch=master
    :alt: Test coverage

Clippings
=========

Python module to manipulate Amazon Kindle clippings files.

It allows you to:

-  Parse your existing clippings file into a structured representation;
-  Generate clippings file programmatically.

Installation
------------

.. code:: shell

    pip install clippings

Usage
-----

.. code:: shell

    # Parse a clippings file
    python -m clippings.parser -o dict ./clippings.txt
    
    # or from stdin:
    cat clippings.txt | python -m clippings.parser -

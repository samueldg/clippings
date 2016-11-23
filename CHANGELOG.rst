==========
Change Log
==========

This document tracks changes to `clippings <https://pypi.python.org/pypi/clippings>`_ between releases.


`0.1.2`_ (2016-11-23)
---------------------

* [fix] The clipping page should always return an ``int``.
* [fix] ``authors`` will be a string, not a list (no easy way to parse this reliably).
* [fix] Removed the initial new line from notes' content.
* [test] Added a test suite for utils and parsing classes.
* [test] Integrated coverage and travis CI.
* [misc] Classes implement ``__str__``, and not ``__repr__``.

`0.1.1`_ (2016-11-20)
---------------------

* [dist] Pushed to PyPI!
* [dist] Small fixes for distribution.
* [docs] README converted from markdown into reStructuredText.

`0.1.0`_ (2016-11-20)
---------------------

* [dist] Initial release.

.. _`0.1.0`: https://github.com/samueldg/clippings/releases/tag/0.1.0
.. _`0.1.1`: https://github.com/samueldg/clippings/compare/0.1.0...0.1.1
.. _`0.1.2`: https://github.com/samueldg/clippings/compare/0.1.1...0.1.2

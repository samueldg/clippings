# Change Log

This document tracks changes to [clippings](https://pypi.org/pypi/clippings) between releases.

## [0.9.0](https://github.com/samueldg/clippings/releases/tag/0.9.0) (2022-11-03)

* [feature] Extend API to allow custom metadata line parsers. Includes an example of providing an English + Spanish bilingual parser. (@jonahsol)
* [feature] Allow document title lines that don't include an author. (@jonahsol)
* [dist] Drop support for Python 3.6.
* [dist] Add support for Python 3.11, and include in CI.
* [misc] Upgrade all dev dependencies.
* [misc] Add linter step in Github Actions CI.

## [0.8.0](https://github.com/samueldg/clippings/releases/tag/0.8.0) (2021-11-09)

* [dist] Add support for Python 3.10.

## [0.7.0](https://github.com/samueldg/clippings/releases/tag/0.7.0) (2021-01-13)

* [fix] Compatibility with latest clippings file format (capitalized "Page") (@rjalexa)
* [misc] Ditch HTTP links in docs, in favor of HTTPS
* [misc] Better qualify dev dependencies
* [dist] Add support for Python 3.9.
* [dist] Drop support for Python 3.5.
* [misc] Switch CI over to GitHub actions.
* [test] Convert tests from unittest style to pytest style.

## [0.6.0](https://github.com/samueldg/clippings/releases/tag/0.6.0) (2020-06-27)

* [feature] Compatibility with Paperwhite 3 clippings format (@twkrol)

## [0.5.0](https://github.com/samueldg/clippings/releases/tag/0.5.0) (2019-11-24)

* [dist] Drop support for Python 2.7.
* [dist] Drop support for Python 3.4.
* [dist] Add support for Python 3.8, and include in CI.

## [0.4.0](https://github.com/samueldg/clippings/releases/tag/0.4.0) (2018-01-08)

* [dist] Officially drop support for Python 3.3.
* [dist] Add support for Python 3.7, and include in CI.
* [fix] Fix Travis CI build, which no longer supported Python 3.3.

## [0.3.0](https://github.com/samueldg/clippings/releases/tag/0.3.0) (2017-01-19)

* [feature] Add a 'clippings' console script.

## [0.2.1](https://github.com/samueldg/clippings/releases/tag/0.2.1) (2017-01-08)

* [dist] Add support for Python 3.6, and include in CI.

## [0.2.0](https://github.com/samueldg/clippings/releases/tag/0.2.0) (2016-11-29)

* [feature] Ability to specify the write file using ``--write-to`` or ``-w``.
* [dist] Officially dropped support for Python 2.6.
* [fix] Print a list/JSON array, rather than concatenated dict's/JSON objects (backwards-incompatible).
* [fix] Removed leading zero's in hours, to align with the Kindle format.
* [fix] Fixed broken Python 2 support (module, and tests).
* [test] Added tests for the output functions and ``main()``.
* [test] Added all supported Python version in test automation.
* [misc] Added ``.coveragerc`` file for coverage configuration.
* [misc] Added coveralls to CI process, and badge on the README.

## [0.1.2](https://github.com/samueldg/clippings/releases/tag/0.1.2) (2016-11-23)

* [fix] The clipping page should always return an ``int``.
* [fix] ``authors`` will be a string, not a list (no easy way to parse this reliably).
* [fix] Removed the initial new line from notes' content.
* [test] Added a test suite for utils and parsing classes.
* [test] Integrated coverage and travis CI.
* [misc] Classes implement ``__str__``, and not ``__repr__``.

## [0.1.1](https://github.com/samueldg/clippings/releases/tag/0.1.1) (2016-11-20)

* [dist] Pushed to PyPI!
* [dist] Small fixes for distribution.
* [docs] README converted from markdown into reStructuredText.

## [0.1.0](https://github.com/samueldg/clippings/releases/tag/0.1.0) (2016-11-20)

* [dist] Initial release.

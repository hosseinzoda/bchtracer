bchtracer
===========================

|PyPI| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov| |pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/bchtracer.svg
   :target: https://pypi.org/project/bchtracer/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/bchtracer
   :target: https://pypi.org/project/bchtracer
   :alt: Python Version
.. |License| image:: https://img.shields.io/github/license/hosseinzoda/bchtracer
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/bchtracer/latest.svg?label=Read%20the%20Docs
   :target: https://bchtracer.readthedocs.io/
   :alt: Read the documentation at https://bchtracer.readthedocs.io/
.. |Build| image:: https://github.com/hosseinzoda/bchtracer/workflows/Build%20bchtracer%20Package/badge.svg
   :target: https://github.com/hosseinzoda/bchtracer/actions?workflow=Package
   :alt: Build Package Status
.. |Tests| image:: https://github.com/hosseinzoda/bchtracer/workflows/Run%20bchtracer%20Tests/badge.svg
   :target: https://github.com/hosseinzoda/bchtracer/actions?workflow=Tests
   :alt: Run Tests Status
.. |Codecov| image:: https://codecov.io/gh/hosseinzoda/bchtracer/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/hosseinzoda/bchtracer
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------

* BFS for finding shortest paths to a target address

.. code:: console

   $ python -m bchtracer bfs-find-link --funding-txo <TXID>:<INDEX> --target-address <ADDRESS> --max-depth 4 --limit 10


Installation
------------

Install with poetry

.. code:: console

   $ poetry install


You can install *bchtracer* via pip_ from PyPI_:

.. code:: console

   $ pip install bchtracer


Usage
-----

Please see the `Command-line Reference <Usage_>`_ for details.


Credits
-------

This package was created with cookietemple_ using Cookiecutter_ based on Hypermodern_Python_Cookiecutter_.

.. _cookietemple: https://cookietemple.com
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _PyPI: https://pypi.org/
.. _Hypermodern_Python_Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _pip: https://pip.pypa.io/
.. _Usage: https://bchtracer.readthedocs.io/en/latest/usage.html

==============
SqlAlchemy2UML
==============


.. image:: https://img.shields.io/pypi/v/sqla2uml.svg
        :target: https://pypi.python.org/pypi/sqla2uml

.. image:: https://img.shields.io/travis/sfermigier/sqla2uml.svg
        :target: https://travis-ci.com/sfermigier/sqla2uml

.. image:: https://readthedocs.org/projects/sqla2uml/badge/?version=latest
        :target: https://sqla2uml.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



Usage
-----

Install as a development dependency in your project, then type `sqla2uml` for help::

    Usage: sqla2uml [OPTIONS]

    Options:
      -m, --module TEXT          Package to analyse (recursively)
      -o, --output TEXT          File to output result (defaults to stdout)
      -p, --properties           Include properties in diagrams 
      -x, --exclude TEXT         List of class names to exclude from diagram
      -d, --debug-level INTEGER  Debug level
      --help                     Show this message and exit.


* Free software: MIT license
* Documentation: https://sqla2uml.readthedocs.io. (not working yet)


Features
--------

* Generate UML diagrams from SQLAlchemy models.
* One must have PlantUML installed.
* More features / more flexibility to come later.


Development
-----------

* Pull-requests accepted.
* Participants must adhere to the Python COC (<https://www.python.org/psf/>)


Credits
-------

This package was created with Cruft_ and the `abilian/cookiecutter-abilian-python`_ project template.

.. _Cruft: https://github.com/cruft/cruft
.. _`abilian/cookiecutter-abilian-python`: https://github.com/abilian/cookiecutter-abilian-python

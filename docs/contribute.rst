Contributing
============

Want to help out with *behave-django*?  Cool!  Here's a quick guide to
do just that.

Preparation
-----------

Fork the *behave-django* repository, then clone it:

.. code:: console

    $ git clone git@github.com:your-username/behave-django.git

Ensure Tox is installed.  We use it to run linters, run the tests and
generate the docs:

.. code:: console

    $ pip install tox

If you use uv, install Tox with the tox-uv plugin:

.. code:: console

    $ uv tool install tox --with tox-uv

uv also allows you to easily install several Python versions in parallel,
which is handy to help us test against all supported Pythons, e.g.

.. code:: console

    $ uv python install 3.14 --preview --default

Essentials
----------

Make sure the tests pass.  The ``@failing`` tag is used for tests that
are supposed to fail.  The ``@requires-live-http`` tag is used for
tests that can't run with ``--simple`` flag.  See the ``[testenv]``
section in ``tox.ini`` for details.

.. code:: console

    $ tox list               # show all Tox environments
    $ tox -e py314-django52  # run just a single environment
    $ tox                    # run all linting and tests

Getting your hands dirty
------------------------

Start your topic branch:

.. code:: console

    $ git switch -c your-topic-branch

Make your changes.  Add tests for your change.  Make the tests pass:

.. code:: console

    $ tox -e py-django52

Finally, make sure your tests pass on all the configurations
*behave-django* supports.  This is defined in ``tox.ini``.  The Python
versions you test against need to be available in your PATH.

.. code:: console

    $ tox

You can choose not to run all tox tests and let the CI server take care
about that.  In this case make sure your tests pass when you push your
changes and open the PR.

Code style
----------

We use Ruff to govern our code style.  ``ruff check`` and ``ruff format``
are executed with Tox and run over the code also on the CI server.

.. code:: console

    $ tox -e lint,format

To fix formatting complaints conveniently, you can run Ruff over a
specific file or the entire code base like this:

.. code:: console

    $ tox -e format -- .

You can find and adapt the Ruff configuration for checks and formatting
in `pyproject.toml`_.

Writing tests
-------------

The `tests`_ folder contains:

- Unit tests (in ``tests/unit``)
- Feature tests (in ``tests/acceptance``)
- A minimal Django project consisting of the directories ``test_project``
  and ``test_app``, and the inevitable ``manage.py`` module.  This Django
  project is used for the feature tests.  It also serves as an example
  for how to use *behave-django*.

When you run the tests with Tox both the unit tests and the feature tests
are executed, and test coverage is measured.

.. code:: console

    $ tox -e py-django52

Documentation changes
---------------------

If you make changes to the documentation generate it locally and take a
look at the results.  Sphinx builds the output in ``docs/_build/``.

.. code:: console

    $ tox -e docs
    $ python -m webbrowser -t docs/_build/html/index.html

Finally
-------

Push to your fork and `submit a pull request`_.

To clean up behind you, you can run:

.. code:: console

    $ tox -e clean


.. _pyproject.toml: https://github.com/behave/behave-django/blob/main/pyproject.toml
.. _tests: https://github.com/behave/behave-django/tree/main/tests
.. _submit a pull request: https://github.com/behave/behave-django/compare/

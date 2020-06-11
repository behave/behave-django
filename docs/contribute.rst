Contributing
============

Want to help out with *behave-django*?  Cool!  Here's a quick guide to
do just that.

Preparation
-----------

Fork, then clone the repo:

.. code:: console

    $ git clone git@github.com:your-username/behave-django.git

Ensure Tox is installed.  We use it to run linters, run the tests and
generate the docs:

.. code:: console

    $ pip install tox

Essentials
----------

Make sure the tests pass.  The ``@failing`` tag is used for tests that
are supposed to fail.  The ``@requires-live-http`` tag is used for
tests that can't run with ``--simple`` flag.  See the ``[testenv]``
section in ``tox.ini`` for details.

.. code:: console

    $ tox -lv               # show all Tox targets
    $ tox -e py37-django22  # run just a single target
    $ tox                   # run all linting and tests

Getting your hands dirty
------------------------

Start your topic branch:

.. code:: console

    $ git checkout -b your-topic-branch

Make your changes.  Add tests for your change.  Make the tests pass:

.. code:: console

    $ tox -e behave-latest

Finally, make sure your tests pass on all the configurations
*behave-django* supports.  This is defined in ``tox.ini``.  The Python
versions you test against need to be available in your PATH.

.. code:: console

    $ tox

You can choose not to run all tox tests and let the CI server take care
about that.  In this case make sure your tests pass when you push your
changes and open the PR.

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

Other things to note
--------------------

- Write tests.
- Your tests don't have to be *behave* tests. ``:-)``
- We're using PEP8 as our code style guide (``flake8`` will run over the code
  on the CI server).

Thank you!


.. _submit a pull request: https://github.com/behave/behave-django/compare/

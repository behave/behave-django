Test Coverage
=============

You can integrate `Coverage.py`_ with behave-django to find out the test coverage
of your code.

There are two ways to do this.  The simple (and obvious one) is via invocation
through the ``coverage`` CLI.  Alternatively, you can integrate Coverage in the
``environment.py`` file of your BDD test setup as shown below.

Prerequisites
-------------

Obviously, you need to install Coverage to measure code coverage, e.g.

.. code-block:: bash

    $ pip install coverage[toml]

Invoke via ``coverage``
-----------------------

Instead of using ``python manage.py``, you simply use
``coverage run manage.py`` to invoke your BDD tests, e.g.

.. code-block:: bash

    $ coverage run manage.py behave

Afterwards, you can display a coverage report in your terminal to understand
which lines your tests are missing, e.g.

.. code-block:: bash

    $ coverage report --show-missing

.. tip::

    A Django project setup with coverage configured in ``pyproject.toml`` and
    executed by Tox is show-cased in the `Painless CI/CD Copier template for
    Django`_.

Integrate via ``environment.py``
--------------------------------

In ``environment.py``, add the code snippet below in the ``before_all`` function
to start measuring test coverage:

.. code-block:: python

    import coverage

    def before_all(context):
        cov = coverage.Coverage()
        cov.start()
        context.cov = cov

Then write below code to end up measuring test coverage.
You can save the coverage result on html format.

.. code-block:: python

    def after_all(context):
        cov = context.cov
        cov.stop()
        cov.save()
        cov.html_report(directory="./cov")

You can check the test coverage on the web with the following command.

.. code-block:: bash

    $ python -m http.server --directory ./cov

.. warning::

    Internally, the time ``before_all`` is executed seems to be later than the
    time when django loads the modules set in each app.

    So sometimes it is necessary to reload django app's modules for accurate
    test coverage measurement.

    Like this:

    .. code-block:: python

        import inspect
        import importlib

        def reload_modules():
        import your_app1
        import your_app2

        for app in [your_app1, your_app2]:
            members = inspect.getmembers(app)
            modules = map(
                lambda keyval: keyval[1],
                filter(lambda keyval: inspect.ismodule(keyval[1]), members),
            )
            for module in modules:
                try:
                    importlib.reload(module)
                except:
                    continue

    .. code-block:: python

        def before_all(context):
        # cov
        cov = coverage.Coverage()
        cov.start()
        context.cov = cov

        # modules
        reload_modules()

.. _Coverage.py: https://coverage.readthedocs.io/
.. _Painless CI/CD Copier template for Django:
    https://gitlab.com/painless-software/cicd/app/django

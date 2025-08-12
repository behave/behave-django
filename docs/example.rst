Project Example
===============

This is a full example on how to start a Django project with a BDD test
setup that runs from commit #1. (See :doc:`usage` if you want to start
using Behave with an existing Django project.)

We will use modern Python tooling.  No need to worry about managing virtual
environments and project dependencies.  ``uv`` will take care of everything.

Django with BDD from Scratch
----------------------------

Bootstrap your Python project.

.. code-block:: shell

    mkdir myproject
    cd myproject
    uv init
    rm main.py  # we don't need uv's example module

Turn it into a Django project.

.. code-block:: shell

    uv add django
    uv run django-admin startproject application .

Add Behave to your development dependencies.

.. code-block:: shell

    uv add --dev behave-django

Integrate Behave with your Django project by adding something like this to
``application/settings.py``:

.. code-block:: python

    try:
        import behave_django
    except ImportError:
        print("Behave not available. Probably running in production.")
    else:
        INSTALLED_APPS += ["behave_django"]

Add the following to ``pyproject.toml`` to tell Behave where to look for
the tests:

.. code-block:: toml

    [tool.behave]
    paths = ["tests"]

Create a ``tests`` folder and add your first feature file to start
behavior-driven development (BDD), e.g.

.. code-block:: shell

    mkdir -p tests/features
    touch tests/features/admin-login.feature

Add a test scenario to the empty feature file, e.g.

.. code-block:: gherkin

    Feature: Verify Django Admin is available

    Scenario: Use the Django Admin login form
        Given we have created a Django superuser
        And we have navigated to the Django Admin login page
        When we enter username and password
        Then the Django Admin overview is shown

Create a steps folder and run Behave using the Django management command
``behave`` to show you the missing step implementations.

.. code-block:: shell

    mkdir tests/steps
    uv run manage.py behave

Note that Behave will print out Python code that you can copy and paste.

Now, create a Python module for your step implementation, say,
``tests/steps/admin_login.py``, and paste the output into that file.

If you want to run Python code before or after features, scenarios, steps
or tags add a ``tests/environment.py`` file (see `the Behave docs`_ for
details).

Your setup should now look like this:

.. code-block:: console

    ├── application
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    ├── pyproject.toml
    ├── README.md
    ├── tests
    │   ├── environment.py
    │   ├── features
    │   │   └── admin-login.feature
    │   └── steps
    │       └── admin_login.py
    └── uv.lock

You can now start implementing the business logic of your steps and tweak
your test environment using Python code.

Copier Template
---------------

.. tip::

    You can create a Django starter project with this layout using the
    `Painless CI/CD Copier template for Django`_.

.. _the Behave docs: https://behave.readthedocs.io/en/latest/tutorial/#environmental-controls
.. _Painless CI/CD Copier template for Django: https://gitlab.com/painless-software/cicd/app/django

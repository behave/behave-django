Getting Started
===============

If you're new to *Behave* you should start with the `Behave Tutorial`_ and
its follow-up chapters on the theory and practice of behavior-driven
development (BDD).

Setting up Behave for a Django project is no different than using Behave
for any other Python project, except that:

#. you add *behave-django* to the ``INSTALLED_APPS`` in the settings of
   your Django project, and
#. you run Behave via the ``behave`` management command.

Create a folder structure
-------------------------

The `Feature Testing Setup`_ chapter of Behave's documentation describes
the various files and directories to prepare for your BDD test setup.

The Behave documentation suggest to start by adding a ``features`` folder
to your project root directory, which contains your feature files, the
test environment control module, and a ``steps`` subdirectory for the
code that implements the *given*, *when*, *then* steps of your features
in Python.

::

    features/
        steps/
            your_steps.py
        environment.py
        your-feature.feature

Alternatively, you can put both the ``features`` and the ``steps`` folder
in a ``tests`` folder of your project root directory.  This is recommended
if you want to follow common practices of Python projects.

::

    tests/
        features/
            example.feature
        steps/
            given.py
            then.py
            when.py
        environment.py

Your Behave configuration in ``pyproject.toml`` should then look somewhat
like this:

.. code-block:: toml

    [tool.behave]
    junit = true
    junit_directory = "tests"
    paths = ["tests"]

Execute your tests
------------------

Run ``python manage.py behave`` to execute your feature tests::

    $ python manage.py behave
    Creating test database for alias 'default'...
    Feature: Running tests # features/running-tests.feature:1
      In order to prove that behave-django works
      As the Maintainer
      I want to test running behave against this features directory
      Scenario: The Test                       # features/running-tests.feature:6
        Given this step exists                 # features/steps/running_tests.py:4 0.000s
        When I run "python manage.py behave"   # features/steps/running_tests.py:9 0.000s
        Then I should see the behave tests run # features/steps/running_tests.py:14 0.000s

    1 features passed, 0 failed, 0 skipped
    1 scenarios passed, 0 failed, 0 skipped
    3 steps passed, 0 failed, 0 skipped, 0 undefined
    Took.010s
    Destroying test database for alias 'default'...

See the `environment.py`_, `running-tests.feature`_ and `steps/running_tests.py`_
files in the ``tests/acceptance`` folder of the *behave-django* project
repository for implementation details of the above example.  See that
folder also for `more useful examples`_.

.. note::

   The `behave docs`_ provide additional helpful information on using Behave
   with Django and various test automation libraries.

.. _Behave Tutorial: https://behave.readthedocs.io/en/latest/tutorial/
.. _Feature Testing Setup: https://behave.readthedocs.io/en/latest/gherkin/
.. _environment.py: https://github.com/behave/behave-django/blob/main/tests/acceptance/environment.py
.. _running-tests.feature: https://github.com/behave/behave-django/blob/main/tests/acceptance/features/running-tests.feature
.. _more useful examples: https://github.com/behave/behave-django/tree/main/tests/acceptance/features
.. _steps/running_tests.py: https://github.com/behave/behave-django/blob/main/tests/acceptance/steps/running_tests.py
.. _behave docs: https://behave.readthedocs.io/en/latest/practical_tips/

Getting Started
===============

Create the features directory in your project’s root directory. (Next
to ``manage.py``)

::

    features/
        steps/
            your_steps.py
        environment.py
        your-feature.feature

Run ``python manage.py behave``::

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
files in the ``features`` folder of the project repository for implementation
details of this very example.  See the folder also for `more useful examples`_.

Alternative folder structure
----------------------------

For larger projects, specifically those that also have other types of tests,
it's recommended to use a more sophisticated folder structure, e.g.

::

    tests/
        acceptance/
            features/
                example.feature
            steps/
                given.py
                then.py
                when.py
            environment.py

Your *behave* configuration should then look something like this:

.. code-block:: ini

    [behave]
    paths = tests/acceptance
    junit_directory = tests/reports
    junit = yes

This way you'll be able to cleanly accommodate unit tests, integration
tests, field tests, penetration tests, etc. and test reports in a single
tests folder.

.. note::

   The `behave docs`_ provide additional helpful information on using *behave*
   with Django and various test automation libraries.

.. _environment.py: https://github.com/behave/behave-django/blob/main/tests/acceptance/environment.py
.. _running-tests.feature: https://github.com/behave/behave-django/blob/main/tests/acceptance/features/running-tests.feature
.. _more useful examples: https://github.com/behave/behave-django/tree/main/tests/acceptance/features
.. _steps/running_tests.py: https://github.com/behave/behave-django/blob/main/tests/acceptance/steps/running_tests.py
.. _behave docs: https://behave.readthedocs.io/en/latest/practical_tips.html

Fixture Loading
===============

behave-django can load your fixtures for you per feature/scenario. There are
two approaches to this:

* loading the fixtures in ``environment.py``, or
* using a decorator on your step function


Fixtures in environment.py
--------------------------

In ``environment.py`` we can load our context with the fixtures array.

.. code-block:: python

    def before_all(context):
        context.fixtures = ['user-data.json']

This fixture would then be loaded before every scenario.

If you wanted different fixtures for different scenarios:

.. code-block:: python

    def before_scenario(context, scenario):
        if scenario.name == 'User login with valid credentials':
            context.fixtures = ['user-data.json']
        elif scenario.name == 'Check out cart':
            context.fixtures = ['user-data.json', 'store.json', 'cart.json']

You could also have fixtures per Feature too

.. code-block:: python

    def before_feature(context, feature):
        if feature.name == 'Login':
            context.fixtures = ['user-data.json']
            # This works because behave will use the same context for
            # everything below Feature. (Scenarios, Outlines, Backgrounds)

``context.fixtures`` is processed after the ``before_scenario()`` function of
your ``environment.py`` file completes, and is automatically reset after each
scenario to prevent fixtures from carrying over to subsequent scenarios.

.. attention::

    Starting with **behave-django 2.0.0**, the ``context.fixtures`` attribute
    is automatically reset after each scenario. You no longer need to
    explicitly set ``context.fixtures = []`` to reset fixtures between
    scenarios or features.

    If you are upgrading from an earlier version and were manually resetting
    fixtures, you can safely remove those reset statements. If your code was
    appending to ``context.fixtures`` in ``before_scenario()``, you will need
    to update it to set the complete list of fixtures instead, since the
    attribute is reset after each scenario.

.. note::

    If you provide initial data via Python code `using the ORM`_ you need
    to place these calls in ``before_scenario()`` even if the data is
    meant to be used on the whole feature.  This is because Django's
    ``LiveServerTestCase`` resets the test database after each scenario.

Fixtures using a decorator
--------------------------

You can define `Django fixtures`_ using a function decorator. The decorator will
load the fixtures in the ``before_scenario``, as documented above. It is merely
a convenient way to keep fixtures close to your steps.

.. code-block::  python

    from behave_django.decorators import fixtures

    @fixtures('users.json')
    @when('someone does something')
    def step_impl(context):
        pass

.. note::

    Fixtures included with the decorator will apply to all other steps that
    they share a scenario with. This is because *behave-django* needs to
    provide them to the test environment before processing the particular
    scenario.

Support for multiple databases
------------------------------

By default, Django only loads fixtures into the ``default`` database.

Use ``before_scenario`` to load the fixtures in all of the databases you have
configured if your tests rely on the fixtures being loaded in all of them.

.. code-block:: python

    def before_scenario(context, scenario):
        context.databases = '__all__'

You can read more about it in the `Multiple database docs`_.


.. _using the ORM: https://docs.djangoproject.com/en/stable/topics/testing/tools/#fixture-loading
.. _Django fixtures: https://docs.djangoproject.com/en/stable/howto/initial-data/#provide-data-with-fixtures
.. _Multiple database docs: https://docs.djangoproject.com/en/stable/topics/testing/tools/#multi-database-support

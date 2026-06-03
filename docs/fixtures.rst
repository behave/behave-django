Fixture Loading
===============

behave-django can load your fixtures for you per scenario. There are
two approaches to this:

* loading the fixtures in ``environment.py``, or
* using a decorator on your step function


Fixtures in environment.py
--------------------------

You configure fixtures by populating ``context.fixtures`` from one of
behave's hooks (``before_all``, ``before_feature``, ``before_rule`` or
``before_scenario``).  behave-django takes a **fresh copy** of
``context.fixtures`` when each scope starts, so anything you do inside
that scope — whether you assign (``context.fixtures = [...]``) or mutate
in place (``context.fixtures.append(...)``) — is confined to that scope
and is automatically discarded when behave leaves it.

This means:

* Values set in an outer scope (e.g. ``before_all``) flow into inner
  scopes as a baseline.
* Mutations in an inner scope (e.g. ``before_scenario``) never leak back
  out to the outer scope or sideways into sibling scopes.
* You never need to "reset" ``context.fixtures`` manually between
  scenarios or features.

Loading the same fixtures for every scenario:

.. code-block:: python

    def before_all(context):
        context.fixtures = ['user-data.json']

Loading fixtures for an entire feature:

.. code-block:: python

    def before_feature(context, feature):
        if feature.name == 'Login':
            context.fixtures = ['user-data.json']

Loading or extending fixtures for individual scenarios:

.. code-block:: python

    def before_scenario(context, scenario):
        if scenario.name == 'User login with valid credentials':
            context.fixtures = ['user-data.json']
        elif scenario.name == 'Check out cart':
            context.fixtures = ['user-data.json', 'store.json', 'cart.json']

Combining a feature-wide baseline with scenario-specific extras:

.. code-block:: python

    def before_feature(context, feature):
        if feature.name == 'Shopping':
            context.fixtures = ['user-data.json']

    def before_scenario(context, scenario):
        if scenario.name == 'Check out cart':
            context.fixtures.append('cart.json')

In the example above, the "Shopping" feature's other scenarios still
receive only ``user-data.json`` — the ``cart.json`` append affects only
the "Check out cart" scenario.  Other features are not affected at all.

Opting out of inherited fixtures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run a scenario (or a whole feature) without the fixtures inherited
from a parent scope, assign an empty list:

.. code-block:: python

    def before_all(context):
        context.fixtures = ['user-data.json']

    def before_scenario(context, scenario):
        if scenario.name == 'Anonymous visitor':
            context.fixtures = []

The "Anonymous visitor" scenario runs without any fixtures; every other
scenario still receives ``user-data.json`` from ``before_all``.

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

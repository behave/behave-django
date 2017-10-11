Usage
=====

Web browser automation
----------------------

You can access the test HTTP server from your preferred web automation
library via ``context.base_url`` (normally, this would be set to
``http://localhost:8081``).  Alternatively, you can use
``context.get_url()``, which is a helper function for absolute paths and
reversing URLs in your Django project.  It takes an absolute path, a view
name, or a model as an argument, similar to `django.shortcuts.redirect`_.

Examples:

.. code-block:: python

    # Using Splinter
    @when(u'I visit "{url}"')
    def visit(context, url):
        context.browser.visit(context.base_url + url)

.. code-block:: python

    # Get context.base_url
    context.get_url()
    # Get context.base_url + '/absolute/url/here'
    context.get_url('/absolute/url/here')
    # Get context.base_url + reverse('view-name')
    context.get_url('view-name')
    # Get context.base_url + reverse('view-name', 'with args', and='kwargs')
    context.get_url('view-name', 'with args', and='kwargs')
    # Get context.base_url + model_instance.get_absolute_url()
    context.get_url(model_instance)

Django’s testing client
-----------------------

Attached to the context is an instance of TestCase.  You can access it
via ``context.test``.  This means you can do things like use Django’s
testing client.

.. code-block:: python

    # Using Django's testing client
    @when(u'I visit "{url}"')
    def visit(context, url):
        # save response in context for next step
        context.response = context.test.client.get(url)


Simple testing
--------------

If you only use Django's testing client then behave tests can run
much quicker with the ``--simple`` command line option. In this case
transaction rollback is used for test automation instead of flushing
the database after each scenario, just like in Django's standard
``TestCase``.

No HTTP server is started during the simple testing, so you can't
use web browser automation. Accessing ``context.base_url``
or calling ``context.get_url()`` will raise an exception.

unittest + Django assert library
--------------------------------

Additionally, you can utilize unittest and Django’s assert library.

.. code-block:: python

    @then(u'I should see "{text}"')
    def visit(context, text):
        # compare with response from ``when`` step
        response = context.response
        context.test.assertContains(response, text)

Database transactions per scenario
----------------------------------

Each scenario is run inside a database transaction, just like your
regular TestCases.  So you can do something like:

.. code-block:: python

    @given(u'user "{username}" exists')
    def create_user(context, username):
        # This won't be here for the next scenario
        User.objects.create_user(username=username, password='correcthorsebatterystaple')

And you don’t have to clean the database yourself.

If you have `factories`_ you want to instantiate on a per-scenario basis,
you can initialize them in ``environment.py`` like this:

.. code-block:: python

    from myapp.main.tests.factories import UserFactory, RandomContentFactory


    def before_scenario(context, scenario):
        UserFactory(username='user1')
        UserFactory(username='user2')
        RandomContentFactory()

Fixture loading
---------------

behave-django can load your fixtures for you per feature/scenario. There are
two approaches to this:

* loading the fixtures in ``environment.py``, or
* using a decorator on your step method


Fixtures in environment.py
**************************

In ``environment.py`` we can load our context with the fixtures array.

.. code-block:: python

    def before_scenario(context, scenario):
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

Of course, since ``context.fixtures`` is really just a list, you can
mutate it however you want, it will only be processed upon leaving the
``before_scenario()`` function of your ``environment.py`` file.

.. note::

    If you provide initial data via Python code `using the ORM`_ you need
    to place these calls in ``before_scenario()`` even if the data is
    meant to be used on the whole feature.  This is because Django's
    ``LiveServerTestCase`` resets the test database after each scenario.


Fixtures using a decorator
**************************

You can define `django fixtures`_ or a path to a callable for any step, using
a method decorator. The decorator will load the fixture in the
``before_scenario``, as documented above. It is merely a convenient way to keep
fixtures close to your steps. The decorator also accepts a string, containing
the full path to a callable.

.. code-block::  python

    from behave_django.decorators import fixtures

    @fixtures('users.json', 'path.to.my_callable')
    @when('someone does something')
    def step_impl(context):
        # context.school_of is available
        pass


This will append ``users.json`` to ``context.fixtures`` in ``before_scenario``.
The callable is executed and receives ``context`` as single argument, which is
also available in the decorated step.

.. code-block:: python

    def my_callable(context):
        silly_walks = '_/\_, _/|_, _|\_'
        context.school_of = silly_walks


Command line options
--------------------

You can use regular behave command line options with the behave
management command.

.. code-block:: bash

    $ python manage.py behave --tags @wip

Additional command line options provided by django_behave:

``--use-existing-database``
***************************

Don't create a test database, and use the database of your default runserver
instead. USE AT YOUR OWN RISK! Only use this option for testing against a
*copy* of your production database or other valuable data. Your tests may
destroy your data irrecoverably.

``--keepdb``
************

Starting with Django 1.8, the ``--keepdb`` flag was added to ``manage.py test``
to facilitate faster testing by using the existing database instead of
recreating it each time you run the test. This flag enables
``manage.py behave --keepdb`` to take advantage of that feature.
|keepdb docs|_.

``--simple``
************

Use Django's simple ``TestCase`` which rolls back the database transaction after
each scenario instead of flushing the entire database. Tests run much quicker,
however HTTP server is not started and therefore web browser automation is
not available.

Behave configuration file
-------------------------

You can use behave’s configuration file.  Just create a ``behave.ini``,
``.behaverc``, ``setup.cfg`` or ``tox.ini`` file in your project’s root
directory and behave will pick it up.  You can read more about it in the
`behave docs`_.

For example, if you want to have your features directory somewhere else.
In your .behaverc file, you can put

.. code-block:: ini

    [behave]
    paths=my_project/apps/accounts/features/
          my_project/apps/polls/features/

Behave should now look for your features in those folders.


.. _django.shortcuts.redirect: https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#redirect
.. _factories: https://factoryboy.readthedocs.io/en/latest/
.. _behave docs: https://behave.readthedocs.io/en/latest/behave.html#configuration-files
.. |keepdb docs| replace:: More information about ``--keepdb``
.. _keepdb docs: https://docs.djangoproject.com/en/stable/topics/testing/overview/#the-test-database
.. _using the ORM: https://docs.djangoproject.com/en/stable/topics/testing/tools/#fixture-loading
.. _django fixtures: https://docs.djangoproject.com/en/stable/howto/initial-data/#providing-initial-data-with-fixtures

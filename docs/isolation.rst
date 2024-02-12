Test Isolation
==============

Database transactions per scenario
----------------------------------

Each scenario is run inside a database transaction, just like Django does
it with the related TestCase implementation.  So you can do something like:

.. code-block:: python

    @given('user "{username}" exists')
    def create_user(context, username):
        # This won't be here for the next scenario
        User.objects.create_user(username=username, password='correcthorsebatterystaple')

And you don’t have to clean the database yourself.

Troubleshooting
---------------

.. note::

    Users have reported that test isolation and loading fixtures works
    differently with different test runners (e.g. when the ``--simple``
    option is used).  This is likely related to the Django TestCase class
    configured for the runner.

    Be sure you understand which Django TestCase class is used in your
    case, and how it's implemented in Django. See the `runner module`_
    and Django's documentation on `Writing and running tests`_ for details.


.. _runner module: https://github.com/behave/behave-django/blob/main/behave_django/runner.py
.. _Writing and running tests: https://docs.djangoproject.com/en/stable/topics/testing/overview/

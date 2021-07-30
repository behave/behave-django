Environment Setup
=================


before_django_ready hook
-----------------

You can add a ``before_django_ready`` function in your ``environment.py`` file in case
you want to make per-scenario changes inside a transaction.

This custom hook runs on the behave `before_scenario` hook.
It's executed before the TestCase is configured and initialized.

For example, if you have your own DjangoTestCase implemented and want to use it instead of
the existing BehaviorDrivenTestCase, ExistingDatabaseTestCase, DjangoSimpleTestCase,
you can monkey patch it in ``environment.py`` like this:

.. code-block:: python

    from behave_django.test_case import BehaviorDrivenTestMixin

    from myapp.main.test_utils import MyOtherTestCase


    def before_django_ready(context):
        # This function is run inside the transaction
        class MyOtherBehaviorDrivenTestCase(MyOtherTestCase, BehaviorDrivenTestMixin):
            pass
        context.test_runner.testcase_class = MyOtherBehaviorDrivenTestCase


django_ready hook
-----------------

You can add a ``django_ready`` function in your ``environment.py`` file in case
you want to make per-scenario changes inside a transaction.

This custom hook runs on the behave `before_scenario` hook.
It's executed after the TestCase is configured and initialized.

For example, if you have `factories`_ you want to instantiate on a per-scenario
basis, you can initialize them in ``environment.py`` like this:

.. code-block:: python

    from myapp.main.tests.factories import UserFactory, RandomContentFactory


    def django_ready(context):
        # This function is run inside the transaction
        UserFactory(username='user1')
        UserFactory(username='user2')
        RandomContentFactory()

Or maybe you want to modify the ``test`` instance:

.. code-block:: python

    from rest_framework.test import APIClient


    def django_ready(context):
        context.test.client = APIClient()


.. _factories: https://factoryboy.readthedocs.io/en/latest/
.. |keepdb docs| replace:: More information about ``--keepdb``
.. _keepdb docs: https://docs.djangoproject.com/en/stable/topics/testing/overview/#the-test-database

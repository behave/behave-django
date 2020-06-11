Environment Setup
=================

django_ready hook
-----------------

You can add a ``django_ready`` function in your ``environment.py`` file in case
you want to make per-scenario changes inside a transaction.

For example, if you have `factories`_ you want to instantiate on a per-scenario
basis, you can initialize them in ``environment.py`` like this:

.. code-block:: python

    from myapp.main.tests.factories import UserFactory, RandomContentFactory


    def django_ready(context, scenario):
        # This function is run inside the transaction
        UserFactory(username='user1')
        UserFactory(username='user2')
        RandomContentFactory()

Or maybe you want to modify the ``test`` instance:

.. code-block:: python

    from rest_framework.test import APIClient


    def django_ready(context, scenario):
        context.test.client = APIClient()


.. _factories: https://factoryboy.readthedocs.io/en/latest/
.. |keepdb docs| replace:: More information about ``--keepdb``
.. _keepdb docs: https://docs.djangoproject.com/en/stable/topics/testing/overview/#the-test-database

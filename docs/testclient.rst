Django’s Test Client
====================

Internally, Django's TestCase is used to maintain the test environment.
You can access the TestCase instance via ``context.test``.

.. code-block:: python

    # Using Django's testing client
    @when('I visit "{url}"')
    def visit(context, url):
        # save response in context for next step
        context.response = context.test.client.get(url)

Cross-version compatibility features
------------------------------------

Some properties of Django's test client are set on class-level, and some
are set on class-level only since Django version 5.2, which is slightly
inconvenient if you test across versions or upgrade Django one day.  With
*behave-django*, you can set those attributes on the ``context`` object
instead:

``databases``
    Control target databases. See :ref:`Support for multiple databases`.

``fixtures``
    Load database fixtures. See :ref:`Fixtures in environment.py`.

``reset_sequences``
    Can be set to ``True`` to always reset sequences. See Django's
    related `TransactionTestCase`_ documentation.

.. _TransactionTestCase: https://docs.djangoproject.com/en/stable/topics/testing/advanced/#django.test.TransactionTestCase.reset_sequences

Simple testing
--------------

If you only use Django's test client then *behave* tests can run much
quicker with the ``--simple`` command line option. In this case transaction
rollback is used for test automation instead of flushing the database after
each scenario, just like in Django's standard ``TestCase``.

No HTTP server is started during the simple testing, so you can't use web
browser automation. Accessing ``context.base_url`` or calling
``context.get_url()`` will raise an exception.

unittest + Django assert library
--------------------------------

Additionally, you can utilize unittest and Django’s assert library.

.. code-block:: python

    @then('I should see "{text}"')
    def visit(context, text):
        # compare with response from ``when`` step
        response = context.response
        context.test.assertContains(response, text)

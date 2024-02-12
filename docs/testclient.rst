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

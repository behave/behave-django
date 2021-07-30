Django’s Test Integration
====================

Django's TestCase
-----------------

Internally, Django's TestCase is used to maintain the test environment.
You can access the TestCase instance via ``context.test``.

.. code-block:: python

    # Using Django's testing client
    @when(u'I visit "{url}"')
    def visit(context, url):
        # save response in context for next step
        context.response = context.test.client.get(url)

Django's Test Runner
--------------------

Internally, Django's default Test Runner is used to start the test suite.

Refer to Django's configuration  for more info: https://docs.djangoproject.com/en/3.2/ref/settings/#test-runner

You can access the Runner instance via ``context.test_runner``.

.. code-block:: python

    from unittest.mock import patch

    from myapp.interfaces import MyRequestInterface

    @when(u'I require a third-party "{url}"')
    def visit(context, url):
        # verify some custom configuration
        should_mock_request = context.test_runner.should_mock_requests

        if should_mock_request:
            context.requests_patcher = patch('myapp.interfaces.requests')
            context.mocked_requests = context.requests_patcher.start()
            context.test.addCleanup(context.requests_patcher.stop)

        MyRequestInterface().require(url)

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

    @then(u'I should see "{text}"')
    def visit(context, text):
        # compare with response from ``when`` step
        response = context.response
        context.test.assertContains(response, text)

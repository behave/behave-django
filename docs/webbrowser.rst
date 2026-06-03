Web Browser Automation
======================

You can access the test HTTP server from your preferred web automation
library via ``context.base_url``.  Alternatively, you can use
``context.get_url()``, which is a helper function for absolute paths and
reversing URLs in your Django project.  It takes an absolute path, a view
name, or a model as an argument, similar to `django.shortcuts.redirect`_.

Examples:

.. code-block:: python

    # Using Splinter
    @when('I visit "{page}"')
    def visit(context, page):
        context.browser.visit(context.get_url(page))

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


Remote browsers and Selenium Hub
--------------------------------

By default the live test server binds to ``localhost``, which is fine when
the browser runs on the same machine as the tests.  If your browser runs in
a separate container or on a different host (for example, behind a
`Selenium Grid`_ hub), the server needs to listen on an address the browser
can reach.

Django exposes ``host`` and ``port`` as class attributes on
``LiveServerTestCase``, and uses the same ``host`` both to bind the socket
and to build ``live_server_url`` (which is what ``context.get_url()``
returns).  Pick a hostname the remote browser can resolve — for example,
the docker-compose service name of the Django container — rather than
``0.0.0.0``, which would leak into the URL handed to the browser.  Then
pair the subclass with a custom test runner and select it via the
|--runner|_ option:

.. code-block:: python

    # myproject/runner.py
    from behave_django.runner import BehaviorDrivenTestRunner
    from behave_django.testcase import BehaviorDrivenTestCase


    class RemoteBrowserTestCase(BehaviorDrivenTestCase):
        # Must be resolvable from the browser container.
        # In docker-compose this is typically the service name.
        host = 'myapp'
        port = 8100


    class RemoteBrowserTestRunner(BehaviorDrivenTestRunner):
        testcase_class = RemoteBrowserTestCase

.. code-block:: console

    $ python manage.py behave --runner myproject.runner.RemoteBrowserTestRunner

In your step setup you can then connect to a remote WebDriver and visit
``context.get_url()`` as usual — the URL will resolve to the address your
browser container can reach:

.. code-block:: python

    # features/environment.py
    from splinter.browser import Browser

    def before_all(context):
        context.browser = Browser(
            driver_name='remote',
            browser='chrome',
            command_executor='http://selenium-hub:4444/wd/hub',
        )

Make sure the chosen host is listed in ``ALLOWED_HOSTS`` (or set
``ALLOWED_HOSTS = ['*']`` in a test-only settings module), so Django accepts
the incoming requests.


.. _django.shortcuts.redirect: https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#redirect
.. _Selenium Grid: https://www.selenium.dev/documentation/grid/
.. |--runner| replace:: ``--runner``
.. _--runner: configuration.html#runner

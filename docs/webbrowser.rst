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


.. _django.shortcuts.redirect: https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#redirect

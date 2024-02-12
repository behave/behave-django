Using Page Objects
==================

.. warning::

    This is an *alpha* feature.  It may be removed or its underlying
    implementation changed without a deprecation process!  Please follow the
    discussions in `related issues`_ or on `Gitter`_ if you plan to use it.

With *behave-django* you can use the `Page Object pattern`_ and work on a
natural abstraction layer for the content or behavior your web application
produces.  This is a popular approach to make your tests more stable and
your code easier to read.

.. code-block:: python

    # FILE: steps/pageobjects/pages.py
    from behave_django.pageobject import PageObject, Link

    class Welcome(PageObject):
        page = 'home'  # view name, model or URL path
        elements = {
            'about': Link(css='footer a[role=about]'),
        }

    class About(PageObject):
        page = 'about'

.. code-block:: python

    # FILE: steps/welcome.py
    from pageobjects.pages import About, Welcome

    @given('I am on the Welcome page')
    def step_impl(context):
        context.welcome_page = Welcome(context)
        assert context.welcome_page.response.status_code == 200

    @when('I click on the "About" link')
    def step_impl(context):
        context.target_page = \
            context.welcome_page.get_link('about').click()
        assert context.target_page.response.status_code == 200

    @then('The About page is loaded')
    def step_impl(context):
        assert About(context) == context.target_page

A ``PageObject`` instance automatically loads and parses the page you
specify by its ``page`` attribute.  You then have access to the following
attributes:

``request``
    The HTTP request used by the Django test client to fetch the document.
    This is merely a convenient alias for ``response.request``.

``response``
    The Django test client's HTTP response object.  Use this to verify the
    actual HTTP response related to the retrieved document.

``document``
    The parsed content of the response.  This is, technically speaking, a
    `Beautiful Soup`_ object.  You *can* use this to access and verify any
    part of the document content, though it's recommended that you only
    access the elements you specify with the ``elements`` attribute, using
    the appropriate helper methods.

Helpers to access your page object's elements:

``get_link(name) -> Link``
    A subdocument representing a HTML anchor link, retrieved from
    ``document`` using the CSS selector specified in ``elements[name]``.
    The returned ``Link`` object provides a ``click()`` method to trigger
    loading the link's URL, which again returns a ``PageObject``.

.. note::

    *behave-django*'s `PageObject`_ is a headless page object, meaning
    that it doesn't use Selenium to drive the user interface.

    If you need a page object that encapsulates Selenium you may take a look
    at alternative libraries, such as `page-object`_, `page-objects`_ or
    `selenium-page-factory`_.  But keep in mind that this is a different
    kind of testing:

    - You'll be testing the Web browser, hence for Web browser compatibility.
    - Preparing an environment for test automation will be laborious.
    - Mocking objects in your tests will be difficult, if not impossible.
    - Your tests will be *significantly* slower and potentially brittle.

    Think twice if that is really what you need.  In most cases you'll be
    better off testing your Django application code only.  That's when you
    would use `Django's test client`_ and our headless page object.


.. _related issues: https://github.com/behave/behave-django/issues
.. _Gitter: https://gitter.im/behave/behave-django
.. _Page Object pattern: https://www.martinfowler.com/bliki/PageObject.html
.. _Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
.. _PageObject:
    https://github.com/behave/behave-django/blob/main/behave_django/pageobject.py
.. _page-object: https://pypi.org/project/page-object/
.. _page-objects: https://pypi.org/project/page-objects/
.. _selenium-page-factory: https://pypi.org/project/selenium-page-factory/
.. _Django's test client:
    https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client

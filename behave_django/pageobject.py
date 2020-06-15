"""
A headless Page Object pattern implementation.

Background reading: https://www.martinfowler.com/bliki/PageObject.html
"""
import django.shortcuts

from bs4 import BeautifulSoup


class WrongElementError(RuntimeError):
    """
    A different PageObject element was expected by the getter from the
    ```elements`` dictionary.
    """
    def __init__(self, element, expected):
        message = "Expected %s, found %s" % (element.__class__, expected)
        super(WrongElementError, self).__init__(message)


class PageObject:
    """
    Headless page object pattern implementation.

    :page:
        view name, model or URL path for ``django.shortcuts.resolve_url``
        to load the respective page using the Django test client
    :elements:
        Dictionary of elements accessible by helper methods
    """
    page = None
    elements = dict()

    def __init__(self, context):
        """
        Load and parse the page specified by the ``page`` class attribute.

        :context:
            Behave's context patched with Django support by behave-django
        """
        urlpath = django.shortcuts.resolve_url(self.__class__.page)
        self.response = context.test.client.get(urlpath)
        self.document = BeautifulSoup(self.response.content, 'html.parser')
        self.request = self.response.request
        self.context = context

    def __eq__(self, other):
        """
        Override default implementation, ignoring changing details of
        request and response.

        Instead of page we compare the request URL path, which is the
        resolved value and should always match for equal pages.
        """
        return isinstance(other, PageObject) and \
            self.elements == other.elements and \
            self.document.string == other.document.string and \
            self.request == other.request and \
            self.response.status_code == other.response.status_code

    def _get_element_ensure(self, name, ensure):
        """
        Return a subdocument matching the CSS selector of ``elements[name]``
        and enforcing a requested PageObject element class.

        :raises KeyError:
            if there is no element configured with the ``name`` key
        :raises WrongElementError:
            if the element found for ``name`` doesn't match the requested type
        """
        element = self.__class__.elements[name]
        if isinstance(element, ensure):
            return element
        raise WrongElementError(element, expected=ensure)

    def get_element(self, name):
        """
        Return a subdocument matching the CSS selector of elements[name].
        """
        return self.get_elements(name)[0]

    def get_elements(self, name):
        """
        Return all subdocuments matching the CSS selector of elements[name].
        """
        element = self._get_element_ensure(name, Element)
        return self.document.select(element.selector)

    def get_link(self, name):
        """
        Return a subdocument matching the CSS selector of elements[name],
        patched with methods for a link.
        """
        return self.get_links(name)[0]

    def get_links(self, name):
        """
        Return all subdocuments matching the CSS selector of elements[name],
        patched with methods for a link.
        """
        current_context = self.context
        element = self._get_element_ensure(name, Link)
        links = self.document.select(element.selector)
        for link in links:
            def click():
                """Visit a link, load related URL, return a PageObject"""
                href = link.get('href')

                class NewPageObject(PageObject):
                    page = href

                return NewPageObject(current_context)
            link.click = click
        return links


class Element:
    """An arbitrary HTML element"""

    def __init__(self, css):
        self.selector = css


class Link(Element):
    """A HTML anchor element representing a hyperlink"""

    def __init__(self, css):
        super(Link, self).__init__(css)

from bs4 import BeautifulSoup
from bs4.element import Tag
from behave import then, when

from pageobjects.pages import About, Welcome


@when(u'I instantiate the Welcome page object')
def new_pageobject(context):
    context.page = Welcome(context)


@then(u'it provides a valid Beautiful Soup document')
def pageobject_works(context):
    assert context.page.response.status_code == 200
    assert context.page.request == context.page.response.request
    assert isinstance(context.page.document, BeautifulSoup)
    assert 'Test App: behave-django' == context.page.document.title.string, \
        "unexpected title: %s" % context.page.document.title.string


@then(u'get_link() returns the link subdocument')
def getlink_subdocument(context):
    context.about_link = context.page.get_link('about')
    assert isinstance(context.about_link, Tag), \
        "should be instance of %s (not %s)" % (
            Tag.__name__, context.about_link.__class__.__name__)


@when('I call click() on the link')
def linkelement_click(context):
    context.next_page = context.about_link.click()


@then('it loads a new PageObject')
def click_returns_pageobject(context):
    assert About(context) == context.next_page

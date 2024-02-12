from http import HTTPStatus

from behave import then, when
from bs4 import BeautifulSoup
from bs4.element import Tag
from pageobjects.pages import About, Welcome


@when('I instantiate the Welcome page object')
def new_pageobject(context):
    context.page = Welcome(context)


@then('it provides a valid Beautiful Soup document')
def pageobject_works(context):
    assert context.page.response.status_code == HTTPStatus.OK
    assert context.page.request == context.page.response.request
    assert isinstance(context.page.document, BeautifulSoup)
    assert (
        context.page.document.title.string == 'Test App: behave-django'
    ), f'unexpected title: {context.page.document.title.string}'


@then('get_link() returns the link subdocument')
def getlink_subdocument(context):
    context.about_link = context.page.get_link('about')
    assert isinstance(context.about_link, Tag), (
        f'should be instance of {Tag.__name__} '
        f'(not {context.about_link.__class__.__name__})'
    )


@when('I call click() on the link')
def linkelement_click(context):
    context.next_page = context.about_link.click()


@then('it loads a new PageObject')
def click_returns_pageobject(context):
    assert About(context) == context.next_page

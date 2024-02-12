from urllib.request import urlopen

from behave import then, when


@when('I visit "{url}"')
def visit(context, url):
    page = urlopen(context.base_url + url)
    context.response = str(page.read())


@then('I should see "{text}"')
def i_should_see(context, text):
    assert text in context.response

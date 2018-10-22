try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from behave import when, then


@when(u'I visit "{url}"')
def visit(context, url):
    page = urlopen(context.base_url + url)
    context.response = str(page.read())


@then(u'I should see "{text}"')
def i_should_see(context, text):
    assert text in context.response

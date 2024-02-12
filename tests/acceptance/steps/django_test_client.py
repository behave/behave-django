from http import HTTPStatus

from behave import then, when


@when('I use django\'s test client to visit "{url}"')
def use_django_client(context, url):
    context.response = context.test.client.get(url)


@then('it should return a successful response')
def it_should_be_successful(context):
    assert context.response.status_code == HTTPStatus.OK

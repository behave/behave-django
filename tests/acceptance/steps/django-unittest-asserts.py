from behave import then, when


@when('I use the unittest assert library')
def use_unittest_assert_library(context):
    # If one of them works, all of them work. ;)
    context.test.assertEqual(1, 1)


@when('I use the django assert library')
def use_django_assert_library(context):
    response = context.test.client.get('/')
    context.test.assertTemplateUsed(response, 'index.html')


@then('it should work properly')
def asserts_should_work(context):
    pass

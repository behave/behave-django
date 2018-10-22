from behave import then


@then(u'this step should fail')
def failing_set(context):
    context.test.assertEqual(0, 1)

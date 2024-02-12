from behave import then


@then('this step should fail')
def failing_set(context):
    context.test.assertEqual(0, 1)

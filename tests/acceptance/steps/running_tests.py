from behave import given, then, when


@given('this step exists')
def step_exists(context):
    pass


@when('I run "python manage.py behave"')
def run_command(context):
    pass


@then('I should see the behave tests run')
def is_running(context):
    pass


@then('django_ready should be called')
def django_context(context):
    assert context.django

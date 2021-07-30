from behave import given, when, then


@given(u'this step exists')
def step_exists(context):
    pass


@when(u'I run "python manage.py behave"')
def run_command(context):
    pass


@then(u'I should see the behave tests run')
def is_running(context):
    pass


@then(u'before_django_ready should be called')
def before_django_context(context):
    assert context.before_django
    assert context.test_runner.before_django


@then(u'django_ready should be called')
def django_context(context):
    assert context.django

from django.conf import settings
from django.test.utils import get_runner

from behave import given, when, then

from tests.test_app.tests import MyCustomTestCase


@given(u'this step exists')
def step_exists(context):
    pass


@when(u'I run "python manage.py behave"')
def run_command(context):
    pass


@then(u'I should see the behave tests run')
def is_running(context):
    pass


@then(u'the test_runner should be MyCustomTestRunner')
def get_runner_dynamically(context):
    assert context.test_runner.is_custom
    DJANGO_CONFIGURED_RUNNER = get_runner(settings)
    assert isinstance(context.test_runner, DJANGO_CONFIGURED_RUNNER), "test runner should be created from Django's get_runner"  # noqa: E501


@then(u'before_django_ready should be called')
def before_django_context(context):
    assert context.before_django
    assert context.test_runner.before_django, "runner should have custom hook flag"  # noqa: E501
    assert issubclass(context.test_runner.testcase_class, MyCustomTestCase), "test case should be created from MyCustomTestCase"  # noqa: E501
    assert context.test_runner.testcase_class.is_custom, "test case should be the custom one"  # noqa: E501


@then(u'django_ready should be called')
def django_context(context):
    assert context.django

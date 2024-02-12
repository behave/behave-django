from behave import given, then
from test_app.models import BehaveTestModel

from behave_django.decorators import fixtures


@fixtures('behave-fixtures.json')
@given('a step with a fixture decorator')
def check_decorator_fixtures(context):
    pass


@fixtures('behave-second-fixture.json')
@given('a step with a second fixture decorator')
def check_decorator_second_fixture(context):
    pass


@fixtures('behave-fixtures.json', 'behave-second-fixture.json')
@given('a step with multiple fixtures')
def check_decorator_multiple(context):
    pass


@then('the fixture should be loaded')
def check_fixtures(context):
    context.test.assertEqual(BehaveTestModel.objects.count(), 1)


@then('the fixture for the second scenario should be loaded')
def check_second_fixtures(context):
    context.test.assertEqual(BehaveTestModel.objects.count(), 2)


@then('the sequences should be reset')
def check_reset_sequences(context):
    context.test.assertEqual(BehaveTestModel.objects.first().pk, 1)
    context.test.assertEqual(BehaveTestModel.objects.last().pk, 2)


@then('databases should be set to all database in the Django settings')
def check_databases_attribute(context):
    context.test.assertEqual(context.test.databases, frozenset({'default'}))

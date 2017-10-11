from behave import then, given

from behave_django.decorators import fixtures
from test_app.models import BehaveTestModel


@fixtures('behave-fixtures.json')
@given(u'a step with a fixture decorator')
def check_decorator_fixtures(context):
    pass


@fixtures('behave-fixtures.json', 'behave-second-fixture.json',
          'test_app.fixtures.callable.my_callable')
@given(u'a step with multiple fixtures and a callable')
def check_decorator_multiple(context):
    pass


@then(u'the fixture should be loaded')
def check_fixtures(context):
    context.test.assertEqual(BehaveTestModel.objects.count(), 1)


@then(u'the fixture for the second scenario should be loaded')
def check_second_fixtures(context):
    context.test.assertEqual(BehaveTestModel.objects.count(), 2)


@then(u'the sequences should be reset')
def check_reset_seqeunces(context):
    context.test.assertEqual(BehaveTestModel.objects.first().pk, 1)
    context.test.assertEqual(BehaveTestModel.objects.last().pk, 2)

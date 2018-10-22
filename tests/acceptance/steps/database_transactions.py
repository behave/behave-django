from behave import when, then

from test_app.models import BehaveTestModel


@when(u'I save the object')
def save_object(context):
    BehaveTestModel.objects.create(name='Behave Works', number=123)


@then(u'I should only have one object')
def should_have_only_one_object(context):
    assert 1 == BehaveTestModel.objects.count()

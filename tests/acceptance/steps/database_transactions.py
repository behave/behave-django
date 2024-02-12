from behave import then, when
from test_app.models import BehaveTestModel


@when('I save the object')
def save_object(context):
    BehaveTestModel.objects.create(name='Behave Works', number=123)


@then('I should only have one object')
def should_have_only_one_object(context):
    assert BehaveTestModel.objects.count() == 1

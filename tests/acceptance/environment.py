"""
behave environment module for testing behave-django
"""


def before_feature(context, feature):
    """Using ``append()`` here also verifies that mutations in
    ``before_feature`` are confined to the current feature and do not
    leak into the next one.
    """
    if feature.name == 'Fixture loading':
        context.fixtures.append('behave-fixtures.json')

    elif feature.name == 'Fixture loading with decorator':
        # Including empty fixture to test that #92 is fixed
        context.fixtures.append('empty-fixture.json')


def before_scenario(context, scenario):
    if (
        scenario.feature.name == 'Fixture auto-reset across scenarios'
        and scenario.name == 'First scenario loads a fixture'
    ):
        # Other scenarios in this feature deliberately leave
        # context.fixtures empty to verify the auto-reset behaviour.
        context.fixtures.append('behave-fixtures.json')

    if scenario.name == 'Load fixtures for this scenario and feature':
        context.fixtures.append('behave-second-fixture.json')

    if scenario.name == 'Load fixtures then reset sequences':
        context.fixtures.append('behave-second-fixture.json')
        context.reset_sequences = True

    if scenario.name == 'Load fixtures with databases option':
        context.databases = '__all__'

    if scenario.name == 'Override inherited fixtures with empty list':
        # Suppress the fixture inherited from ``before_feature``.
        context.fixtures = []


def django_ready(context):
    context.django = True

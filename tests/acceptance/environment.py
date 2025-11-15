"""
behave environment module for testing behave-django
"""


def before_feature(context, feature):
    if feature.name == 'Fixture loading with decorator':
        # Including empty fixture to test that #92 is fixed
        context.fixtures = ['empty-fixture.json']

    elif feature.name == 'Fixture reset - first feature with fixtures':
        context.fixtures = ['behave-fixtures.json']

    elif feature.name == 'Fixture reset - second feature with empty fixtures':
        context.fixtures = []


def before_scenario(context, scenario):
    # Set fixtures for each scenario explicitly since auto-reset happens after
    # each scenario
    if scenario.name == 'Load fixtures':
        context.fixtures = ['behave-fixtures.json']

    elif scenario.name == 'Load fixtures for this scenario and feature':
        context.fixtures = ['behave-fixtures.json', 'behave-second-fixture.json']

    elif scenario.name == 'Load fixtures then reset sequences':
        context.fixtures = ['behave-fixtures.json', 'behave-second-fixture.json']
        context.reset_sequences = True

    elif scenario.name == 'Load fixtures with databases option':
        context.fixtures = ['behave-fixtures.json']
        context.databases = '__all__'


def django_ready(context):
    context.django = True

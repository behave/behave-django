"""
behave environment module for testing behave-django
"""


def before_feature(context, feature):
    if feature.name == 'Fixture loading':
        context.fixtures = ['behave-fixtures.json']

    elif feature.name == 'Fixture loading with decorator':
        # Including empty fixture to test that #92 is fixed
        context.fixtures = ['empty-fixture.json']


def before_scenario(context, scenario):
    if scenario.name == 'Load fixtures for this scenario and feature':
        context.fixtures.append('behave-second-fixture.json')

    if scenario.name == 'Load fixtures then reset sequences':
        context.fixtures.append('behave-second-fixture.json')
        context.reset_sequences = True

    if scenario.name == 'Load fixtures with databases option':
        context.databases = '__all__'


def django_ready(context):
    context.django = True

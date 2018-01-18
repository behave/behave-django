"""
behave environment module for testing behave-django
"""


def before_feature(context, feature):
    if feature.name == 'Fixture loading':
        context.fixtures = ['behave-fixtures.json']


def before_scenario(context, scenario):
    if scenario.name == 'Load fixtures then reset sequences':
        context.reset_sequences = True

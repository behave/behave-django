Feature: Fixture loading with decorator
    In order to have sample data during my behave tests
    As a developer
    I want to load fixtures for specific steps with a decorator

    Scenario: Load fixtures with the decorator
       Given a step with a fixture decorator
        Then the fixture should be loaded

    Scenario: Load multiple fixtures and callables
       Given a step with multiple fixtures
        Then the fixture for the second scenario should be loaded

@requires-live-http
Feature: Fixture loading with decorator
    In order to have sample data during my behave tests
    As a developer
    I want to load fixtures for specific steps with a decorator

    Scenario: Load fixtures with the decorator
       Given a step with a fixture decorator
        Then the fixture should be loaded

    Scenario: A Subsequent scenario should only load its fixtures
        Given a step with a second fixture decorator
        Then I should only have one object

    Scenario: Load multiple fixtures and callables
       Given a step with multiple fixtures
        Then the fixture for the second scenario should be loaded

@requires-live-http
Feature: Fixture loading
    In order to have sample data during my behave tests
    As the Maintainer
    I want to load fixtures

    Scenario: Load fixtures
        Then the fixture should be loaded

    Scenario: Load fixtures for this scenario and feature
        Then the fixture for the second scenario should be loaded

    @failing
    Scenario: Load fixtures then reset sequences
        Then the sequences should be reset

    Scenario: Load fixtures with databases option
        Then databases should be set to all database in the Django settings

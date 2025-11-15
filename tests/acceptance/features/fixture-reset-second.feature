@requires-live-http
Feature: Fixture reset - second feature with empty fixtures
    In order to test fixture reset between features
    As a developer
    I want fixtures to be properly reset when set to empty list in before_feature

    Scenario: Second feature should have no fixtures
        Then there should be no fixtures loaded

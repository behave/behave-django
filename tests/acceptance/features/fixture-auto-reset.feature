@requires-live-http
Feature: Fixture auto-reset across scenarios
    In order to write independent scenarios without manual cleanup
    As a developer
    I want context.fixtures to be reset automatically between scenarios

    Scenario: First scenario loads a fixture
        Then the fixture should be loaded

    Scenario: Second scenario inherits no fixtures
        Then there should be no fixtures loaded

    Scenario: Third scenario also inherits no fixtures
        Then there should be no fixtures loaded

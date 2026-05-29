@requires-live-http
Feature: Settings overrides do not accumulate across scenarios
    In order to run my tests without issues
    As a behave-django developer
    I want to avoid RecursionError when running many scenarios
    So that my test suite does not crash regardless of its size

    Scenario Outline: Scenario <n> completes without RecursionError
        Then a Django setting can be accessed with a recursion headroom of 5

    Examples:
        | n |
        | 1 |
        | 2 |
        | 3 |
        | 4 |
        | 5 |

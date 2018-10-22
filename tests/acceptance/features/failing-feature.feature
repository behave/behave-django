@failing
Feature: Test failing feature
    In order for the system to know that there is a failing test
    As the Maintainer
    I want behave-django to return a non-zero return code for failing tests

    Scenario: Failing test
        Given this step exists
        Then this step should fail

@requires-live-http
Feature: Using page objects works as documented
    In order to ensure that page objects can be used as documented
    As the Maintainer
    I want to test all suggested uses

    Scenario: Welcome page object returns a valid (Beautiful Soup) document
        When I instantiate the Welcome page object
        Then it provides a valid Beautiful Soup document
        And get_link() returns the link subdocument
        When I call click() on the link
        Then it loads a new PageObject

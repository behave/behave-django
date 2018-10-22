@requires-live-http
Feature: Live server
    In order to prove that the live server works
    As the Maintainer
    I want to send an HTTP request
    
    Scenario: HTTP GET
        When I visit "/"
        Then I should see "Behave Django works"

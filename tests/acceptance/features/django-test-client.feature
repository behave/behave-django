Feature: Django's test client
    In order to ensure that the django's test client works in behave steps
    As the Maintainer
    I want to test if the client works
    
    Scenario: Django's test client
        When I use django's test client to visit "/"
        Then it should return a successful response

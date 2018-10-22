Feature: Database Transactions
    In order to test if transactions are done per scenario
    As the Maintainer
    I want to save two database items

    Scenario: Save the first item
        When I save the object
        Then I should only have one object

    Scenario: Save the second item
        When I save the object
        Then I should only have one object

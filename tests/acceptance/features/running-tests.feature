Feature: Running tests
    In order to prove that behave-django works
    As the Maintainer
    I want to test running behave against this features directory

    Scenario: The Test
        Given this step exists
        When I run "python manage.py behave"
        Then I should see the behave tests run

    Scenario: Test before_django_ready
        When I run "python manage.py behave"
        Then before_django_ready should be called

    Scenario: Test django_ready
        When I run "python manage.py behave"
        Then django_ready should be called

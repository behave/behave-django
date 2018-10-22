@requires-live-http
Feature: URL helpers are available in behave's context
    In order to ensure that url helpers are available as documented
    As the Maintainer
    I want to test all suggested uses

    Scenario: get_url() is an alias for the base_url property
        When I call get_url() without arguments
        Then it returns the value of base_url

    Scenario: The first argument in get_url() is appended to base_url if it is a path
        When I call get_url("/path/to/page/") with an absolute path
        Then the result is the base_url with "/path/to/page/" appended

    Scenario: The reversed view path is appended to base_url if the first argument in get_url() is a view name
        When I call get_url("admin:password_change") with a view name
        Then this returns the same result as get_url(reverse("admin:password_change"))
        And the result is the base_url with reverse("admin:password_change") appended

    Scenario: The model's absolute_url is appended to base_url if the first argument in get_url() is a model
        When I call get_url(model) with a model instance
        Then this returns the same result as get_url(model.get_absolute_url())
        And the result is the base_url with model.get_absolute_url() appended

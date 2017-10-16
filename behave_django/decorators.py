def fixtures(*fixture_files):
    """
    Provide fixtures for given step_impl. Fixtures will be loaded in
    environment.py#before_scenario.

    @fixtures('data.json')
    @when('a user clicks the button')
    def step_impl(context):
        pass

    :param fixture_files: list of fixture files
    """

    def wrapper(step_impl):
        setattr(step_impl, 'registered_fixtures', fixture_files)
        return step_impl

    return wrapper

from django.utils.module_loading import import_string


class FixtureRegister:
    """
    Expects a list of strings, holding either django-fixtures or paths to
    callables.
    """

    def __init__(self, *fixture_or_callable):
        self.modules = fixture_or_callable

    def setup(self, context):
        """
        Execute registered callables, and return fixture strings so they can
        be passed on to djangos testcase.
        """
        for fixture in self.modules:
            try:
                import_string(fixture)(context)
            except ImportError:
                yield fixture


def fixtures(*fixture_or_callable):
    """
    Provide fixtures for given step_impl. Fixtures will be loaded in
    environment.py#before_scenario, as this is the appropriate hook before
    the TestCase is loaded.

    @fixtures('mydata.json', 'path.to.my.callable')
    @when('a user clicks the button')
    def step_impl(context):
        pass

    :param fixture_or_callable: list of module-strings or fixture-files
    """

    def wrapper(step_impl):
        setattr(step_impl, 'fixtures', FixtureRegister(*fixture_or_callable))
        return step_impl

    return wrapper

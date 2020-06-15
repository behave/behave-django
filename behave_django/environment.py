from copy import copy

from behave import step_registry as module_step_registry
from behave.runner import ModelRunner, Context
from django.shortcuts import resolve_url


class PatchedContext(Context):

    @property
    def base_url(self):
        try:
            return self.test.live_server_url
        except AttributeError:
            raise RuntimeError('Web browser automation is not available. '
                               'This scenario step can not be run with the '
                               '--simple or -S flag.')

    def get_url(self, to=None, *args, **kwargs):
        return self.base_url + (
            resolve_url(to, *args, **kwargs) if to else '')


def load_registered_fixtures(context):
    """
    Apply fixtures that are registered with the @fixtures decorator.
    """
    # -- SELECT STEP REGISTRY:
    # HINT: Newer behave versions use runner.step_registry
    # to be able to support multiple runners, each with its own step_registry.
    runner = context._runner    # pylint: disable=protected-access
    step_registry = getattr(runner, 'step_registry', None)
    if not step_registry:
        # -- BACKWARD-COMPATIBLE: Use module_step_registry
        step_registry = module_step_registry.registry

    # -- SETUP SCENARIO FIXTURES:
    for step in context.scenario.all_steps:
        match = step_registry.find_match(step)
        if match and hasattr(match.func, 'registered_fixtures'):
            if not context.test.fixtures:
                context.test.fixtures = []
            context.test.fixtures.extend(match.func.registered_fixtures)


class BehaveHooksMixin(object):
    """
    Provides methods that run during test execution

    These methods are attached to behave via monkey patching.
    """
    testcase_class = None

    def patch_context(self, context):
        """
        Patches the context to add utility functions

        Sets up the base_url, and the get_url() utility function.
        """
        context.__class__ = PatchedContext
        # Simply setting __class__ directly doesn't work
        # because behave.runner.Context.__setattr__ is implemented wrongly.
        object.__setattr__(context, '__class__', PatchedContext)

    def setup_testclass(self, context):
        """
        Adds the test instance to context
        """
        context.test = self.testcase_class()

    def setup_fixtures(self, context):
        """
        Sets up fixtures
        """
        if getattr(context, 'fixtures', None):
            context.test.fixtures = copy(context.fixtures)

        if getattr(context, 'reset_sequences', None):
            context.test.reset_sequences = context.reset_sequences

        if getattr(context, 'databases', None):
            context.test.__class__.databases = context.databases

        if hasattr(context, 'scenario'):
            load_registered_fixtures(context)

    def setup_test(self, context):
        """
        Sets up the Django test

        This method runs the code necessary to create the test database, start
        the live server, etc.
        """
        context.test._pre_setup(run=True)
        context.test.setUpClass()
        context.test()

    def teardown_test(self, context):
        """
        Tears down the Django test
        """
        context.test.tearDownClass()
        context.test._post_teardown(run=True)
        del context.test


def monkey_patch_behave(django_test_runner):
    """
    Integrate behave_django in behave via before/after scenario hooks
    """
    behave_run_hook = ModelRunner.run_hook

    def run_hook(self, name, context, *args):
        if name == 'before_all':
            django_test_runner.patch_context(context)

        behave_run_hook(self, name, context, *args)

        if name == 'before_scenario':
            django_test_runner.setup_testclass(context)
            django_test_runner.setup_fixtures(context)
            django_test_runner.setup_test(context)
            behave_run_hook(self, 'django_ready', context)

        if name == 'after_scenario':
            django_test_runner.teardown_test(context)

    ModelRunner.run_hook = run_hook

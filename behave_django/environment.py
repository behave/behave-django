import inspect
from copy import copy

import django
from behave import step_registry as module_step_registry
from behave.runner import Context, ModelRunner
from django.shortcuts import resolve_url


class PatchedContext(Context):
    """Provides methods for Behave's ``context`` variable."""

    @property
    def base_url(self):
        try:
            return self.test.live_server_url
        except AttributeError as err:
            msg = (
                'Web browser automation is not available. '
                'This scenario step can not be run with the --simple or -S flag.'
            )
            raise RuntimeError(msg) from err

    def get_url(self, to=None, *args, **kwargs):
        return self.base_url + (resolve_url(to, *args, **kwargs) if to else '')


def load_registered_fixtures(context):
    """
    Apply fixtures that are registered with the @fixtures decorator.
    """
    # -- SELECT STEP REGISTRY:
    # HINT: Newer behave versions use runner.step_registry
    # to be able to support multiple runners, each with its own step_registry.
    runner = context._runner
    step_registry = getattr(runner, 'step_registry', None)
    if not step_registry:
        # -- BACKWARD-COMPATIBLE: Use module_step_registry
        step_registry = module_step_registry.registry

    # -- SETUP SCENARIO FIXTURES:
    for step in context.scenario.all_steps:
        match = step_registry.find_match(step)
        if match and hasattr(match.func, 'registered_fixtures'):
            if django.VERSION >= (5, 2):
                if (
                    not hasattr(context.test.__class__, 'fixtures')
                    or not context.test.__class__.fixtures
                ):
                    context.test.__class__.fixtures = []
                context.test.__class__.fixtures.extend(match.func.registered_fixtures)
            else:
                if not context.test.fixtures:
                    context.test.fixtures = []
                context.test.fixtures.extend(match.func.registered_fixtures)


class BehaveHooksMixin:
    """
    Provides methods that run during test execution.

    These methods are attached to behave via monkey patching.
    """

    testcase_class = None

    def patch_context(self, context):
        """Patch the context to add utility functions.

        Sets up the base_url, and the get_url() utility function.
        """
        context.__class__ = PatchedContext
        # Simply setting __class__ directly doesn't work
        # because behave.runner.Context.__setattr__ is implemented wrongly.
        object.__setattr__(context, '__class__', PatchedContext)

    def setup_testclass(self, context):
        """Add the test instance to context."""
        context.test = self.testcase_class()

    def setup_fixtures(self, context):
        """Set up fixtures."""

        if getattr(context, 'fixtures', None):
            if django.VERSION >= (5, 2):
                context.test.__class__.fixtures = copy(context.fixtures)
            else:
                context.test.fixtures = copy(context.fixtures)

        if getattr(context, 'reset_sequences', None):
            if django.VERSION >= (5, 2):
                context.test.__class__.reset_sequences = context.reset_sequences
            else:
                context.test.reset_sequences = context.reset_sequences

        if getattr(context, 'databases', None):
            context.test.__class__.databases = context.databases

        if hasattr(context, 'scenario'):
            load_registered_fixtures(context)

    def setup_test(self, context):
        """Set up the Django test.

        This method runs the code necessary to create the test database, start
        the live server, etc.
        """
        if django.VERSION >= (5, 2):
            context.test.__class__._pre_setup(run=True)
        else:
            context.test._pre_setup(run=True)
        context.test.setUpClass()
        context.test()

    def teardown_test(self, context):
        """Tear down the Django test."""
        context.test.tearDownClass()
        context.test._post_teardown(run=True)
        del context.test


def monkey_patch_behave(django_test_runner):
    """
    Integrate behave_django in behave via before/after scenario hooks.
    """
    behave_run_hook = ModelRunner.run_hook

    # Check if the new Behave version uses the updated run_hook signature.
    # In newer versions, the signature is (self, hook_name, *args) and
    # context is accessed via `self.context`.
    # In older versions, it was (self, name, context, *args)
    sig = inspect.signature(behave_run_hook)
    param_names = list(sig.parameters.keys())
    # New version uses 'hook_name', old used 'name'
    # See https://github.com/behave/behave/commit/f4d5028
    uses_new_signature = 'hook_name' in param_names

    if uses_new_signature:
        # New Behave version: context is available as self.context
        def run_hook(self, hook_name, *args):
            context = self.context

            if hook_name == 'before_all':
                django_test_runner.patch_context(context)

            behave_run_hook(self, hook_name, *args)

            if hook_name == 'before_scenario':
                django_test_runner.setup_testclass(context)
                django_test_runner.setup_fixtures(context)
                django_test_runner.setup_test(context)
                # In new Behave version, context is automatically passed by run_hook
                behave_run_hook(self, 'django_ready')

            if hook_name == 'after_scenario':
                django_test_runner.teardown_test(context)
    else:
        # Old Behave version: context is passed as parameter
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

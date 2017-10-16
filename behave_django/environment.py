from behave import step_registry
from behave.runner import ModelRunner, Context
from django.shortcuts import resolve_url


class PatchedContext(Context):

    @property
    def base_url(self):
        assert hasattr(self.test, 'live_server_url'), (
            'Web browser automation is not available.'
            ' This scenario step can not be run'
            ' with the --simple or -S flag.')
        return self.test.live_server_url

    def get_url(self, to=None, *args, **kwargs):
        return self.base_url + (
            resolve_url(to, *args, **kwargs) if to else '')


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

    def before_scenario(self, context):
        """
        Method that runs immediately before behave's before_scenario function

        Sets up the test case.
        """
        context.test = self.testcase_class()

        if getattr(context, 'fixtures', None):
            context.test.fixtures = context.fixtures

        if getattr(context, 'reset_sequences', None):
            context.test.reset_sequences = context.reset_sequences

        if hasattr(context, 'scenario'):
            self.load_registered_fixtures(context=context)

        context.test._pre_setup(run=True)
        context.test.setUpClass()
        context.test()

    def after_scenario(self, context):
        """
        Method that runs immediately after behave's after_scenario function
        """
        context.test.tearDownClass()
        context.test._post_teardown(run=True)
        del context.test

    def load_registered_fixtures(self, context):
        """
        Apply fixtures that are registered with the @fixtures decorator.
        """
        for step in context.scenario.all_steps:
            match = step_registry.registry.find_match(step)
            if match and hasattr(match.func, 'registered_fixtures'):
                if not context.test.fixtures:
                    context.test.fixtures = []
                context.test.fixtures.extend(match.func.registered_fixtures)


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
            django_test_runner.before_scenario(context)

        if name == 'after_scenario':
            django_test_runner.after_scenario(context)

    ModelRunner.run_hook = run_hook

import django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.testcases import TestCase


class PreventTestSetupMixin:
    """Prevents the TestCase from executing its setup and teardown methods.

    This mixin overrides the test case's ``_pre_setup`` and ``_post_teardown``
    methods in order to prevent them from executing when the test case is
    instantiated.  We do this to have total control over the test execution.

    Django 5.2 changed ``_pre_setup`` and ``_fixture_setup`` to classmethods,
    hence the conditional handling below.
    See https://github.com/django/django/commit/8eca3e9b
    """

    def _post_teardown(self, run=False):
        if run:
            super()._post_teardown()

    def runTest(self):
        pass


if django.VERSION < (5, 2):

    class BehaviorDrivenTestMixin(PreventTestSetupMixin):
        def _pre_setup(self, run=False):
            if run:
                super()._pre_setup()

    class PreventFixturesMixin:
        def _fixture_setup(self):
            pass

else:  # Django 5.2 introduced some classmethods

    class BehaviorDrivenTestMixin(PreventTestSetupMixin):
        @classmethod
        def _pre_setup(cls, run=False):
            if run:
                super()._pre_setup()

    class PreventFixturesMixin:
        @classmethod
        def _fixture_setup(cls):
            pass


class BehaviorDrivenTestCase(BehaviorDrivenTestMixin, StaticLiveServerTestCase):
    """Test case attached to the context during behave execution.

    This test case prevents the regular tests from running.
    """


class ExistingDatabaseTestCase(PreventFixturesMixin, BehaviorDrivenTestCase):
    """Test case used for the --use-existing-database setup.

    This test case prevents fixtures from being loaded to the database in use.
    """

    def _fixture_teardown(self):
        pass


class DjangoSimpleTestCase(BehaviorDrivenTestMixin, TestCase):
    """Test case attached to the context during behave execution.

    This test case uses `transaction.atomic()` to achieve test isolation
    instead of flushing the entire database. As a result, tests run much
    quicker and have no issues with altered DB state after all tests ran
    when `--keepdb` is used.

    As a side effect, this test case does not support web browser automation.
    Use Django's testing client instead to test requests and responses.

    Also, it prevents the regular tests from running.
    """

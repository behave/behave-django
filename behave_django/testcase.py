from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.testcases import TestCase


class BehaviorDrivenTestMixin:
    """Prevents the TestCase from executing its setup and teardown methods.

    This mixin overrides the test case's ``_pre_setup`` and ``_post_teardown``
    methods in order to prevent them from executing when the test case is
    instantiated.  We do this to have total control over the test execution.
    """

    def _pre_setup(self, run=False):
        if run:
            super()._pre_setup()

    def _post_teardown(self, run=False):
        if run:
            super()._post_teardown()

    def runTest(self):
        pass


class BehaviorDrivenTestCase(BehaviorDrivenTestMixin, StaticLiveServerTestCase):
    """Test case attached to the context during behave execution.

    This test case prevents the regular tests from running.
    """


class ExistingDatabaseTestCase(BehaviorDrivenTestCase):
    """Test case used for the --use-existing-database setup.

    This test case prevents fixtures from being loaded to the database in use.
    """

    def _fixture_setup(self):
        pass

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

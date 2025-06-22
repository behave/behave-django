"""
TestCase classes to prevent unit tests from being executed.

We want to run Behave under the hood instead of unit tests.
We do this by disabling the setup, teardown and fixture loading methods
of Django's TestCase classes. This way we can reuse what the Django
project adds to Python's unittest setup, yet having full total control
over the test execution.

Django 5.2 changed ``_pre_setup`` and ``_fixture_setup`` to classmethods,
hence the conditional handling below.
See https://github.com/django/django/commit/8eca3e9b
"""

import django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.testcases import TestCase

if django.VERSION < (5, 2):

    class PreventTestExecutionMixin:
        def _pre_setup(self, run=False):
            if run:
                super()._pre_setup()

        def _post_teardown(self, run=False):
            if run:
                super()._post_teardown()

        def runTest(self):
            pass

    class PreventFixturesMixin:
        def _fixture_setup(self):
            pass

        def _fixture_teardown(self):
            pass

else:  # Django 5.2 introduced some classmethods

    class PreventTestExecutionMixin:
        @classmethod
        def _pre_setup(cls, run=False):
            if run:
                super()._pre_setup()

        def _post_teardown(self, run=False):
            if run:
                super()._post_teardown()

        def runTest(self):
            pass

    class PreventFixturesMixin:
        @classmethod
        def _fixture_setup(cls):
            pass

        def _fixture_teardown(self):
            pass


class BehaviorDrivenTestCase(PreventTestExecutionMixin, StaticLiveServerTestCase):
    """Test case attached to the context during behave execution.

    This test case prevents the regular tests from running.
    """


class ExistingDatabaseTestCase(
    PreventFixturesMixin, PreventTestExecutionMixin, StaticLiveServerTestCase
):
    """Test case used for the --use-existing-database setup.

    This test case prevents fixtures from being loaded to the database in use.
    """


class DjangoSimpleTestCase(PreventTestExecutionMixin, TestCase):
    """Test case attached to the context during behave execution.

    This test case uses `transaction.atomic()` to achieve test isolation
    instead of flushing the entire database. As a result, tests run much
    quicker and have no issues with altered DB state after all tests ran
    when `--keepdb` is used.

    As a side effect, this test case does not support web browser automation.
    Use Django's testing client instead to test requests and responses.

    Also, it prevents the regular tests from running.
    """

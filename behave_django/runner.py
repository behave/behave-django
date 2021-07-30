from django.conf import settings
from django.test.utils import get_runner

from behave_django.environment import BehaveHooksMixin
from behave_django.testcase import (BehaviorDrivenTestCase,
                                    ExistingDatabaseTestCase,
                                    DjangoSimpleTestCase)


DJANGO_CONFIGURED_RUNNER = get_runner(settings)
"""
90% of times DJANGO_CONFIGURED_RUNNER will be DiscoverRunner.
The other 10% the user will have another django complied runner.

For more info:
- https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#using-the-django-test-runner-to-test-reusable-applications  # noqa
- https://docs.djangoproject.com/en/3.2/ref/settings/#test-runner
"""


class BehaviorDrivenTestRunner(DJANGO_CONFIGURED_RUNNER, BehaveHooksMixin):
    """
    Test runner that uses the BehaviorDrivenTestCase
    """
    testcase_class = BehaviorDrivenTestCase


class ExistingDatabaseTestRunner(DJANGO_CONFIGURED_RUNNER, BehaveHooksMixin):
    """
    Test runner that uses the ExistingDatabaseTestCase

    This test runner nullifies Django's test database setup methods. Using this
    test runner would make your tests run with the default configured database
    in settings.py.
    """
    testcase_class = ExistingDatabaseTestCase

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass


class SimpleTestRunner(DJANGO_CONFIGURED_RUNNER, BehaveHooksMixin):
    """
    Test runner that uses DjangoSimpleTestCase with atomic
    transaction management and no support of web browser automation.
    """
    testcase_class = DjangoSimpleTestCase

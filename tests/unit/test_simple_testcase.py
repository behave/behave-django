import os
from unittest import mock

import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

"""
We need to configure Django settings now because
the Runner is retrived dynamically by Django!
"""

from behave_django.runner import SimpleTestRunner  # noqa:
from behave.runner import Context, Runner  # noqa:
from django.test.testcases import TestCase  # noqa:

from .util import DjangoSetupMixin  # noqa:


class TestSimpleTestCase(DjangoSetupMixin):

    @mock.patch('behave_django.management.commands.behave.behave_main', return_value=0)  # noqa
    @mock.patch('behave_django.management.commands.behave.SimpleTestRunner')  # noqa
    def test_use_simple_test_runner(self,
                                    mock_simple_test_runner,
                                    mock_behave_main):
        self.run_management_command('behave', simple=True)
        mock_behave_main.assert_called_once_with(args=[])
        mock_simple_test_runner.assert_called_once_with()

    def test_simple_test_runner_uses_simple_testcase(self):
        runner = mock.MagicMock()
        context = Context(runner)
        SimpleTestRunner().setup_testclass(context)
        assert isinstance(context.test, TestCase)

    def test_simple_testcase_fails_when_accessing_base_url(self):
        runner = Runner(mock.MagicMock())
        runner.context = Context(runner)
        SimpleTestRunner().patch_context(runner.context)
        SimpleTestRunner().setup_testclass(runner.context)
        with pytest.raises(RuntimeError):
            assert runner.context.base_url == 'should raise an exception!'

    def test_simple_testcase_fails_when_calling_get_url(self):
        runner = Runner(mock.MagicMock())
        runner.context = Context(runner)
        SimpleTestRunner().patch_context(runner.context)
        SimpleTestRunner().setup_testclass(runner.context)
        with pytest.raises(RuntimeError):
            runner.context.get_url()

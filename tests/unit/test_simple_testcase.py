try:
    from unittest import mock
except ImportError:
    import mock

import pytest

from behave_django.runner import SimpleTestRunner
from behave.runner import Context, Runner
from django.test.testcases import TestCase

from .util import DjangoSetupMixin


class FakeSimpleTestRunner(SimpleTestRunner):
    """Wrapper around SimpleTestRunner.

    Without this we would be running a lot of setup/teardown code thats
    unnecessary for this test.
    """
    def setup_test_environment(self, *args, **kargs):
        pass

    def setup_databases(self, *args, **kargs):
        pass

    def teardown_databases(self, *args, **kargs):
        pass

    def teardown_test_environment(self, *args, **kargs):
        pass


mock_simple_test_runner = mock.Mock(wraps=FakeSimpleTestRunner)


class TestSimpleTestCase(DjangoSetupMixin):

    def setup_method(self):
        mock_simple_test_runner.reset_mock()

    @mock.patch('behave_django.management.commands.behave.behave_main', return_value=0)  # noqa
    @mock.patch('behave_django.runner.SimpleTestRunner', mock_simple_test_runner)  # noqa
    def test_use_simple_test_runner(self,
                                    mock_behave_main):
        with mock.patch('sys.argv', ['test.py', 'behave', '--simple']):
            self.run_management_command('behave', simple=True)
        mock_behave_main.assert_called_once_with(args=[])
        mock_simple_test_runner.assert_called_once_with(keepdb=False,
                                                        reverse=False)

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

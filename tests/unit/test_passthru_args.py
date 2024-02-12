from unittest import mock

from .util import DjangoSetupMixin


@mock.patch('behave_django.management.commands.behave.behave_main', return_value=0)
@mock.patch('behave_django.runner.BehaviorDrivenTestRunner')
class TestPassThruArgs(DjangoSetupMixin):
    def test_keepdb_flag(self, mock_test_runner, mock_behave_main):
        """Test if keepdb is properly set on the test_runner."""

        self.run_management_command('behave', keepdb=True)
        _, kwargs = mock_test_runner.call_args
        assert kwargs['keepdb'] is True

    def test_interactive_flag(self, mock_test_runner, mock_behave_main):
        """Test if interactive is properly set on the test_runner."""

        self.run_management_command('behave', interactive=False)
        _, kwargs = mock_test_runner.call_args
        assert kwargs['interactive'] is False

    def test_failfast_flag(self, mock_test_runner, mock_behave_main):
        """Test if failfast is properly set on the test_runner."""

        self.run_management_command('behave', failfast=True)
        _, kwargs = mock_test_runner.call_args
        assert kwargs['failfast'] is True

    def test_reverse_flag(self, mock_test_runner, mock_behave_main):
        """Test if reverse is properly set on the test_runner."""

        self.run_management_command('behave', reverse=True)
        _, kwargs = mock_test_runner.call_args
        assert kwargs['reverse'] is True

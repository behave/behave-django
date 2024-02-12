from unittest import mock

from .util import DjangoSetupMixin


class TestExitCodes(DjangoSetupMixin):
    @mock.patch('behave_django.management.commands.behave.behave_main', return_value=0)
    @mock.patch('sys.exit')
    def test_command_should_exit_zero_if_passing(self, mock_sys_exit, mock_behave_main):
        # If the exit status returned by behave_main is 0, make sure sys.exit
        # does not get called
        self.run_management_command('behave', dry_run=True)
        assert not mock_sys_exit.called

    @mock.patch('behave_django.management.commands.behave.behave_main', return_value=1)
    @mock.patch('sys.exit')
    def test_command_should_exit_nonzero_if_failing(
        self, mock_sys_exit, mock_behave_main
    ):
        # If the exit status returned by behave_main is anything other than 0,
        # make sure sys.exit gets called with the exit code

        # Dry run to not create the database for faster tests
        self.run_management_command('behave', dry_run=True)
        mock_sys_exit.assert_called_once_with(1)

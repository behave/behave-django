from unittest import mock

from .util import DjangoSetupMixin


class TestUseExistingDB(DjangoSetupMixin):
    @mock.patch('behave_django.management.commands.behave.behave_main', return_value=0)
    @mock.patch('behave_django.management.commands.behave.ExistingDatabaseTestRunner')
    def test_dont_create_db_with_dryrun(
        self, mock_existing_database_runner, mock_behave_main
    ):
        self.run_management_command('behave', dry_run=True)
        mock_behave_main.assert_called_once_with(args=[])
        mock_existing_database_runner.assert_called_once_with()

    @mock.patch('behave_django.management.commands.behave.behave_main', return_value=0)
    @mock.patch('behave_django.management.commands.behave.ExistingDatabaseTestRunner')
    def test_dont_create_db_with_useexistingdb(
        self, mock_existing_database_runner, mock_behave_main
    ):
        self.run_management_command('behave', use_existing_database=True)
        mock_behave_main.assert_called_once_with(args=[])
        mock_existing_database_runner.assert_called_once_with()

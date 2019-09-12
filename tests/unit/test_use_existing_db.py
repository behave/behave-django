try:
    from unittest import mock
except ImportError:
    import mock

from .util import DjangoSetupMixin
from behave_django.runner import ExistingDatabaseTestRunner


class FakeExistingDatabaseTestRunner(ExistingDatabaseTestRunner):
    """Wrapper around ExistingDatabaseTestRunner.

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


mock_existing_database_runner = mock.Mock(wraps=FakeExistingDatabaseTestRunner)


@mock.patch('behave_django.management.commands.behave.behave_main', return_value=0)  # noqa
@mock.patch('behave_django.runner.ExistingDatabaseTestRunner', mock_existing_database_runner)  # noqa
class TestUseExistingDB(DjangoSetupMixin):

    def setup_method(self):
        mock_existing_database_runner.reset_mock()

    def test_dont_create_db_with_dryrun(self, mock_behave_main):
        with mock.patch('sys.argv', ['test.py', 'behave', '--dry-run']):
            self.run_management_command('behave', dry_run=True)
        mock_behave_main.assert_called_once_with(args=['--dry-run'])
        mock_existing_database_runner.assert_called_once_with(keepdb=False,
                                                              reverse=False)

    def test_dont_create_db_with_useexistingdb(self, mock_behave_main):
        argv = ['test.py', 'behave', '--use-existing-database']
        with mock.patch('sys.argv', argv):
            self.run_management_command('behave', use_existing_database=True)
        mock_behave_main.assert_called_once_with(args=[])
        mock_existing_database_runner.assert_called_once_with(keepdb=False,
                                                              reverse=False)

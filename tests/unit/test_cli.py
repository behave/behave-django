import os
from imp import reload

from .util import DjangoSetupMixin, run_silently, show_run_error


class TestCommandLine(DjangoSetupMixin):

    def test_additional_management_command_options(self):
        exit_status, output = run_silently(
            'python tests/manage.py behave --help')
        assert exit_status == 0, \
            show_run_error(exit_status, output)
        assert (
            os.linesep + '  --use-existing-database' + os.linesep) in output
        assert (
            os.linesep + '  -k, --keepdb') in output
        assert (
            os.linesep + '  -S, --simple') in output

    def test_should_accept_behave_arguments(self):
        from behave_django.management.commands.behave import Command
        command = Command()
        args = command.get_behave_args(
            argv=['manage.py', 'behave',
                  '--format', 'progress',
                  '--settings', 'test_project.settings',
                  '-i', 'some-pattern',
                  'features/running-tests.feature'])

        assert '--format' in args
        assert 'progress' in args
        assert '-i' in args
        assert 'some-pattern' in args

    def test_should_not_include_non_behave_arguments(self):
        from behave_django.management.commands.behave import Command
        command = Command()
        args = command.get_behave_args(
            argv=['manage.py', 'behave',
                  '--format', 'progress',
                  '--settings', 'test_project.settings',
                  'features/running-tests.feature'])

        assert '--settings' not in args
        assert 'test_project.settings' not in args

    def test_should_return_positional_args(self):
        from behave_django.management.commands.behave import Command
        command = Command()
        args = command.get_behave_args(
            argv=['manage.py', 'behave',
                  '--format', 'progress',
                  '--settings', 'test_project.settings',
                  'features/running-tests.feature'])

        assert 'features/running-tests.feature' in args

    def test_no_arguments_should_not_cause_issues(self):
        from behave_django.management.commands.behave import Command
        command = Command()
        args = command.get_behave_args(
            argv=['manage.py', 'behave'])

        assert args == []

    def test_positional_args_should_work(self):
        exit_status, output = run_silently(
            'python tests/manage.py behave'
            '    tests/acceptance/features/running-tests.feature')
        assert exit_status == 0, \
            show_run_error(exit_status, output)

    def test_command_import_dont_patch_behave_options(self):
        # We reload the tested imports because they
        # could have been imported by previous tests.
        import behave.configuration
        reload(behave.configuration)
        behave_options_backup = [
            (first, second.copy())
            for (first, second) in behave.configuration.options
        ]

        import behave_django.management.commands.behave
        reload(behave_django.management.commands.behave)

        assert behave.configuration.options == behave_options_backup

    def test_conflicting_options_should_get_prefixed(self):
        from behave_django.management.commands.behave import Command
        command = Command()
        args = command.get_behave_args(
            argv=['manage.py', 'behave', '--behave-k', '--behave-version'])

        assert args == ['-k', '--version']

    def test_simple_and_use_existing_database_flags_raise_a_warning(self):
        exit_status, output = run_silently(
            'python tests/manage.py behave'
            '    --simple --use-existing-database --tags=@skip-all'
        )
        assert exit_status == 0, \
            show_run_error(exit_status, output)
        assert (
            os.linesep +
            '--simple flag has no effect ' +
            'together with --use-existing-database' +
            os.linesep) in output

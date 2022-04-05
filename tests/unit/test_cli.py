import os
from importlib import reload

import pytest

from .util import DjangoSetupMixin, run_silently, show_run_error


class TestCommandLine(DjangoSetupMixin):

    def test_additional_management_command_options(self):
        exit_status, output = run_silently(
            'python tests/manage.py behave --help')
        assert exit_status == 0, \
            show_run_error(exit_status, output)
        assert (os.linesep + '  --use-existing-database' +
                os.linesep) in output
        assert (os.linesep + '  -k, --keepdb') in output
        assert (os.linesep + '  -S, --simple') in output
        assert (os.linesep + '  --runner-class') in output
        assert (os.linesep + '  --noinput, --no-input') in output
        assert (os.linesep + '  --failfast') in output
        assert (os.linesep + '  -r, --reverse') in output

    def test_should_accept_behave_arguments(self):
        from behave_django.management.commands.behave import Command
        command = Command()
        argv = [
            'manage.py', 'behave',
            '--format', 'progress',
            '--behave-runner-class', 'behave.runner.Runner',
            '--runner-class', 'behave_django.runner.BehaviorDrivenTestRunner',
            '--settings', 'test_project.settings',
            '-i', 'some-pattern',
            'features/running-tests.feature'
        ]
        args = command.get_behave_args(argv=argv)

        assert '--format' in args
        assert '--runner-class' in args
        assert args[args.index('--runner-class') + 1] == 'behave.runner.Runner'
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
            '--simple flag has no effect together with '
            '--use-existing-database' +
            os.linesep) in output

    @pytest.mark.parametrize('arguments, expect_error', [
        (
            '--runner-class behave_django.runner.BehaviorDrivenTestRunner',
            False
        ),
        (
            (
                '--runner-class behave_django.runner.SimpleTestRunner '
                '--simple'
            ),
            True
        ),
        (
            (
                '--runner-class behave_django.runner.BehaviorDrivenTestRunner '
                '--simple'
            ),
            False
        ),
        (
            (
                '--behave-runner-class behave.runner.Runner '
                '--runner-class behave_django.runner.SimpleTestRunner '
                '--simple'
            ),
            True
        ),
        (
            (
                '--runner-class behave_django.runner.SimpleTestRunner '
                '--use-existing-database'
            ),
            True
        ),
        ('--behave-runner-class behave.runner.Runner --simple', False),
        (
            (
                '--behave-runner-class behave.runner.Runner '
                '--runner-class behave_django.runner.BehaviorDrivenTestRunner'
            ),
            False
        ),
    ])
    def test_runner_class_and_others_flags_raise_a_warning(self, arguments,
                                                           expect_error):
        exit_status, output = run_silently(
            'python tests/manage.py behave'
            '    %s --tags=@skip-all' % arguments
        )
        assert exit_status == 0, \
            show_run_error(exit_status, output)

        warning_message = (
            os.linesep +
            '--use-existing-database or --simple has no effect'
            ' together with --runner-class' +
            os.linesep)
        if expect_error:
            assert warning_message in output
        else:
            assert warning_message not in output

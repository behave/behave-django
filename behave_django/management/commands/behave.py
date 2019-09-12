from __future__ import absolute_import
import sys
import os

from argparse import ArgumentError

from distutils.version import LooseVersion

from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.core.management.base import (BaseCommand, OutputWrapper,
                                         CommandParser)
from django.core.management.utils import CommandError
from django.test.utils import get_runner

from behave.configuration import options as behave_options
from behave.__main__ import main as behave_main
from behave_django.environment import monkey_patch_behave


# If django<2.0 mimic the django 2.2 code for better intercompatibility.
if LooseVersion('2.0') > LooseVersion('.'.join((str(x) for x in DJANGO_VERSION[:3]))):  # noqa: E501
    from argparse import ArgumentParser

    class CommandParser(ArgumentParser):  # noqa: F811
        """
        Customized ArgumentParser class to improve some error messages and
        prevent SystemExit in several occasions, as SystemExit is unacceptable
        when a command is called programmatically.
        """
        def __init__(self, **kwargs):
            self.missing_args_message = kwargs.pop('missing_args_message', None)  # noqa: E501
            self.called_from_command_line = kwargs.pop('called_from_command_line', None)  # noqa: E501
            kwargs.pop('allow_abbrev', False)
            super(CommandParser, self).__init__(**kwargs)

        def parse_args(self, args=None, namespace=None):
            # Catch missing argument for a better error message
            if (self.missing_args_message and
                    not (args or any(not arg.startswith('-') for arg in args))):  # noqa: E501
                self.error(self.missing_args_message)
            return super(CommandParser, self).parse_args(args, namespace)


def get_command_line_option(argv, *args, **kwargs):
    """
    Return the value of a command line option (which should include leading
    dashes, e.g. '--testrunner') from an argument list. Return None if the
    option wasn't passed or if the argument list couldn't be parsed.
    """
    kwargs['dest'] = 'value'
    parser = CommandParser(add_help=False, allow_abbrev=False)
    parser.add_argument(*args, **kwargs)
    try:
        options, _ = parser.parse_known_args(argv[2:])
    except CommandError:
        return None
    else:
        return options.value


def remove_option(parser, *arg):
    """Removes duplicate options from inside ArgumentParser.

    We have arguments being supplied by the DiscoverRunner and other
    arguments injected by the behave management command, if they conflict
    we want to keep the options from the behave management command and
    remove the latter.
    """
    for action in parser._actions:
        if any(option in arg for option in action.option_strings):
            parser._remove_action(action)

    for key, action in list(parser._option_string_actions.items()):
        if any(option in arg for option in action.option_strings):
            parser._option_string_actions.pop(key)

    for action in parser._action_groups:
        vars_action = vars(action)
        var_group_actions = vars_action['_group_actions']

        for action in var_group_actions:
            if any(option in arg for option in action.option_strings):
                var_group_actions.remove(action)


def add_behave_arguments(parser):  # noqa
    """
    Additional command line arguments extracted directly from behave
    """

    # Option strings that conflict with Django
    conflicts = [
        '--no-color',
        '--version',
        '-c',
        '-k',
        '-v',
        '-S',
        '--simple',
    ]

    parser.add_argument(
        'paths',
        action='store',
        nargs='*',
        help="Feature directory, file or file location (FILE:LINE)."
    )

    for fixed, keywords in behave_options:
        keywords = keywords.copy()

        # Configfile only entries are ignored
        if not fixed:
            continue

        # Build option strings
        option_strings = []
        for option in fixed:
            # Prefix conflicting option strings with `--behave`
            if option in conflicts:
                prefix = '--' if option.startswith('--') else '-'
                option = option.replace(prefix, '--behave-', 1)

            option_strings.append(option)

        # config_help isn't a valid keyword for add_argument
        if 'config_help' in keywords:
            keywords['help'] = keywords['config_help']
            del keywords['config_help']

        try:
            parser.add_argument(*option_strings, **keywords)
        except ArgumentError:
            remove_option(parser, *fixed)
            parser.add_argument(*option_strings, **keywords)


class Command(BaseCommand):
    help = 'Runs behave tests'
    test_runner = None

    DEFAULT_TEST_RUNNER = 'behave_django.runner.BehaviorDrivenTestRunner'
    SIMPLE_TEST_RUNNER = 'behave_django.runner.SimpleTestRunner'
    EXISTING_TEST_RUNNER = 'behave_django.runner.ExistingDatabaseTestRunner'

    def init_test_runner(self, argv=None):
        """
        Pre-parse the command line to extract the value of the --testrunner
        option. This allows a test runner to define additional command line
        arguments.
        """

        argv = argv or sys.argv
        self.test_runner = get_command_line_option(argv, '--testrunner')
        use_simple = get_command_line_option(argv, '-S', '--simple',
                                             action='store_true',
                                             default=False)
        use_existing_database = get_command_line_option(
            argv,
            '--use-existing-database',
            action='store_true',
            default=False
        )
        use_dry_run = get_command_line_option(
            argv,
            '--dry-run',
            action='store_true',
            default=False
        )
        if use_simple:
            # TODO: Delete in upcoming version
            self.stderr.write(self.style.WARNING(
                '-S/--simple has been depricated, please use: '
                '"--testrunner behave_django.runner.SimpleTestRunner"'
            ))
            self.test_runner = self.SIMPLE_TEST_RUNNER
        elif use_existing_database:
            # TODO: Delete in upcoming version
            self.stderr.write(self.style.WARNING(
                '--use-existing-database has been depricated, please use: '
                '"--testrunner behave_django.runner.'
                'ExistingDatabaseTestRunner"'
            ))
            self.test_runner = self.EXISTING_TEST_RUNNER
        elif use_dry_run:
            # TODO: Delete in upcoming version
            self.test_runner = self.EXISTING_TEST_RUNNER

    def add_arguments(self, parser, append_behave=True):
        """
        Add behave's and our command line arguments to the command
        """

        if not self.test_runner:
            self.init_test_runner()

        parser.usage = "%(prog)s [options] [ [DIR|FILE|FILE:LINE] ]+"
        parser.description = """\
        Run a number of feature tests with behave."""

        test_runner_class = get_runner(settings, self.test_runner or
                                       self.DEFAULT_TEST_RUNNER)

        if hasattr(test_runner_class, 'add_arguments'):
            test_runner_class.add_arguments(parser)

        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_const',
            const=False,
            dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )
        parser.add_argument(
            '--failfast', action='store_const', const=True, dest='failfast',
            help=('Tells Django to stop running the '
                  'test suite after first failed test.'),
        )
        parser.add_argument(
            '--use-existing-database',
            action='store_true',
            default=False,
            help="Don't create a test database. USE AT YOUR OWN RISK!",
        )
        parser.add_argument(
            '-S', '--simple',
            action='store_true',
            default=False,
            help="Use simple test runner that supports Django's"
            " testing client only (no web browser automation)"
        )
        parser.add_argument(
            '--testrunner', action='store', dest='testrunner',
            help='Tells Django to use specified test runner class instead of '
                 'the one specified by the TEST_RUNNER setting.',
        )

        parser.parse_args

        if append_behave:
            add_behave_arguments(parser)

    def handle(self, *args, **options):

        # Check the flags
        if options['use_existing_database'] and options['simple']:
            self.stderr.write(self.style.WARNING(
                '--simple flag has no effect'
                ' together with --use-existing-database'
            ))

        # Configure django environment
        passthru_args = ('failfast',
                         'interactive',
                         'keepdb',
                         'reverse')
        runner_args = {k: v for
                       k, v in
                       options.items() if k in passthru_args and v is not None}

        TestRunner = get_runner(settings, self.test_runner or
                                self.DEFAULT_TEST_RUNNER)
        django_test_runner = TestRunner(**runner_args)
        django_test_runner.setup_test_environment()

        old_config = django_test_runner.setup_databases()

        # Run Behave tests
        monkey_patch_behave(django_test_runner)
        behave_args = self.get_behave_args()
        exit_status = behave_main(args=behave_args)

        # Teardown django environment
        django_test_runner.teardown_databases(old_config)
        django_test_runner.teardown_test_environment()

        if exit_status != 0:
            sys.exit(exit_status)

    def get_behave_args(self, argv=None):
        """
        Get a list of those command line arguments specified with the
        management command that are meant as arguments for running behave.
        """
        argv = argv or sys.argv
        parser = BehaveArgsHelper().create_parser('manage.py', 'behave')
        args, unknown = parser.parse_known_args(argv[2:])

        behave_args = []
        for option in unknown:
            # Remove behave prefix
            if option.startswith('--behave-'):
                option = option.replace('--behave-', '', 1)
                prefix = '-' if len(option) == 1 else '--'
                option = prefix + option

            behave_args.append(option)

        return behave_args


class BehaveArgsHelper(Command):

    def __init__(self, *args, **kwargs):
        """
        Let's ignore any and all output that comes out of here, all the mayor
        warning were already shown to the user inside the original Command,
        there is no need to duplicate the messages.
        """
        super(BehaveArgsHelper, self).__init__(self, *args, **kwargs)
        f = open(os.devnull, 'w')
        self.stdout = OutputWrapper(f)
        self.stderr = OutputWrapper(f)

    def add_arguments(self, parser):
        """
        Override setup of command line arguments to make behave commands not
        be recognized. The unrecognized args will then be for behave! :)
        """
        super(BehaveArgsHelper, self).add_arguments(parser,
                                                    append_behave=False)

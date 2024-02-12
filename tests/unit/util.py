import os
from subprocess import PIPE, Popen

import django
from django.core.management import call_command


class DjangoSetupMixin:
    @classmethod
    def setup_class(cls):
        # NOTE: this may potentially have side-effects, making tests pass
        # that would otherwise fail, because it *always* overrides which
        # settings module is used.
        os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

    def run_management_command(self, command, *args, **kwargs):
        django.setup()
        call_command(command, *args, **kwargs)


def run_silently(command):
    """Run a shell command and return both exit_status and console output."""
    command_args = command.split()
    process = Popen(command_args, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    stdout, stderr = process.communicate()
    output = (
        stdout.decode('UTF-8') + os.linesep + stderr.decode('UTF-8')
    ).strip() + os.linesep
    return process.returncode, output


def show_run_error(exit_status, output):
    """An easy-to-read error message for assert"""
    return f'Failed with exit status {exit_status}\n--------------\n{output}'

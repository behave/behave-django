import os

import django
from django.core.management import call_command


class DjangoSetupMixin(object):

    @classmethod
    def setup_class(cls):
        # NOTE: this may potentially have side-effects, making tests pass
        # that would otherwise fail, because it *always* overrides which
        # settings module is used.
        os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

    def run_management_command(self, command, *args, **kwargs):
        django.setup()
        call_command(command, *args, **kwargs)

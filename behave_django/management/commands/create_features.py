import os

from django.core.management.base import BaseCommand
from django.conf import settings


def write_step_file(step_file):
    with open(step_file, "w") as python_file:
        python_file.write(
            """from behave import *


@given("we have behave installed")
def step_impl(context):
    raise NotImplementedError(u'STEP: Given we have behave installed')


@when("we implement a test")
def step_impl(context):
    raise NotImplementedError(u'STEP: When we implement a test')


@then("behave will test it for us!")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then behave will test it for us!') 
"""
        )


def write_feature_file(feature_file):
    with open(feature_file, "w") as gherkin_file:
        gherkin_file.write(
            """Feature: showing off behave

     Scenario: run a simple test
        Given we have behave installed
         When we implement a test
         Then behave will test it for us!
    """
        )


class Command(BaseCommand):
    help = "Create a gherkin and step files for behave-django."

    def add_arguments(self, parser):
        parser.add_argument(
            "feature_name", nargs="+", type=str, help="name of feature"
        )

    def handle(self, *args, **options):
        if not hasattr(settings, "BEHAVE_DJANGO_FEATURES_DIR"):
            self.stdout.write(
                self.style.ERROR(
                    "Set BEHAVE_DJANGO_FEATURES_DIR on your settings file."
                )
            )
            return

        for feature_name in options["feature_name"]:
            feature_dir = os.path.join(
                settings.BEHAVE_DJANGO_FEATURES_DIR, "features"
            )
            steps_dir = os.path.join(feature_dir, "steps")
            feature_file = os.path.join(
                feature_dir, "{}.feature".format(feature_name)
            )
            step_file = os.path.join(
                feature_dir, steps_dir, "{}.py".format(feature_name)
            )

            if os.path.isfile(step_file) or os.path.isfile(feature_file):
                if os.path.isfile(step_file):
                    self.stdout.write(
                        self.style.ERROR(
                            "A step file already exists for the feature {}".format(
                                feature_name
                            )
                        )
                    )
                if os.path.isfile(feature_file):
                    self.stdout.write(
                        self.style.ERROR(
                            "A feature file already exists for the feature {}".format(
                                feature_name
                            )
                        )
                    )
            else:
                if os.path.isdir(feature_dir):
                    write_feature_file(feature_file)
                    if os.path.isdir(steps_dir):
                        write_step_file(step_file)
                    else:
                        os.mkdir(steps_dir)
                        write_step_file(step_file)
                else:
                    os.mkdir(feature_dir)
                    os.mkdir(steps_dir)
                    write_feature_file(feature_file)
                    write_step_file(step_file)

                self.stdout.write(
                    self.style.SUCCESS(
                        "Feature file: {} created".format(feature_file)
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "Step file: {} created".format(step_file)
                    )
                )

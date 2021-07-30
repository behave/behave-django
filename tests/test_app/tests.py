from django.test import TestCase
from django.test.runner import DiscoverRunner

# Create your tests here.


class MyCustomTestRunner(DiscoverRunner):
    is_custom = True


class MyCustomTestCase(TestCase):
    is_custom = True

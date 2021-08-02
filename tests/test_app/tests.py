from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.runner import DiscoverRunner


# Create your tests here.


class MyCustomTestRunner(DiscoverRunner):
    is_custom = True


class MyCustomTestCase(StaticLiveServerTestCase):
    is_custom = True

import sys
import traceback

from behave import then
from django.conf import settings


@then('a Django setting can be accessed with a recursion headroom of {headroom:d}')
def access_django_setting(context, headroom):
    depth = len(traceback.extract_stack())
    settings.__dict__.pop('DEBUG', None)
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(depth + headroom)
    try:
        _ = settings.DEBUG
    finally:
        sys.setrecursionlimit(old_limit)

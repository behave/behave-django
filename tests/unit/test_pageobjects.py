"""
Tests for the pageobject module
"""

from http import HTTPStatus
from unittest import mock

import django
import pytest
from django.test import Client
from django.test.utils import override_settings

from behave_django.pageobject import (
    Element,
    Link,
    PageObject,
    WrongElementError,
)

from .util import DjangoSetupMixin


class HomePage(PageObject):
    page = 'home'
    elements = {
        'heading': Element('h1'),
        'about_link': Link('a[role="about"]'),
    }


class TestElement:
    def test_element_stores_css_selector(self):
        element = Element('div.foo')
        assert element.selector == 'div.foo'

    def test_link_is_an_element(self):
        link = Link('a.nav')
        assert isinstance(link, Element)
        assert link.selector == 'a.nav'


class TestWrongElementError:
    def test_is_runtime_error(self):
        assert issubclass(WrongElementError, RuntimeError)

    def test_error_message_mentions_expected_and_actual(self):
        error = WrongElementError(Element('div'), expected=Link)
        message = str(error)
        assert 'Element' in message
        assert 'Link' in message


class TestPageObject(DjangoSetupMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        django.setup()
        cls._overrides = override_settings(ALLOWED_HOSTS=['testserver'])
        cls._overrides.enable()

    @classmethod
    def teardown_class(cls):
        cls._overrides.disable()

    @staticmethod
    def _build_context():
        context = mock.MagicMock()
        context.test.client = Client()
        return context

    def test_loads_page_via_view_name(self):
        page = HomePage(self._build_context())
        assert page.response.status_code == HTTPStatus.OK
        assert page.request['PATH_INFO'] == '/'

    def test_get_element_returns_first_match(self):
        page = HomePage(self._build_context())
        heading = page.get_element('heading')
        assert heading.text.strip() == 'Behave Django works'

    def test_get_elements_returns_all_matches(self):
        page = HomePage(self._build_context())
        headings = page.get_elements('heading')
        assert len(headings) == 1

    def test_get_element_for_unknown_name_raises_key_error(self):
        page = HomePage(self._build_context())
        with pytest.raises(KeyError):
            page.get_element('does_not_exist')

    def test_get_link_when_type_mismatch_raises_wrong_element_error(self):
        page = HomePage(self._build_context())
        with pytest.raises(WrongElementError):
            page.get_link('heading')

    def test_get_link_returns_clickable_link(self):
        page = HomePage(self._build_context())
        about_link = page.get_link('about_link')
        assert about_link.get('href') == '/about/'

    def test_clicking_link_loads_target_page(self):
        page = HomePage(self._build_context())
        about_page = page.get_link('about_link').click()
        assert about_page.response.status_code == HTTPStatus.OK
        assert about_page.request['PATH_INFO'] == '/about/'

    def test_equal_pages_compare_equal(self):
        context = self._build_context()
        page_a = HomePage(context)
        page_b = HomePage(context)
        assert page_a == page_b

    def test_non_pageobject_is_not_equal(self):
        page = HomePage(self._build_context())
        assert page != 'not a page'

    def test_page_object_is_hashable(self):
        page = HomePage(self._build_context())
        assert isinstance(hash(page), int)

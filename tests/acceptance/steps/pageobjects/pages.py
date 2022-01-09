from behave_django.pageobject import Link, PageObject


class Welcome(PageObject):
    page = 'home'  # view name, model or URL path
    elements = {
        'about': Link(css='footer a[role=about]'),
    }


class About(PageObject):
    page = 'about'

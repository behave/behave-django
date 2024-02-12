Release History
---------------

1.5.0 (unreleased)
++++++++++++++++++

**Features and Improvements**

- Use ruff for linting and code style; reformat code base
- Migrate packaging from ``setup.py`` to pure ``pyproject.toml``.
- Add instructions to measure test coverage to the documentation
- Cover Python 3.9 to 3.12 and Django 3.2, 4.2 and 5.0, drop Python 3.5, 3.6 and Django 2.2 and 3.0 support
- Bump Behave requirement to 1.2.7.dev3/4/5 (allows TOML support and option to change the Behave TestRunner)
- New option to change the Django TestRunner

1.4.0 (2020-06-15)
++++++++++++++++++

**Features and Improvements**

- Add experimental `Page Object pattern`_ helpers
- Cover Python 3.8, drop Python 3.4 and Django 1.11 to 2.1 support

**Bugfixes**

- Replace deprecated `multi_db`_ by suggested ``databases`` attribute
- Remove obsolete Python 2 compatibility code

.. _Page Object pattern: https://www.martinfowler.com/bliki/PageObject.html

1.3.0 (2019-04-16)
++++++++++++++++++

**Features and Improvements**

- Add Bandit security linter to CI setup
- Minor refactorings to please linters
- Update and clarify documentation
- Cover Django 2.2 with test matrix, remove Django 2.0

**Bugfixes**

- Fix fixtures decorator behavior (reset between scenarios)

1.2.0 (2018-03-12)
++++++++++++++++++

**Features and Improvements**

- Added option to set `multi_db`_ on TestCase

**Bugfixes**

- Made fixtures decorator compatible with newly released behave

.. _multi_db: https://docs.djangoproject.com/en/stable/topics/testing/tools/#testing-multi-db

1.1.0 (2017-01-29)
++++++++++++++++++

**Features and Improvements**

- Added :code:`django_ready` hook for running setup code within the django environment

1.0.0 (2017-10-25)
++++++++++++++++++

**Features and Improvements**

- Added decorator to load fixtures
- Updated django integration logic

0.5.0 (2017-03-19)
++++++++++++++++++

**Features and Improvements**

- Added :code:`--simple` command line option to run tests using the
  regular :code:`TestCase` class instead of :code:`StaticLiveServerTestCase`

0.4.1 (2017-01-16)
++++++++++++++++++

**Features and Improvements**

- Behave's short form arguments are now accepted (e.g. :code:`-i` for :code:`--include`)
- Added :code:`--keepdb` short form argument, `-k`
- Prefix conflicting command line options with :code:`--behave`

**Bugfixes**

- Fixed specifying paths didn't work

0.4.0 (2016-08-23)
++++++++++++++++++

**Features and Improvements**

- Replace `optparse` with `argparse`
- Support Django 1.8 + 1.9 + 1.10

0.3.0 (2015-10-27)
++++++++++++++++++

**Features and Improvements**

- Added the :code:`--keepdb` flag to reuse the existing test database
  instead of recreating it for every test run. (Django >= 1.8 only)
- Overhaul tests to use Tox and pytest for a better testing experience.

0.2.3 (2015-08-21)
++++++++++++++++++

**Bugfixes**

- Fixed bug where some behave commands do not work

0.2.2 (2015-07-13)
++++++++++++++++++

**Bugfixes**

- Fixed bug where positional arguments don't get sent to behave.

0.2.1 (2015-06-30)
++++++++++++++++++

**Bugfixes**

- Fixed bug where invalid arguments are passed onto behave, making the command fail to execute.

0.2.0 (2015-06-27)
++++++++++++++++++

**Features and Improvements**

- Integration with :code:`behave` is now done via monkey patching.
  Including the :code:`environment.before_scenario()` and
  :code:`environment.after_scenario()` function calls in your
  :code:`environment.py` file is no longer needed.
- A new CLI option, :code:`--use-existing-database`, has been added.
  See the `Configuration docs`_.

**Bugfixes**

- Calling :code:`python manage.py behave --dry-run` does not create a
  test database any longer.

.. _Configuration docs:
    https://behave-django.readthedocs.io/en/latest/configuration.html

0.1.4 (2015-06-08)
++++++++++++++++++

**Features and Improvements**

- :code:`context.get_url()`. URL helper attached to context with built-in
  reverse resolution as a handy shortcut.

0.1.3 (2015-05-13)
++++++++++++++++++

**Features and Improvements**

- Fixture loading. You can now load your fixtures by setting :code:`context.fixtures`.
- behave-django now supports all versions of Django

**Bugfixes**

- The behave command should now correctly return non-zero exit codes when a test fails.

0.1.2 (2015-04-06)
++++++++++++++++++

**Features and Improvements**

- You can now have a :code:`.behaverc` in your project's root directory.
  You can specify where your feature directories are in this file, among
  other things. See the `behave docs on configuration files`_.
- Removed :code:`BEHAVE\_FEATURES` setting in favor of using behave's configuration file

.. _behave docs on configuration files:
    https://behave.readthedocs.io/en/latest/behave.html#configuration-files

0.1.1 (2015-04-04)
++++++++++++++++++

**Features and Improvements**

- Behave management command now accepts behave command line arguments
- :code:`BEHAVE\_FEATURES` settings added for multiple feature directories

**Bugfixes**

- Removed test apps and projects from the release package

0.1.0 (2015-04-02)
++++++++++++++++++

-  Initial release

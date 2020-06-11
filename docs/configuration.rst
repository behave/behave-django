Configuration
=============

Command line options
--------------------

You can use regular *behave* command line options with the ``behave``
management command.

.. code-block:: console

    $ python manage.py behave --tags @wip

Additional command line options provided by *behave-django*:

``--use-existing-database``
***************************

Don't create a test database, and use the database of your default runserver
instead. USE AT YOUR OWN RISK! Only use this option for testing against a
*copy* of your production database or other valuable data. Your tests may
destroy your data irrecoverably.

``--keepdb``
************

Starting with Django 1.8, the ``--keepdb`` flag was added to ``manage.py test``
to facilitate faster testing by using the existing database instead of
recreating it each time you run the test. This flag enables
``manage.py behave --keepdb`` to take advantage of that feature.
|keepdb docs|_.

``--simple``
************

Use Django's simple ``TestCase`` which rolls back the database transaction
after each scenario instead of flushing the entire database. Tests run much
quicker, however HTTP server is not started and therefore web browser
automation is not available.

Behave configuration file
-------------------------

You can use *behave*’s configuration file.  Just create a ``behave.ini``,
``.behaverc``, ``setup.cfg`` or ``tox.ini`` file in your project’s root
directory and behave will pick it up.  You can read more about it in the
`behave docs`_.

For example, if you want to have your features directory somewhere else.
In your ``.behaverc`` file, you can put

.. code-block:: ini

    [behave]
    paths=my_project/apps/accounts/features/
          my_project/apps/polls/features/

*Behave* should now look for your features in those folders.


.. |keepdb docs| replace:: More information about ``--keepdb``
.. _keepdb docs: https://docs.djangoproject.com/en/stable/topics/testing/overview/#the-test-database
.. _behave docs: https://behave.readthedocs.io/en/latest/behave.html#configuration-files

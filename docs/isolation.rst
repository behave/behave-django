Test Isolation
==============

Database transactions per scenario
----------------------------------

Each scenario is run inside a database transaction, just like your
regular TestCases.  So you can do something like:

.. code-block:: python

    @given(u'user "{username}" exists')
    def create_user(context, username):
        # This won't be here for the next scenario
        User.objects.create_user(username=username, password='correcthorsebatterystaple')

And you don’t have to clean the database yourself.

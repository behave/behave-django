Test Coverage
=============

You can integrate Coverage.py with behave-django to find out the test coverage of your code.

Dependencies
------------

At First, you should install Coverage.py dependency

.. code-block:: bash

    $ pip install coverage

Environment.py
--------------

In environment.py , write below code on function before_all to start measuring test coverage

.. code-block:: python

    import coverage

    def before_all(context):
        cov = coverage.Coverage()
        cov.start()
        context.cov = cov

Then write below code to end up measuring test coverage.
You can save the coverage result on html format.

.. code-block:: python

    def after_all(context):
        cov = context.cov
        cov.stop()
        cov.save()
        cov.html_report(directory="./cov")


You can check the test coverage on the web with the following command.

.. code-block:: bash

    $ python -m http.server --directory ./cov
    
Warning for behave-django
-------------------------

Internally, the time before_all is executed seems to be later than the time when django loads the modules set in each app.

So sometimes it is necessary to reload django app's modules for accurate test coverage measurement.

Like this:

.. code-block:: python

    import inspect
    import importlib
    
    def reload_modules():
      import your_app1
      import your_app2

      for app in [your_app1, your_app2]:
          members = inspect.getmembers(app)
          modules = map(
              lambda keyval: keyval[1],
              filter(lambda keyval: inspect.ismodule(keyval[1]), members),
          )
          for module in modules:
              try:
                  importlib.reload(module)
              except:
                  continue

.. code-block:: python

    def before_all(context):
      # cov
      cov = coverage.Coverage()
      cov.start()
      context.cov = cov

      # modules
      reload_modules()

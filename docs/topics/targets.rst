.. _targets:

Targets
=======

Targets encapsulate
a human-readable string
along with a machine-readable locator.
This will help document
exactly what each locator
means to target,
and allows the logs to use a nice name.

Here are two examples
showing how to create targets::

    from selenium.webdriver.common.by import By

    from screenpy import Target


    WELCOME_MESSAGE = Target.the('"Welcome" message').located_by("//h1")
    LOG_IN_LINK = Target.the('"Log In" link').located((By.ID, "#login"))

Let's break that down a little bit,
beginning with ``WELCOME_MESSAGE``.

Target's :meth:`~screenpy.target.Target.the` method
expects a human-readable string
to give the element a log-friendly name.
Then we use
Target's :meth:`~screenpy.target.Target.located_by` method
to assign the actual locator
for the element.
Target is smart enough
to figure out
which strategy this locator uses—
`XPath <https://developer.mozilla.org/en-US/docs/Web/XPath>`_ or `CSS Selector <https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors>`_.

You can also pass a locator tuple
into Target's :meth:`~screenpy.target.Target.located` method,
if you need a different strategy.
See the ``LOG_IN_LINK`` example above.

Targets live
in your :ref:`userinterface-dir` directory,
in individual Python files.
We will talk about this directory more
on the :ref:`filehierarchy` page.

Up Next
-------

The guided tour continues
on the :ref:`actions` page!

Target Class
------------

.. module:: screenpy.target
.. autoclass:: Target
    :members:

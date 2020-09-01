.. _targets:

Targets
=======

Targets encapsulate
a human-readable string
along with a machine-readable locator.
This will help document
exactly what each locator
is meant to target,
and allows the logs to use a nicer name.

Here are two examples
showing how to create targets::

    from selenium.webdriver.common.by import By

    from screenpy import Target


    WELCOME_MESSAGE = Target.the('"Welcome" message').located_by("//h1")
    LOG_IN_LINK = Target.the('"Log In" link').located((By.ID, "#login"))

Let's break that down a little bit.

Target's |Target.the| method
expects a human-readable string
to give the element a log-friendly name.
Then,
Target's |Target.located_by| method
assigns the actual locator described by that name.
Target is smart enough to figure out which strategy—
`XPath <https://www.w3schools.com/xml/xpath_intro.asp>`_ or `CSS Selector <https://www.w3schools.com/cssref/css_selectors.asp>`_—
was used to make this locator.
If you want to use a different locator strategy,
you can specify your own locator tuple
by using Selenium's |By| tags,
and pass that in
to Target's |Target.located| method.

To best organize your targets,
you should keep them in your ``user_interface`` directory.
Each page or component
should have a separate file,
containing the targets
the actors will need to find.

Up Next
-------

The guided tour continues
on the :ref:`actions` page!

Target Class
------------

.. module:: screenpy.target
.. autoclass:: Target
    :members:

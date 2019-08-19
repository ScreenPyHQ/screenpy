.. _targets:

Targets
=======

Targets are a way to encapsulate a human-readable string along with a CSS selector or xpath locator.

To instantiate a target, you might do something like this::

    from screenpy import Target

    EXAMPLE_ELEMENT1 = Target.the("first example element").located_by("//div")
    EXAMPLE_ELEMENT2 = Target.the("second example element").located_by("span.example")

Let's break that down a little bit.

The class method |Target.the| expects a human-readable string to give the element a log-friendly name. That same class method returns the newly instantiated |Target| object, ready to have its |Target.located_by| method called. The |Target.located_by| method takes in the actual locator, which can either be `XPath <https://www.w3schools.com/xml/xpath_intro.asp>`_ or `CSS Selector <https://www.w3schools.com/cssref/css_selectors.asp>`_.

Targets are expected to be defined in your user_interface files, and can then be used in your :ref:`actions`, your :ref:`questions`, and your :ref:`tasks-dir`.


Target Class
------------

.. module:: screenpy.target
.. autoclass:: Target
    :members:

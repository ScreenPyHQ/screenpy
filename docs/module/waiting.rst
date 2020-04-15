.. _waiting:

Wait Strategies
===============

Automated test scripts are *fast*.
When a test runs quickly,
sometimes it can try
to act on an element
that isn't quite ready
or hasn't even been drawn yet.
ScreenPy allows you
to use each
of the prominent waiting strategies.

You can also reference
`Selenium's "Waits" documentation <https://selenium-python.readthedocs.io/waits.html#implicit-waits>`_
for more information.

Explicit Waits
--------------

ScreenPy provides a |Wait| function
to wait for certain elements
to appear,
to be clickable,
to contain text,
or to disappear.
These are included
as a convenience
because they are
the most common strategies required.
If those strategies aren't enough,
you can also pass in your own strategy.
Here are some examples
of how this action
can be used:

.. code-block:: python

    from screenpy.actions import Wait


    # waits 20 seconds for the sign in modal to appear
    Perry.attempts_to(Wait.for_the(LOGIN_MODAL))

    # waits 42 seconds for the welcome banner to disappear
    Perry.attempts_to(Wait(42).seconds_for(THE_WELCOME_BANNER).to_disappear())

    # waits 20 seconds for a custom expected condition
    Perry.attempts_to(Wait.for_the(PROFILE_ICON).using(appears_in_greyscale))


Implicit Waits
--------------

Implicit waiting is handled
at the driver level.
This method of waiting
is less preferable,
but it can be useful
in some situations,
and does prevent a lot of Wait actions
being littered around.
Before you pass the driver in,
you can set the implicit wait timeout like so:

.. code-block:: python

    from selenium.webdriver import Firefox


    driver = Firefox()
    driver.implicitly_wait(30)

    Perry = AnActor.who_can(BrowseTheWeb.using(driver))


Hard Waits
----------

This method of waiting is discouraged.
However,
sometimes you just **need**
to pause the script
for a few moments.

In these situations,
as a last resort,
ScreenPy offers the |Pause| action.
Here are some ways to use it:

.. code-block:: python

    from screenpy.actions import Pause


    Perry.attempts_to(Pause.for_(30).seconds_because("I need to get a new locator."))

    Perry.attempts_to(Pause.for_(500).milliseconds_because("the banner animation must finish."))

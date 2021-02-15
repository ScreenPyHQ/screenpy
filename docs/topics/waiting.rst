.. _waiting:

Wait Strategies
===============

Automated test scripts are *fast*.
When a test runs too fast,
sometimes it can try to act on an element
that isn't quite ready
or doesn't even exist yet.
ScreenPy allows you to use
each of the prominent waiting strategies.

You can also reference
`Selenium's "Waits" documentation <https://selenium-python.readthedocs.io/waits.html#implicit-waits>`_
for more information.

Explicit Waits
--------------

ScreenPy provides a |Wait| action
to wait for the application
to meet a certain condition.
Wait provides direct methods
for many common conditions,
such as |Wait.to_appear|.
You are also able to pass in any other condition,
including custom ones,
if those don't suit your needs.

Here are some examples
of how to use this action::

    from screenpy.actions import Wait


    # waits 20 seconds for the sign in modal to appear
    Perry.attempts_to(Wait.for_the(LOGIN_MODAL))

    # waits 42 seconds for the welcome banner to disappear
    Perry.attempts_to(Wait(42).seconds_for(THE_WELCOME_BANNER).to_disappear())

    # waits 20 seconds for a custom expected condition
    Perry.attempts_to(Wait.for_the(PROFILE_ICON).to(appear_in_greyscale))


Implicit Waits
--------------

The driver handles implicit waiting.
You will set your implicit wait timeout
after you instantiate your driver.
This method of waiting is less preferable,
but it can be useful in some situations.
Here is an example
of setting an implicit wait timeout::

    from selenium.webdriver import Firefox


    driver = Firefox()
    driver.implicitly_wait(30)

    Perry = AnActor.who_can(BrowseTheWeb.using(driver))


**Do not** use both
the implicit wait setting
and explicit waits.
Both strategies will interfere with each other,
which can lead to tests taking
a *very* long time
to error out.

Hard Waits
----------

This method of waiting is not ideal
and is a last resort.
And yet,
sometimes you **need**
to pause for a few moments.

In these situations,
ScreenPy offers the |Pause| action.
Here are some ways to use it::

    from screenpy.actions import Pause


    Perry.attempts_to(Pause.for_(30).seconds_because("manual intervention is required."))

    Perry.attempts_to(Pause.for_(500).milliseconds_because("the banner animation must finish."))

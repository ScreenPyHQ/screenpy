.. _debugging:

Debugging
=========

Debugging in ScreenPy can sometimes be difficult.
If you're used to stepping through code using a debugger,
getting to the part where your |Actor|
is performing their :ref:`actions`
can be difficult.

To aid in debugging,
the |Debug| action class can be used
to drop into a debugger
in the middle of any action chain!
It hooks into Python 3.7+'s `breakpoint` function if it can,
so you can modify your preferred debugger
and turn debugging off
by manipulating the `PYTHONBREAKPOINT` environment variable.
You can read more about this excellent new function
by perusing `PEP553 <https://www.python.org/dev/peps/pep-0553/>`_.

As for the action class,
here's an example of an action chain:

.. code-block:: python

    given(Perry).was_able_to(
        Click.on_the(LOGIN_LINK),
        Enter.the_text(USERNAME).into_the(USERNAME_FIELD),
        Enter.the_password(PASSWORD).into_the(PASSWORD_FIELD),
        Click.on_the(SIGN_IN_BUTTON),
        Wait(60).seconds_for_the(WELCOME_BANNER),
    )

If we know we have some issue
after entering the username and password,
but before clicking the sign in button,
we can add a `Debug()` call there:

.. code-block:: python

    given(Perry).was_able_to(
        Click.on_the(LOGIN_LINK),
        Enter.the_text(USERNAME).into_the(USERNAME_FIELD),
        Enter.the_password(PASSWORD).into_the(PASSWORD_FIELD),
        Debug(),  # gives you a debugger here!
        Click.on_the(SIGN_IN_BUTTON),
        Wait(60).seconds_for_the(WELCOME_BANNER),
    )

Now the test will drop us into either
your chosen debugger
or `pdb`.
You'll need to return a couple times
to get back up to the |Actor| class's |Actor.attempts_to| method.
From there,
you can step through the rest of the actions
one at a time,
or dive into one if you need to!

Alternative Method
------------------

If you just need the actor to hold on a second
while you verify the state of the webpage,
you can use the |Pause| action instead,
like so:

.. code-block:: python

    given(Perry).was_able_to(
        Click.on_the(LOGIN_LINK),
        Enter.the_text(USERNAME).into_the(USERNAME_FIELD),
        Enter.the_password(PASSWORD).into_the(PASSWORD_FIELD),
        Pause.for_(20).seconds_because("I need to see something"),  # stops the execution here for 20 seconds.
        Click.on_the(SIGN_IN_BUTTON),
        Wait(60).seconds_for_the(WELCOME_BANNER),
    )

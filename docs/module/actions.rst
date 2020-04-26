.. _actions:

Actions
=======

Actions are the things that an |Actor| can do,
using their :ref:`abilities`.

Using Actions
-------------

Actions can be used pretty much anywhere.
They will typically be used to create :ref:`tasks`
or move around in your :ref:`features`.
Here is an example of using the |Click| action::

    from screenpy.actions import Click

    from ..user_interface.homepage import LOGIN_LINK


    Perry.attempts_to(Click.on_the(LOGIN_LINK))


Actors will always only *attempt*
to perform an action.
They may not actually have the correct :ref:`abilities`,
after all.
If an actor is unable to perform an action or task,
they will raise an |UnableToPerformError|.

Writing New Actions
-------------------

Occasionally,
you might find that the base actions
don't quite cover
a unique use case you have
for your test suite.
Since Screenplay Pattern is built to be extensible,
it is easy and encouraged
to create your own custom actions
to achieve what you need!
The only requirement for creating more actions
is that they have a ``perform_as`` method defined
which takes in the actor who will perform the action.

A base class for Actions is provided
to ensure the required methods
are defined:
``screenpy.actions.base_action.BaseAction``


Let's take a look
at what an extremely contrived custom action,
``ChecksTheSpelling``,
might look like::

    # actions/checks_the_spelling.py
    from screenpy.actions import BaseAction


    class ChecksTheSpelling(BaseAction):
        @staticmethod
        def of_words_in_the(locator):
            return ChecksSpelling(locator)

        def perform_as(self, the_actor):
            the_actor.uses_ability_to(CheckSpelling).to_check()

        def __init__(self, locator):
            self.locator = locator


ScreenPy attempts to follow a convention
of putting all the static methods first,
then the ``perform_as`` function,
and leaving the dunder methods at the bottom.
This way the most important methods are first
for someone perusing your code.

.. _tasks:

Tasks
-----

Sometimes,
your actors might repeat
the same series of actions
several times.
A grouping of common actions
can be abstracted into a Task
in your :ref:`tasks-dir`.

A common task for Screenplay Pattern suites
is logging in to your application under test.
This login task
might look something like this:

.. code-block:: python

    # tasks/login.py
    import os

    from screenpy import Actor
    from screenpy.actions import BaseAction, Click, Enter

    from ..user_interface.homepage import (
        SIGN_ON_LINK,
        THE_USERNAME_FIELD,
        THE_PASSWORD_FIELD,
        LOGIN_BUTTON,
    )


    class LoginSuccessfully(BaseAction):
        """
        Log in to the application successfully.
        """

        @staticmethod
        def using_credentials(username: str, password: str) -> "LoginSuccessfully":
            """
            Supply the credentials for the account.

            Args:
                username: the username to use.
                password: the password to use.
            """
            return LoginSuccessfully(username, password)

        def perform_as(self, the_actor: Actor) -> None:
            """
            Asks the actor to log in to the application.

            Args:
                the_actor: the actor who will perform this task.

            Raises:
                UnableToPerformError: the actor does not have the ability to
                    BrowseTheWeb.
            """
            the_actor.attempts_to(
                Click.on(SIGN_ON_LINK),
                Wait.for_the(THE_USERNAME_FIELD).to_appear(),
                Enter.the_text(self.username).into(THE_USERNAME_FIELD),
                Enter.the_text(self.password).into(THE_PASSWORD_FIELD),
                Click.on_the(LOGIN_BUTTON)
            )

        def __init__(self, username: str, password: str):
            self.username = username
            self.password = password

And there you have it!
Now all you have to do
is ask your actor
to attempt to ``LoginSuccessfully``,
and you've got the same set of actions everywhere.

Note that tasks,
just like actions,
are required to have a ``perform_as`` method defined.
You can use the ``BaseAction`` class
for tasks as well.

Provided Actions
----------------

Open
^^^^

.. autoclass:: screenpy.actions.open.Open
    :members:

Click
^^^^^

.. autoclass:: screenpy.actions.click.Click
    :members:

Clear
^^^^^

.. autoclass:: screenpy.actions.clear.Clear
    :members:

Enter
^^^^^

.. autoclass:: screenpy.actions.enter.Enter
    :members:

Enter2FAToken
^^^^^^^^^^^^^

.. autoclass:: screenpy.actions.enter_2fa_token.Enter2FAToken
    :members:

Select
^^^^^^

.. module:: screenpy.actions.select
.. autoclass:: Select
    :members:
.. autoclass:: SelectByText
    :members:
.. autoclass:: SelectByIndex
    :members:
.. autoclass:: SelectByValue
    :members:

AcceptAlert
^^^^^^^^^^^

.. autoclass:: screenpy.actions.accept_alert.AcceptAlert
    :members:

DismissAlert
^^^^^^^^^^^^

.. autoclass:: screenpy.actions.dismiss_alert.DismissAlert
    :members:

RespondToThePrompt
^^^^^^^^^^^^^^^^^^

.. autoclass:: screenpy.actions.respond_to_the_prompt.RespondToThePrompt
    :members:

SwitchTo
^^^^^^^^

.. autoclass:: screenpy.actions.switch_to.SwitchTo
    :members:

Chain
^^^^^

.. autoclass:: screenpy.actions.chain.Chain
    :members:

DoubleClick
^^^^^^^^^^^

.. autoclass:: screenpy.actions.double_click.DoubleClick
    :members:

RightClick
^^^^^^^^^^

.. autoclass:: screenpy.actions.right_click.RightClick
    :members:

HoldDown
^^^^^^^^

.. autoclass:: screenpy.actions.hold_down.HoldDown
    :members:

Release
^^^^^^^

.. autoclass:: screenpy.actions.release.Release
    :members:

MoveMouse
^^^^^^^^^

.. autoclass:: screenpy.actions.move_mouse.MoveMouse
    :members:

Wait
^^^^

.. autoclass:: screenpy.actions.wait.Wait
    :members:

Pause
^^^^^

.. autoclass:: screenpy.actions.pause.Pause
    :members:

Debug
^^^^^

.. autoclass:: screenpy.actions.debug.Debug
    :members:

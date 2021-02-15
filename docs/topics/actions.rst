.. _actions:

Actions
=======

Actions are the things that :ref:`actors` can do,
using their :ref:`abilities`.
They are the mechanism
through which your actors
interact with your application.

Using Actions
-------------

Your actors will use actions
during the `Arrange and Act parts <https://docs.microsoft.com/en-us/visualstudio/test/unit-test-basics?view=vs-2019#write-your-tests>`_
of your tests.
Here is an example of using the |Click| action::

    from screenpy.actions import Click

    from ..user_interface.homepage import LOGIN_LINK


    Perry.attempts_to(Click.on_the(LOGIN_LINK))


Actors will always only *attempt*
to perform an action.
They may not actually have the correct :ref:`abilities`,
after all.
If an actor is unable to perform an action or task,
they will raise an |UnableToPerform| exception.

Writing New Actions
-------------------

You may find that the base actions
don't quite cover all
that you need your actors to do.
Since ScreenPy is extensible,
it is easy—and encouraged!—
to create your own custom actions.

Actions must be ``Performable``,
which means they have a ``perform_as`` method.
This method tells the actor
how to use their abilities
to perform the action.
See the :ref:`protocols` page
for more information.

.. _checkthespelling:

Let's take a look
at what a custom action
might look like.
Here is the source
for the extremely contrived
``CheckTheSpelling``::

    # actions/check_the_spelling.py
    from screenpy import AnActor, Target

    from ..abilities import CheckSpelling


    class CheckTheSpelling:
        """Check the spelling of words in a given target.

        Examples:
            the_actor.attempts_to(CheckTheSpelling.of_words_in_the("WELCOME_BANNER")
        """

        @staticmethod
        def of_words_in_the(target: Target) -> "CheckTheSpelling":
            """Set the target to check."""
            return CheckTheSpelling(target)

        @beat("{} checks the spelling of words in {target}")
        def perform_as(self, the_actor: AnActor) -> None:
            """Direct the actor to check the target's spelling."""
            text = self.target.found_by(the_actor).text
            misspelled = []
            for word in text.split(" "):
                correct = the_actor.uses_ability_to(CheckSpelling).to_check(word)
                if not correct:
                    misspelled.append(word)
            if misspelled:
                aside(f"... finding the following misspellings: {', '.join(misspelled)}"

        def __init__(self, target: Target) -> None:
            self.target = target


This action directs the actor
to use their ability
to :ref:`CheckSpelling <checkspelling>`.
Using that ability,
the actor checks the spelling
of words in an element.
If they find any misspelled,
they log the misspellings.

.. _tasks:

Tasks
-----

As you build your test suite,
your actors might repeat
the same series of actions
several times.
Or you may have
a series of actions
that could use a more approachable name.
Luckily,
there is a solution
to both of these issues!

You can abstract any group of actions
into a task
in your :ref:`tasks directory <tasks-dir>`.
Tasks can even call other tasks!

.. _logintask:

Let's look at an example of a task.
A common task for Screenplay Pattern suites
is logging in to your application under test::

    # tasks/login.py
    import os

    from screenpy import Actor
    from screenpy.actions import Click, Enter, Visit
    from screenpy.pacing import beat

    from ..user_interface.homepage import (
        LOGIN_BUTTON,
        PASSWORD_FIELD,
        SIGN_ON_LINK,
        URL,
        USERNAME_FIELD,
    )


    class LogIn:
        """Log in to the application.

        Examples:
            the_actor.attempts_to(LogIn.using(USERNAME, PASSWORD))
        """

        @staticmethod
        def using(username: str, password: str) -> "LogIn":
            """Set the username and password to use."""
            return LogIn(username, password)

        @beat("{} logs in to the application.")
        def perform_as(self, the_actor: Actor) -> None:
            the_actor.attempts_to(
                Visit(URL),
                Wait.for_the(SIGN_ON_LINK),
                Click.on_the(SIGN_ON_LINK),
                Wait.for_the(USERNAME_FIELD).to_appear(),
                Enter.the_text(self.username).into_the(USERNAME_FIELD),
                Enter.the_text(self.password).into_the(PASSWORD_FIELD),
                Click.on_the(LOGIN_BUTTON)
            )

        def __init__(self, username: str, password: str) -> None:
            self.username = username
            self.password = password


Now,
the series of actions
needed to log in
are all described
by the ``LogIn`` task.
Logging will also use
the ``beat`` description
instead of a long list of ``Wait``,
``Click``,
and ``Enter`` actions.


Note that tasks,
like actions,
must be ``Performable``.
See the :ref:`protocols` page for more information.

Up Next
-------

The guided tour continues
on the :ref:`questions` page!

Provided Actions
----------------

These are the actions included in ScreenPy.

.. module:: screenpy.actions

AcceptAlert
^^^^^^^^^^^

.. autoclass:: AcceptAlert
    :members:

AddHeader
^^^^^^^^^

.. autoclass:: AddHeader

Chain
^^^^^

.. autoclass:: Chain
    :members:

Click
^^^^^

.. autoclass:: Click
    :members:

Clear
^^^^^

.. autoclass:: Clear
    :members:

Debug
^^^^^

.. autoclass:: Debug
    :members:

DismissAlert
^^^^^^^^^^^^

.. autoclass:: DismissAlert
    :members:

DoubleClick
^^^^^^^^^^^

.. autoclass:: DoubleClick
    :members:

Enter
^^^^^

.. autoclass:: Enter
    :members:

Enter2FAToken
^^^^^^^^^^^^^

.. autoclass:: Enter2FAToken
    :members:

GoBack
^^^^^^

.. autoclass:: GoBack
    :members:

GoForward
^^^^^^^^^

.. autoclass:: GoForward
    :members:

HoldDown
^^^^^^^^

.. autoclass:: HoldDown
    :members:

MoveMouse
^^^^^^^^^

.. autoclass:: MoveMouse
    :members:

Open
^^^^

.. autoclass:: Open
    :members:

Pause
^^^^^

.. autoclass:: Pause
    :members:

RefreshPage
^^^^^^^^^^^

.. autoclass:: RefreshPage
    :members:

Release
^^^^^^^

.. autoclass:: Release
    :members:

RespondToThePrompt
^^^^^^^^^^^^^^^^^^

.. autoclass:: RespondToThePrompt
    :members:

RightClick
^^^^^^^^^^

.. autoclass:: RightClick
    :members:

Select
^^^^^^

.. autoclass:: Select
    :members:
.. autoclass:: SelectByText
    :members:
.. autoclass:: SelectByIndex
    :members:
.. autoclass:: SelectByValue
    :members:

SendAPIRequest
^^^^^^^^^^^^^^

.. autoclass:: SendAPIRequest
    :members:

SendDELETERequest
^^^^^^^^^^^^^^^^^

.. autoclass:: SendDELETERequest
    :members:

SendGETRequest
^^^^^^^^^^^^^^

.. autoclass:: SendGETRequest
    :members:

SendHEADRequest
^^^^^^^^^^^^^^^

.. autoclass:: SendHEADRequest
    :members:

SendOPTIONSRequest
^^^^^^^^^^^^^^^^^^

.. autoclass:: SendOPTIONSRequest
    :members:

SendPATCHRequest
^^^^^^^^^^^^^^^^^

.. autoclass:: SendPATCHRequest
    :members:

SendPOSTRequest
^^^^^^^^^^^^^^^

.. autoclass:: SendPOSTRequest
    :members:

SetHeaders
^^^^^^^^^^

.. autoclass:: SetHeaders
    :members:

SwitchTo
^^^^^^^^

.. autoclass:: SwitchTo
    :members:

SwitchToTab
^^^^^^^^^^^

.. autoclass:: SwitchToTab
    :members:

Wait
^^^^

.. autoclass:: Wait
    :members:

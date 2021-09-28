.. _actions:

Actions
=======

Actions are the things that :ref:`actors` can do,
using their :ref:`abilities`.
They are the mechanism
through which your Actors
interact with your application.

Using Actions
-------------

Your Actors will use Actions
during the `Arrange and Act parts <https://docs.microsoft.com/en-us/visualstudio/test/unit-test-basics?view=vs-2019#write-your-tests>`_
of your tests.
Here is an example
using the :class:`~screenpy.actions.Click` Action::

    from screenpy.actions import Click

    from ..user_interface.homepage import LOGIN_LINK


    Perry.attempts_to(Click.on_the(LOGIN_LINK))


Actors will always only *attempt*
to perform an Action.
They may not actually have the correct :ref:`abilities`,
after all.
If an Actor is unable to perform an Action or task,
they will raise an |UnableToPerform| exception.

Writing New Actions
-------------------

You may find that the base Actions
don't quite cover all
that you need your Actors to do.
Since ScreenPy is extensible,
it is easy—and encouraged!—
to create your own custom Actions.

Actions must be :class:`~screenpy.protocols.Performable`,
which means they have a :meth:`~screenpy.protocols.Performable.perform_as` method.
This method tells the Actor
how to use their Abilities
to perform the Action.

.. _checkthespelling:

Let's take a look
at what a custom Action
might look like.
Here is the source
for the extremely contrived
``CheckTheSpelling``::

    # actions/check_the_spelling.py
    from screenpy import AnActor, Target

    from ..abilities import CheckSpelling


    class CheckTheSpelling:
        """Check the spelling of words in a given Target.

        Examples:
            the_actor.attempts_to(CheckTheSpelling.of_words_in_the("WELCOME_BANNER")
        """

        @staticmethod
        def of_words_in_the(target: Target) -> "CheckTheSpelling":
            """Set the Target to check."""
            return CheckTheSpelling(target)

        @beat("{} checks the spelling of words in {target}")
        def perform_as(self, the_actor: AnActor) -> None:
            """Direct the Actor to check the Target's spelling."""
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


This Action directs the Actor
to use their Ability
to :ref:`CheckSpelling <checkspelling>`.
Using that Ability,
the Actor checks the spelling
of words in an element.
If they find any misspelled,
they log the misspellings.

.. _tasks:

Tasks
-----

As you build your test suite,
your Actors might repeat
the same series of Actions
several times.
Or you may have
a series of Actions
that could use a more approachable name.
Luckily,
there is a solution
to both of these issues!

You can abstract any group of Actions
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
the series of Actions
needed to log in
are all described
by the ``LogIn`` task.
Logging will also use
the ``beat`` description
instead of a long list of ``Wait``,
``Click``,
and ``Enter`` Actions.


Note thats,
like Actions,
must be :class:`~screenpy.protocols.Performable`.

Describing Performables
-----------------------

ScreenPy will do its best to describe
the tasks you create.
However,
if you need more fluent descriptions,
you can provide a ``describe`` method
which will describe your task.

Let's add this method
to the ``ChecksTheSpelling`` task above::

    def describe(self) -> str:
        return f"Check the spelling of words in the {self.target}"

\... well that was easy.
This method will give
a more descriptive statement
for the Narrator to log
when the Actor is using :class:`~screenpy.actions.Eventually`.
It will turn the logged message from
"Actor tries to check the spelling, eventually."
to
"Actor tries to check the spelling of words in the Welcome Banner, eventually."

Up Next
-------

The guided tour continues
on the :ref:`questions` page!

Provided Actions
----------------

These are the Actions included in ScreenPy.

.. module:: screenpy.actions

AcceptAlert
^^^^^^^^^^^

.. autoclass:: AcceptAlert
    :members:

AddHeader
^^^^^^^^^

.. autoclass:: AddHeader

AttachTheFile
^^^^^^^^^^^^^

.. autoclass:: AttachTheFile

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

Eventually
^^^^^^^^^^

.. autoclass:: Eventually
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

MakeNote
^^^^^^^^

.. autoclass:: MakeNote
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

SaveConsoleLog
^^^^^^^^^^^^^^

.. autoclass:: SaveConsoleLog
    :members:

SaveScreenshot
^^^^^^^^^^^^^^

.. autoclass:: SaveScreenshot
    :members:

See
^^^

.. autoclass:: See
    :members:

SeeAllOf
^^^^^^^^

.. autoclass:: SeeAllOf
    :members:

SeeAnyOf
^^^^^^^^

.. autoclass:: SeeAnyOf
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

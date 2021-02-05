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
they will raise an |UnableToPerform|.

Writing New Actions
-------------------

Occasionally,
you might find that the base actions
don't quite cover all
that you need your actors to do.
Since ScreenPy is built to be extensible,
it is easy and encouraged
to create your own custom actions
to achieve what you need!

Actions must be ``Performable``,
which means they have a ``perform_as`` method
which gives direction to the actor.
See the :ref:`protocols` page for more information.

Let's take a look
at what an extremely contrived custom action,
``CheckTheSpelling``,
might look like::

    # actions/check_the_spelling.py
    from screenpy import AnActor, Target


    class CheckTheSpelling:
        @staticmethod
        def of_words_in_the(target: Target) -> "CheckTheSpelling":
            return CheckTheSpelling(target)

        def perform_as(self, the_actor: AnActor) -> None:
            the_actor.uses_ability_to(CheckSpelling).to_check(self.target)

        def __init__(self, target: Target) -> None:
            self.target = target

.. _tasks:

Tasks
-----

Sometimes,
your actors might repeat
the same series of actions several times,
or you may want a more approachable name
to describe a bunch of ``Click`` and ``Wait`` actions.
Any grouping of actions
can be abstracted into a task
in your :ref:`tasks directory <tasks-dir>`.
You can even call other tasks in a task!

A common task for Screenplay Pattern suites
is logging in to your application under test::

    # tasks/login.py
    import os

    from screenpy import AnActor
    from screenpy.actions import Click, Enter
    from screenpy.pacing import beat

    from ..user_interface.homepage import (
        SIGN_ON_LINK,
        THE_USERNAME_FIELD,
        THE_PASSWORD_FIELD,
        LOGIN_BUTTON,
    )


    class LogInSuccessfully:
        @staticmethod
        def using(username: str, password: str) -> "LogInSuccessfully":
            return LogInSuccessfully(username, password)

        @beat("{} logs in to the application.")
        def perform_as(self, the_actor: AnActor) -> None:
            the_actor.attempts_to(
                Wait.for_the(SIGN_ON_LINK),
                Click.on(SIGN_ON_LINK),
                Wait.for_the(THE_USERNAME_FIELD).to_appear(),
                Enter.the_text(self.username).into(THE_USERNAME_FIELD),
                Enter.the_text(self.password).into(THE_PASSWORD_FIELD),
                Click.on_the(LOGIN_BUTTON)
            )

        def __init__(self, username: str, password: str) -> None:
            self.username = username
            self.password = password

And there you have it!
Now all you have to do is ask your actor
to attempt to ``LogInSuccessfully``,
and you've got the same set of actions everywhere.

Note that tasks,
just like actions,
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

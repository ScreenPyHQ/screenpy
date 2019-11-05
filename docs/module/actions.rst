.. _actions:

Actions
=======

Actions are the things that an |Actor| can do, using their :ref:`abilities`.

Using Actions
-------------

Actions can be used pretty much anywhere. They will typically be used to create :ref:`tasks` or move around in your :ref:`features`. Here is an example of using the |Click| action::

    from screenpy.actions import Click

    from ..user_interface.homepage import LOGIN_LINK


    Perry.attempts_to(Click.on_the(LOGIN_LINK))

Actors will always only *attempt* to perform an action. They may not actually have the correct :ref:`abilities`, after all. If an actor is unable to perform an action or task, they will raise an |UnableToPerformException|.

Writing New Actions
-------------------

Like most things in the Screenplay Pattern, you may realize you need to define your own custom actions. The only requirement for creating more actions is that they have a ``perform_as`` method defined.

A very common custom action is the ``Start`` action, which will start the test on the homepage. Here's what that might look like:

.. code-block:: python

    from screenpy.actions import Open

    from user_interface.homepage import HOME_URL


    class Start(object):
        def perform_as(self, the_actor):
            the_actor.attempts_to(Open.browser_on(self.location))

        @staticmethod
        def on_the_homepage():
            return Start(HOME_URL)

        def __init__(self, location):
            self.location = location


.. _tasks:

Tasks
-----

Sometimes, your actors might repeat the same series of actions several times. A grouping of common actions can be abstracted into :ref:`tasks-dir`.

A common place this might occur is if your actor needs to log in to test your application. This ``Login`` task might look something like this:

.. code-block:: python

    # task/login.py
    import os

    from screenpy.actions import Click, Enter

    from ..user_interface.homepage import (
        SIGN_ON_LINK,
        THE_USERNAME_FIELD,
        THE_PASSWORD_FIELD,
        LOGIN_BUTTON,
    )


    class LoginSuccessfully(object):
        def perform_as(self, the_actor):
            the_actor.attempts_to(
                Click.on(SIGN_ON_LINK).then_wait_for(THE_USERNAME_FIELD),
                Enter.the_text(self.username).into(THE_USERNAME_FIELD),
                Enter.the_text(self.password).into(THE_PASSWORD_FIELD),
                Click.on_the(LOGIN_BUTTON)
            )

        @staticmethod
        def using_credentials(username, password):
            return LoginSuccessfully(username, password)

        def __init__(self, username, password):
            self.username = username
            self.password = password

And there you have it! Now all you have to do is ask your actor to attempt to ``LoginSuccessfully`` and you've got the same set of actions everywhere.

Note that tasks, just like actions, are required to have a ``perform_as`` method defined.

Provided Actions
----------------

Open
^^^^

.. module:: screenpy.actions.open
.. autoclass:: Open
    :members:

Click
^^^^^

.. module:: screenpy.actions.click
.. autoclass:: Click
    :members:

Clear
^^^^^

.. module:: screenpy.actions.clear
.. autoclass:: Clear
    :members:

Enter
^^^^^

.. module:: screenpy.actions.enter
.. autoclass:: Enter
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

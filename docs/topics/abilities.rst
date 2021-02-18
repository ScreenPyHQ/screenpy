.. _abilities:

Abilities
=========

Abilities allow your :ref:`actors` to **do** things.
Actors will leverage their abilities
to perform their role in your test scripts.

Abilities store the state and configuration
for other libraries
so your actors can use them.
They enable your actor
to perform actions
and ask questions
which use the ability.


Granting Abilities
------------------

To grant an Actor an ability,
pass it in using the Actor's
|Actor.who_can| or |Actor.can| methods::

    from screenpy import Actor, AnActor
    from screenpy.abilities import BrowseTheWeb


    # Add abilities on instantiation
    Perry = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())

    # Or add abilities later
    Perry = AnActor.named("Perry")
    Perry.can(BrowseTheWeb.using_safari())

Now Perry can
perform actions
and ask questions
using his ability to |BrowseTheWeb|.
If an action or question uses an ability
which the actor does not have,
the actor will raise an |UnableToPerform| exception.

Writing New Abilities
---------------------

There may be other abilities
your actors need to have
in order to test your application,
besides the ones
contained herein.
ScreenPy encourages you to write your own!

Abilities must be ``Forgettable``,
which means they must have a ``forget`` method.
This method performs any necessary cleanup,
such as closing connections
or deleting objects.
See the :ref:`protocols` page for more information.

.. _checkspelling:

Let's take a look
at what a custom ability
might look like.
Here is the source
for the extremely contrived
``CheckSpelling``::

    # abilities/check_spelling.py
    import enchant

    class CheckSpelling:

        @staticmethod
        def in_english() -> "CheckSpelling":
            """Set the language to English."""
            return CheckSpelling.in_("en_US")

        @staticmethod
        def in_(language: str) -> "CheckSpelling":
            """Specify what language to use"""
            return CheckSpelling(language)

        def to_check(self, word: str) -> bool:
            """Check the spelling of the given word."""
            return self.dictionary.check(word)

        def forget(self) -> None:
            """Clean up the dictionary."""
            del self.dictionary  # I told you this was contrived

        def __init__(self, language: str) -> None:
            self.dictionary = enchant.Dict(language)


``CheckSpelling`` provides an interface
to the `enchant <https://pyenchant.github.io/pyenchant/>`_ library.
The required ``forget`` method
cleans up the ability
when the actor exits.


Up Next
-------

The guided tour continues
on the :ref:`targets` page!

Included Abilities
------------------

These are the abilities included in ScreenPy.

.. module:: screenpy.abilities

AuthenticateWith2FA
^^^^^^^^^^^^^^^^^^^

.. autoclass:: AuthenticateWith2FA
    :members:

BrowseTheWeb
^^^^^^^^^^^^

.. autoclass:: BrowseTheWeb
    :members:

MakeAPIRequests
^^^^^^^^^^^^^^^

.. autoclass:: MakeAPIRequests
    :members:

.. _abilities:

Abilities
=========

Abilities allow your :ref:`actors` to **do** things.
Actors will leverage their Abilities
to perform their role in your test scripts.

Abilities store state and configuration.
They enable your Actor
to perform Actions
and ask Questions
which use the Ability.


Granting Abilities
------------------

To grant an Actor an Ability,
pass it in using the Actor's
:meth:`~screenpy.actor.Actor.who_can` method::

    from screenpy import Actor, AnActor
    from screenpy.abilities import BrowseTheWeb


    # Add abilities on instantiation
    Perry = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())

    # Or add abilities later
    Perry = AnActor.named("Perry")
    Perry.can(BrowseTheWeb.using_safari())

Now Perry can
perform Actions
and ask Questions
using his Ability to |BrowseTheWeb|.
If an Action or Question uses an Ability
which the Actor does not have,
the Actor will raise an |UnableToPerform| exception.

Writing New Abilities
---------------------

There may be other Abilities
your Actors need to have
in order to test your application,
besides the ones
contained herein.
ScreenPy encourages you to write your own!

Abilities must be :class:`~screenpy.protocols.Forgettable`,
which means they must have a :meth:`~screenpy.protocols.Forgettable.forget` method.
This method performs any necessary cleanup,
such as closing connections
or deleting objects.

.. _checkspelling:

Let's take a look
at what a custom Ability
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
The required :meth:`~screenpy.protocols.Forgettable.forget` method
cleans up the Ability
when the Actor exits.


Up Next
-------

The guided tour continues
on the :ref:`targets` page!

Included Abilities
------------------

These are the Abilities included in ScreenPy.

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

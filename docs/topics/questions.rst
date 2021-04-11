.. _questions:

Questions
=========

Actors ask Questions
about the current state of the application.
Questions also leverage
the :ref:`abilities` an Actor has.
They are the first half
(the "actual value")
of ScreenPy's test assertions.

Asking Questions
----------------

In the assertion step,
you will not be asking a Question
without an expected answer.
This is how you do test assertions in ScreenPy::

    from screenpy.actions import See
    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly

    from ..user_interface.homepage import WELCOME_MESSAGE

    #                    ⇩ here is the Question
    Perry.should(See.the(Text.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")))


That |See| Action
is taking in our Question
along with a Resolution.
We'll talk about :ref:`resolutions` next.
For the Question half,
the Actor is using their Ability to |BrowseTheWeb|.
They examine the current state of the application
to find the text
of the welcome message.

|See| takes that answer
and compares it to the expected answer
passed in with the Resolution.
If they match,
a comedy!
Our test passes.
If they do not match,
a tragedy!
Our test fails.

Writing New Questions
---------------------

It is very likely
that you will want to write
some custom Questions.
Questions must be :class:`~screenpy.protocols.Answerable`,
which means they have an :meth:`~screenpy.protocols.Answerable.answered_by` method.

Let's take a look
at what an extremely contrived custom Question,
``MisspelledWords``,
might look like::

    # questions/misspelled_words.py
    from screenpy import Actor, Target

    from ..abilities import CheckSpelling


    class MisspelledWords:
        """Ask about any misspelled words in a given Target.

        Examples::

            the_actor.should(See.the(MisspelledWords.in_(WELCOME_MESSAGE), IsEmpty()))
        """

        @staticmethod
        def in_(target: Target) -> "MisspelledWords":
            """Set the Target to examine."""
            return MisspelledWords(target)

        def answered_by(self, the_actor: Actor) -> str:
            """Ask about the misspelled words contained in the given Target."""
            text = self.target.found_by(the_actor).text
            misspelled_words = []
            for word in text.split(" "):
                correct = the_actor.uses_ability_to(CheckSpelling).to_check(word)
                if not correct:
                    misspelled_words.append(word)
            return misspelled_words

        def __init__(self, target: Target) -> None:
            self.target = target


You may notice the similarities
between this Question
and the :ref:`CheckTheSpelling <checkthespelling>` Action...
well,
i did tell you
these are extremely contrived.

Anyway,
the magic all happens
in the :meth:`~screenpy.protocols.Answerable.answered_by` method.
It leverages the Actor's Ability
and returns the answer it finds.

Up Next
-------

The guided tour continues
on the :ref:`resolutions` page!

Provided Questions
------------------

These are the Questions included in ScreenPy.

.. module:: screenpy.questions

Attribute
^^^^^^^^^

.. autoclass:: Attribute
    :members:

BodyOfTheLastResponse
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: BodyOfTheLastResponse

BrowserTitle
^^^^^^^^^^^^

.. autoclass:: BrowserTitle

BrowserURL
^^^^^^^^^^

.. autoclass:: BrowserURL

Cookies
^^^^^^^

.. autoclass:: Cookies

Element
^^^^^^^

.. autoclass:: Element

List
^^^^

.. autoclass:: List
    :members:

Number
^^^^^^

.. autoclass:: Number
    :members:

Selected
^^^^^^^^

.. autoclass:: Selected
    :members:

StatusCodeOfTheLastResponse
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: StatusCodeOfTheLastResponse

Text
^^^^

.. autoclass:: Text
    :members:

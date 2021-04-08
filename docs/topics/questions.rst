.. _questions:

Questions
=========

Actors ask Questions
about the current state of the application.
Questions also leverage
the :ref:`abilities` an actor has.
They are the first half
(the "actual value")
of ScreenPy's test assertions.

Asking Questions
----------------

In the assertion step,
you will not be asking a question
without an expected answer.
This is how you do test assertions in ScreenPy::

    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly

    from ..user_interface.homepage import WELCOME_MESSAGE

    #                     ⇩ here is the question
    Perry.should_see_the((Text.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")))


That call to |Actor.should_see_the|
is taking in our question
along with a resolution.
We'll talk about :ref:`resolutions` next.
For the question half,
the actor is using their ability to |BrowseTheWeb|.
They examine the current state of the application
to find the text
of the welcome message.

The actor takes that answer
and compares it to the expected answer
passed in with the resolution.
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
some custom questions.
Questions must be :class:`~screenpy.protocols.Answerable`,
which means they have an :meth:`~screenpy.protocols.Answerable.answered_by` method.

Let's take a look
at what an extremely contrived custom question,
``MisspelledWords``,
might look like::

    # questions/misspelled_words.py
    from screenpy import Actor, Target

    from ..abilities import CheckSpelling


    class MisspelledWords:
        """Ask about any misspelled words in a given target.

        Examples:
            the_actor.should_see_the((MisspelledWords.in_(WELCOME_MESSAGE), IsEmpty()))
        """

        @staticmethod
        def in_(target: Target) -> "MisspelledWords":
            """Set the target to examine."""
            return MisspelledWords(target)

        def answered_by(self, the_actor: Actor) -> str:
            """Ask about the misspelled words contained in the given target."""
            text = self.target.found_by(the_actor).text
            misspelled_words = []
            for word in text.split(" "):
                correct = the_actor.uses_ability_to(CheckSpelling).to_check(word)
                if not correct:
                    misspelled_words.append(word)
            return misspelled_words

        def __init__(self, target: Target) -> None:
            self.target = target


You may notice
the similarities between
this question
and the :ref:`CheckTheSpelling <checkthespelling>` Action.
I did tell you
these are extremely contrived.

Anyway,
the magic all happens
in the ``answered_by`` method.
It leverages the actor's ability
and returns the answer it finds.

Up Next
-------

The guided tour continues
on the :ref:`resolutions` page!

Provided Questions
------------------

These are the questions included in ScreenPy.

.. module:: screenpy.questions

List
^^^^

.. autoclass:: List

Number
^^^^^^

.. autoclass:: Number

Text
^^^^

.. autoclass:: Text

Selected
^^^^^^^^

.. autoclass:: Selected

Element
^^^^^^^

.. autoclass:: Element

BrowserTitle
^^^^^^^^^^^^

.. autoclass:: BrowserTitle

BrowserURL
^^^^^^^^^^

.. autoclass:: BrowserURL

Cookies
^^^^^^^

.. autoclass:: Cookies

BodyOfTheLastResponse
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: BodyOfTheLastResponse

StatusCodeOfTheLastResponse
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: StatusCodeOfTheLastResponse

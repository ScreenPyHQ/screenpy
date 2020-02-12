.. _questions:

Questions
=========

Questions are asked by an actor
about the current state
of the page or application.
They are the first half
(the "actual value")
of ScreenPy's test assertions
(the other half,
:ref:`resolutions`,
is next).

Asking Questions
----------------

Typically,
you will not be asking a question
without an expected answer.
This is how you do test assertions in ScreenPy::

    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly

    from ..user_interface.homepage import WELCOME_MESSAGE

    Perry.should_see_the((Text.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")), )

We'll talk about :ref:`resolutions` next,
but that call to |Actor.should_see_the|
is taking in our question.
Behind the curtain,
our actor is investigating
the current state of the application
(using their ability to |BrowseTheWeb|)
to find out what the text actually says
at the locator described by ``WELCOME_MESSAGE``.
They take that answer
and compare it to the expected answer
passed in by the resolution.
If they match,
a comedy!
Our test passes.
If they do not match,
a tragedy!
Our test fails.


Writing New Questions
---------------------

It is very likely
that you may want to write additional questions,
and you are encouraged to do so!
The only prescribed method
for a question class
is an ``asked_by`` method
that takes in an actor.
This method will do the work
of getting the answer to the question.
For example,
you may want to take a look at
the |Text.asked_by| method
of the |Text| class.

A base class for Questions is provided
to ensure the required methods
are defined:
``screenpy.questions.base_question.BaseQuestion``


Provided Questions
------------------

List
^^^^

.. module:: screenpy.questions.list
.. autoclass:: List

Number
^^^^^^

.. module:: screenpy.questions.number
.. autoclass:: Number

Text
^^^^

.. module:: screenpy.questions.text
.. autoclass:: Text

Selected
^^^^^^^^

.. module:: screenpy.questions.selected
.. autoclass:: Selected

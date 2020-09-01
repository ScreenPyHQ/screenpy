.. _questions:

Questions
=========

Questions are asked by an actor
about the current state of the page or application.
They are the first half
(the "actual value")
of ScreenPy's test assertions.

Asking Questions
----------------

Typically,
you will not be asking a question
without an expected answer.
This is how you do test assertions in ScreenPy::

    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly

    from ..user_interface.homepage import WELCOME_MESSAGE

                        # ⇩ here is the question
    Perry.should_see_the((Text.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")), )

That call to |Actor.should_see_the|
is taking in our question
along with a resolution.
We'll talk about :ref:`resolutions` next.
Behind the curtain,
our actor is investigating
the current state of the application
(using their ability to |BrowseTheWeb|)
to find out what the text actually says
at the element targeted by ``WELCOME_MESSAGE``.

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
that you will want to write additional questions,
and you are encouraged to do so!
Questions must be ``Answerable``,
which means they have an ``answered_by`` method.
For more information,
refer to the :ref:`protocols` page.

Let's take a look
at what an extremely contrived custom question,
``TheClassOf``,
might look like::

    from screenpy import AnActor, Target


    class TheClassOf:
        def answered_by(self, the_actor: AnActor) -> str:
            element = self.target.found_by(the_actor)
            return element.get_attribute("class")

        def __init__(self, target: Target) -> None:
            self.target = target

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

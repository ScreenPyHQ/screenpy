.. _resolutions:

Resolutions
===========

Resolutions provide the correct answer to :ref:`questions`.
They are the second half
(the "expected value")
of test assertions in ScreenPy.

Using Resolutions
-----------------

Like questions,
you probably will not use a resolution directly.
You will typically pass a resolution
along with a question
into your actor's |Actor.should_see_the| method::

    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly

    from ..user_interface.homepage import WELCOME_MESSAGE

                                                      # ⇩ here is the resolution
    Perry.should_see_the((Text.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")))

If the expected value
passed in to |ReadsExactly| (``"Welcome!"``)
matches the actual value
retrieved by our |Text| question,
bravo!
Our test passes.
If they do not match,
boo!
Our test fails.

Writing New Resolutions
-----------------------

Resolutions are really just an abstraction barrier
for the truly excellent |PyHamcrest| library.
To add your own resolutions,
create your resolution class
by inheriting from the |BaseResolution| class.
All you need to provide in your resolution
is a ``line`` class property,
which is just a human readable string for the log,
and then to define the ``__init__`` method.

The custom Resolution's ``__init__`` method
will need to set the expected value,
and instantiate the PyHamcrest matcher
that your resolution is masking.

For several examples,
see the source code
of the :ref:`provided_resolutions` below.

Up Next
-------

The guided tour... concludes here!
You should know everything you need
to get started with your first test.

There are some other pages
which should be very helpful to you,
such as :ref:`cookbook` or :ref:`waiting`,
but from here on out the tour is self-guided.

Thanks for using ScreenPy!

.. _provided_resolutions:

Provided Resolutions
--------------------

These are the resolutions included in ScreenPy.

.. module:: screenpy.resolutions

ContainsTheText
^^^^^^^^^^^^^^^

.. autoclass:: ContainsTheText

ContainsTheEntry
^^^^^^^^^^^^^^^^

.. autoclass:: ContainsTheEntry

ContainsTheKey
^^^^^^^^^^^^^^

.. autoclass:: ContainsTheKey

ContainsTheValue
^^^^^^^^^^^^^^^^

.. autoclass:: ContainsTheValue

ContainsTheItem
^^^^^^^^^^^^^^^

.. autoclass:: ContainsTheItem

HasLength
^^^^^^^^^

.. autoclass:: HasLength

IsEmpty
^^^^^^^

.. autoclass:: IsEmpty

IsEqualTo
^^^^^^^^^

.. autoclass:: IsEqualTo

IsNot
^^^^^

.. autoclass:: IsNot

IsVisible
^^^^^^^^^

.. autoclass:: IsVisible

ReadsExactly
^^^^^^^^^^^^

.. autoclass:: ReadsExactly

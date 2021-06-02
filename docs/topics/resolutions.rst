.. _resolutions:

Resolutions
===========

Resolutions provide the correct answer to :ref:`questions`.
They are the second half
(the "expected value")
of test assertions in ScreenPy.

Using Resolutions
-----------------

You will use Resolutions
by pairing them with a :ref:`Question <questions>`.
The |See| Action
accepts that pair to make an assertion::

    from screenpy.actions import See
    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly

    from ..user_interface.homepage import WELCOME_MESSAGE

    #                                                  ⇩ here is the Resolution
    Perry.should(See.the(Text.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")))


|See| will then compare
the value returned by :class:`~screenpy.questions.Text`
to the value passed in to :class:`~screenpy.resolutions.ReadsExactly`.
If the two values match,
bravo!
Our test passes.
If they do not match,
boo!
Our test fails.

Writing New Resolutions
-----------------------

Resolutions are an abstraction barrier
for the excellent |PyHamcrest| library.
To add a custom Resolutions,
you will need to inherit
from the :class:`~screenpy.resolutions.base_resolution.BaseResolution` class.
All you need to provide
in your custom Resolution
is a ``line`` class property
and a set ``matcher_function``.


The ``line`` is a string
that explains what the Resolution expects.
This line appears in the log.
You can use ``{expectation}`` here
to reference the value passed in.

The ``matcher_function``
is either one of |PyHamcrest|'s matchers
or a custom one
that you have written.

It may be necessary
to overwrite the ``__init__`` function
to properly apply the expected arguments
to the matcher.

For several examples,
see the source code
of the :ref:`provided_resolutions` below.

Up Next
-------

The guided tour... concludes here!
You should know everything you need
to get started with your first test.

There are more pages
which are very good reads,
such as :ref:`cookbook` or :ref:`waiting`.
But from here on out the tour is self-guided.

Thanks for using ScreenPy!

.. _provided_resolutions:

Provided Resolutions
--------------------

These are the Resolutions included in ScreenPy.

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

IsClickable
^^^^^^^^^^^

.. autoclass:: IsClickable

IsCloseTo
^^^^^^^^^

.. autoclass:: IsCloseTo

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

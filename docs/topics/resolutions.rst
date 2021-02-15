.. _resolutions:

Resolutions
===========

Resolutions provide the correct answer to :ref:`questions`.
They are the second half
(the "expected value")
of test assertions in ScreenPy.

Using Resolutions
-----------------

You will use resolutions
by pairing them with a :ref:`question <questions>`.
Your actor's |Actor.should_see_the| method
accepts that pair to make an assertion::

    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly

    from ..user_interface.homepage import WELCOME_MESSAGE

    #                                                   ⇩ here is the resolution
    Perry.should_see_the((Text.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")))


The actor will then compare
the value returned by |Text|
to the value passed in to |ReadsExactly|.
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
To add a custom resolutions,
you will need to inherit
from the |BaseResolution| class.
All you need to provide
in your custom resolution
is a ``line`` class property
and an ``__init__`` method.


The ``line`` is a string
that explains what the resolution expects.
This line appears in the log.
You can use ``{expectation}`` here
to reference the value passed in.

The ``__init__`` method
sets the ``expected`` value
and instantiates a PyHamcrest matcher.

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

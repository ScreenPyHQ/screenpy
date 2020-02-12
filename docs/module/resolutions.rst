.. _resolutions:

Resolutions
===========

Resolutions provide an expected answer to questions.
They are the second half
of test assertions
in ScreenPy:
the "expected value".
(The first half are :ref:`questions`,
if you missed that page.)

Using Resolutions
-----------------

Like :ref:`questions`,
you probably will not use
a resolution directly.
You will typically pass a resolution
along with a question
into your actor's
|Actor.should_see_the| method::

    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly

    from ..user_interface.homepage import WELCOME_MESSAGE

    Perry.should_see_the((Text.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")))

In that line of code,
|ReadsExactly| is returning
a |PyHamcrest| matcher.
It will be evaluated later
as |Actor.should_see_the| does its job.
If the expected value
("Welcome!")
matches the actual value
retrieved by our question,
bravo!
Our test passes.
If they do not match,
boo!
Our test fails.


Writing New Resolutions
-----------------------

Resolutions are really
just an abstraction barrier
for the truly excellent
|PyHamcrest| library.
To add your own resolutions,
create your resolution class
by inheriting from the
|BaseResolution| class.
All you need to provide in your resolution
is a ``line`` class property,
which is just a human readable string
for the log,
and then to define
the ``__init__`` method.

The custom Resolution's
``__init__`` method
will need to set
the expected value,
and instantiate the PyHamcrest matcher
that your resolution is masking.
For several examples,
see the documentation
of the :ref:`provided_resolutions` below.

.. _provided_resolutions:

Provided Resolutions
--------------------

ContainsTheText
^^^^^^^^^^^^^^^

.. module:: screenpy.resolutions
.. autoclass:: ContainsTheText

IsEmpty
^^^^^^^

.. autoclass:: IsEmpty

IsEqualTo
^^^^^^^^^

.. autoclass:: IsEqualTo

IsNot
^^^^^

.. autoclass:: IsNot

ReadsExactly
^^^^^^^^^^^^

.. autoclass:: ReadsExactly


===========
Resolutions
===========

Resolutions provide both
the expected value
and the comparison method
to the answer to a Question.
Pairing a Question
and a Resolution
forms the assertion step
to your tests.

There were a couple examples of assertions
in our :ref:`Complete Example`,
both performed by Polly.
One used the built-in :class:`~screenpy.resolutions.Equals` Resolution,
while the other used a custom ``IsPalpable`` Resolution.
Let's examine the latter.

Resolutions are :class:`~screenpy.protocols.Resolvable`.
This means they have a ``resolve`` method,
which calls and returns a "matcher" function
for the assertion.

The "matcher" function
can come from `PyHamcrest <https://github.com/hamcrest/PyHamcrest#pyhamcrest>`__,
or it can be a custom matcher
written by you.

Anyway,
``IsPalpable`` uses the custom matcher
``HasSaturationGreaterThan``.
Here's how those might be assembled::

    # resolutions/matchers/has_at_least_tension_level.py
    from typing import Any

    from hamcrest.core.base_matcher import BaseMatcher
    from hamcrest.core.description import Description


    class HasSaturationGreaterThan(BaseMatcher):
        """Assert that a mood object has at least a specific saturation level."""

        def _matches(self, item: Any) -> bool:
            """Whether the assertion passes."""
            return self.saturation_level <= item.saturation

        def describe_to(self, description: Description) -> None:
            """Describe the passing case."""
            description.append_text(
                f"the mood has a saturation level of at least {self.saturation_level}"
            )

        def describe_mismatch(self, item: Any, mismatch_description: Description) -> None:
            """Description used when a match fails."""
            mismatch_description.append_text(
                f"the saturation level was less than {self.saturation_level}"
            )

        def describe_match(self, item: Any, match_description: Description) -> None:
            """Description used when a negated match fails."""
            match_description.append_text(
                f"the saturation level was at least {self.saturation_level}"
            )

        def __init__(self, saturation_level: int) -> None:
            self.saturation_level = saturation_level


    def is_palpable() -> HasSaturationGreaterThan:
        return HasSaturationGreaterThan(85)

.. code-block:: python

    # resolutions/is_palpable.py
    from hamcrest.core.matcher import Matcher
    from screenpy.pacing import beat

    from .matchers.has_saturation_greater_than import is_palpable


    class IsPalpable(BaseResolution):
        """Match a tension level that is very, very high!!!

        Examples::

            the_actor.should(See.the(AudienceTension(), IsPalpable()))
        """

        @beat("... hoping it's a palpable tension!")
        def resolve(self) -> Matcher[str]:
            """Provide the Matcher to make the assertion."""
            return is_palpable()


That's really all there is
to creating a Resolution!

The End!
========

This is the final step
of the guided example.
If you want to revisit any section,
you can visit the :ref:`guided example` page.

You can also see
the included Resolutions
at the :ref:`resolutions api` page.

Finally,
you may be interested to see
more examples of ScreenPy suites.
There are several in the
`ScreenPy Examples repo! <https://github.com/ScreenPyHQ/screenpy_examples>`__

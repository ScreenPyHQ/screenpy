=========
Questions
=========

When you are ready
to make an assertion
in your test,
your Actor can ask a Question.
The answer to this Question
will be compared
against a Resolution.
This pairing forms an assertion in ScreenPy.

Our :ref:`Complete Example` used two Questions:
``AudienceTension`` and ``TopAudienceReaction``.
Let's see how the latter might look::

    from screenpy import Actor
    from screenpy.pacing import beat

    from ..abilities import PollTheAudience


    class TopAudienceReaction:
        """Ask the audience for their top reaction to a moment.

        Examples::

            the_actor.should(See.the(TopAudienceReaction(), ReadsExactly("Cry")))
        """

        @beat("{} asks the audience for their top reaction.")
        def answered_by(self, the_actor: Actor) -> str:
            """Direct the actor to poll the audience for their top reaction."""
            poll = the_actor.ability_to(PollTheAudience)
            return sorted(poll.for_reactions(), key=keygetter("percent"))[-1]["reaction"]

A Question is :class:`~screenpy.protocols.Answerable`,
which is to say
it has an ``answered_by`` method.

Passing a Question
along with a Resolution
into the :class:`~screenpy.actions.See` Action
is how to make assertions in ScreenPy.
The Question provides the actual value
while the Resolution provides the expected value.

Where to Go from Questions
==========================

* :ref:`resolutions`

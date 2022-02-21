.. _complete example:

================
Complete Example
================

Let's begin
our ScreenPy tour
with an examination
of a complete test file
using `pytest <https://docs.pytest.org>`__.
We'll reference this test file
as we discuss each piece
in the following sections.

For this example,
imagine we have some application
which allows us to control a film camera.
We also have a tool
which allows us
to poll our audience.
We have written
a few test cases
to ensure our control of the camera
produces the expected results::

    from typing import Generator

    import pytest
    from cam_py import Camera
    from screenpy import AnActor, given, then, when
    from screenpy.actions import See
    from screenpy.resolutions import ReadsExactly

    from ..abilities import ControlCameras, PollTheAudience
    from ..actions import (
        JumpToCamera,
        Dolly,
        Pan,
        StartRecording,
        StopRecording,
        Zoom,
    )
    from ..tasks import CutToCloseUp, DollyZoom
    from ..questions import AudienceTension, TopAudienceReaction
    from ..resolutions import IsPalpable


    @pytest.fixture
    def Cameron() -> Generator:
        """Generate our cameraman, Cameron."""
        the_actor = AnActor.named("Cameron").who_can(ControlCameras())
        yield the_actor
        the_actor.exits()


    @pytest.fixture
    def Polly() -> Generator:
        """Generate our audience-polling stats wizard, Polly."""
        the_actor = AnActor.named("Polly").who_can(PollTheAudience())
        yield the_actor
        the_actor.exits()


    def test_dramatic_moment(Cameron: AnActor, Polly: AnActor) -> None:
        """We can use the camera to create dramatic tension."""
        Cameron.has_cleanup_tasks(StopRecording())

        given(Cameron).was_able_to(StartRecording())

        when(Cameron).attempts_to(
            Dolly.left().for_(5).seconds(),
            CutToCloseup.on("Ackerman"),
            DollyZoom.on("Frieda")
        )

        then(Polly).should(See.the(AudienceTension(), IsPalpable()))


    def test_comedic_timing(Cameron: AnActor, Polly: AnActor) -> None:
        """We can use the camera to make funny moments."""
        Cameron.has_cleanup_tasks(StopRecording())
        one = Camera("Shaun")
        two = Camera("Ed")

        given(Cameron).was_able_to(StartRecording.on(one).and_(two))

        when(Cameron).attempts_to(
            Zoom.in().on_camera(one),
            JumpToCamera(two),
            Zoom.out().on_camera(two),
            JumpToCamera(one),
            Pan.left(),
            JumpToCamera(two),
            JumpToCamera(one),
        )

        then(Polly).should(See.the(TopAudienceReaction(), ReadsExactly("Laughing")))

As you can see,
a ScreenPy test
begins with an Actor.
So,
too,
will our discussion!

Start
=====

* :ref:`Actors`

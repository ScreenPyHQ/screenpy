"""
An action to click on an element. An actor must possess the ability to
BrowseTheWeb to perform this action. An actor performs this action like
so:

    the_actor.attempts_to(Click.on_the(LOGIN_LINK))

    the_actor.attempts_to(
        Click.on(THE_MODAL_LAUNCHER).then_wait_for_the(MODAL)
    )
"""


import warnings
from typing import Union

from selenium.common.exceptions import WebDriverException

from ..actor import Actor
from ..exceptions import DeliveryError
from ..pacing import beat
from ..target import Target
from .base_action import BaseAction
from .wait import Wait


class Click(BaseAction):
    """
    Clicks on an element! A Click action is expected to be instantiated
    via its static |Click.on| or |Click.on_the| methods. A typical
    invocation might look like:

        Click.on_the(PROFILE_LINK)

    It can then be passed along to the |Actor| to perform the action.
    """

    target: Target
    action_complete_target: Union[None, Target]

    @staticmethod
    def on_the(target: Target) -> "Click":
        """
        Creates a new Click action with its crosshairs aimed at the
        provided target.

        Args:
            target: The |Target| describing the element to click.

        Returns:
            |Click|
        """
        return Click(target)

    @staticmethod
    def on(target: Target) -> "Click":
        """Syntactic sugar for |Click.on_the|."""
        return Click.on_the(target)

    def then_wait_for_the(self, target: Target) -> "Click":
        """
        Supplies a target to wait for after performing the click.

        This method has been deprecated as of version 1.0.0. Please use
        the included |Wait| action instead. This method will be removed in
        version 2.0.0.

        Args:
            target: The |Target| describing the element to wait for after
                performing the click.

        Returns:
            |Click|
        """
        warnings.warn(
            "Click.then_wait_for_the is deprecated. Please use the new Wait action "
            "instead.",
            DeprecationWarning,
        )

        self.action_complete_target = target
        return self

    def then_wait_for(self, target: Target) -> "Click":
        """Syntactic sugar for |Click.then_wait_for_the|."""
        return self.then_wait_for_the(target)

    @beat("{0} clicks on the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to find the element described by the stored target,
        and then clicks it. May wait for another target to appear, if
        |Click.then_wait_for| had been called.

        Args:
            the_actor: the |Actor| who will perform the action.

        Raises:
            |DeliveryError|: an exception was raised by Selenium.
            |UnableToPerformError|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        element = self.target.found_by(the_actor)

        try:
            element.click()
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to click "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg).with_traceback(e.__traceback__)

        if self.action_complete_target is not None:
            the_actor.attempts_to(Wait.for_the(self.action_complete_target).to_appear())

    def __init__(self, target: Target) -> None:
        self.target = target
        self.action_complete_target = None

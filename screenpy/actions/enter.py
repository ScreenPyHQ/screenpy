from typing import List

from ..abilities.browse_the_web import BrowseTheWeb
from ..pacing import beat, aside, MINOR


class Enter(object):
    """
    Enters text into an input field. An Enter action is expected to be
    instantiated by its static |Enter.the_text| method. A typical
    invocation might look like:

        Enter.the_text("Hello world!").into(COMMENT_FIELD)

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def the_text(text: str) -> "Enter":
        """
        Creates a new Enter action with the provided text. It is expected
        that the next call will be to the instantiated Enter object's
        |Enter.into| method.

        Args:
            text (str): The text to eventually enter.

        Returns:
            |Enter|
        """
        return Enter(text)

    @staticmethod
    def the_keys(text: str) -> "Enter":
        """Syntactic sugar for |Enter.the_text|."""
        return Enter(text)

    def into(self, target: "Target") -> "Enter":
        """
        Supplies the target to enter the text into. This is most likely
        an input field.

        Args:
            target (Target): The |Target| to enter text into.

        Returns:
            |Enter|
        """
        self.target = target
        return self

    def on(self, target: "Target") -> "Enter":
        """Syntactic sugar for |Enter.into|."""
        self.target = target
        return self

    def then_hit(self, *keys: List[str]) -> "Enter":
        """
        Supplies the target to enter the text into. This is most likely
        an input field.

        Args:
            keys (list(str)): A list of keys to hit afterwards. These are
                probably |Keys|, but they can be strings if you know the
                codes.

        Returns:
            |Enter|
        """
        self.following_keys.extend(keys)
        return self

    def then_press(self, *keys: List[str]) -> "Enter":
        """Syntactic sugar for |Enter.then_hit|."""
        self.following_keys.extend(keys)
        return self

    def then_wait_for(self, target: "Target") -> "Enter":
        """
        Supplies the target to wait for after entering text (and hitting
        any additional keys, if this object's |Enter.then_hit| method was
        called).

        Args:
            target (Target): The |Target| to wait for after entering text.

        Returns:
            |Enter|
        """
        self.action_complete_target = target
        return self

    @beat("{0} enters '{text}' into the {target}.", gravitas=MINOR)
    def perform_as(self, the_actor: "Actor") -> None:
        """
        Asks the |Actor| to performs the Enter action, entering the text
        into the targeted input field using their ability to
        |BrowseTheWeb|.

        If this Enter object's |Enter.then_hit| method was called, it will
        also hit the supplied keys. Finally, if the |Enter.then_wait_for|
        method was called, it will wait for the supplied |Target| to
        appear.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToPerformException|: if the actor does not have the
                ability to |BrowseTheWeb|.
        """
        element = self.target.found_by(the_actor)
        element.send_keys(self.text)
        for key in self.following_keys:
            aside("then hits the {} key".format(key))
            element.send_keys(key)
        if self.action_complete_target is not None:
            aside("then waits to see the {}".format(self.action_complete_target))
            the_actor.uses_ability_to(BrowseTheWeb).to_wait_for(
                self.action_complete_target.get_locator()
            )

    def __init__(self, text: str) -> None:
        self.text = text
        self.target = None
        self.action_complete_target = None
        self.following_keys = []


# Natural-language-enabling syntactic sugar
Press = Enter

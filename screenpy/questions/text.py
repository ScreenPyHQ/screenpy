from typing import List, Union


TargetOrNone = Union["Target", None]


class Text(object):
    """
    Asks what text appears in an element or elements, viewed by an|Actor|.
    This question is meant to be instantiated using its static |Text.of|
    or |Text.of_all| methods. Typical invocations might look like:

        Text.of(THE_WELCOME_HEADER)
        Text.of_all(SEARCH_RESULTS)

    It can then be passed along to the |Actor| to ask the question.
    """

    @staticmethod
    def of(target: "Target") -> "Text":
        """
        Provides the target to read.

        Args:
            target (Target): the |Target| describing the element to read.

        Returns:
            |Text|
        """
        return Text(target=target)

    @staticmethod
    def of_all(multi_target):
        """
        Provides the targets to read.

        Args:
            multi_target (Target): the |Target| describing the elements to
                read.

        Returns:
            |Text|
        """
        return Text(multi_target=multi_target)

    def viewed_by(self, the_actor: "Actor") -> Union[str, List[str], None]:
        """
        Investigates the page as viewed by the supplied |Actor| and gives
        their answer.

        Args:
            the_actor (Actor): The |Actor| who will answer the question.

        Returns:
            list(str) or str or None
        """
        if self.multi_target is not None:
            texts = []
            for e in self.multi_target.all_found_by(the_actor):
                texts.append(e.text)

            return texts[0] if len(texts) == 1 else texts
        elif self.target is not None:
            return self.target.found_by(the_actor).text
        else:
            return None

    def __init__(
        self, target: TargetOrNone = None, multi_target: TargetOrNone = None
    ) -> None:
        self.target = target
        self.multi_target = multi_target

from ..abilities.browse_the_web import BrowseTheWeb
from ..pacing import beat, aside, MINOR


class Click(object):
    @beat("{0} clicks on the {target}.", severity=MINOR)
    def perform_as(self, the_actor):
        element = self.target.resolve_for(the_actor)
        element.click()
        if self.action_complete_target is not None:
            aside("then waits to see the {}".format(self.action_complete_target))
            the_actor.uses_ability_to(BrowseTheWeb).to_wait_for(
                self.action_complete_target
            )

    @staticmethod
    def on(target):
        return Click(target)

    def then_wait_for(self, target):
        self.action_complete_target = target
        return self

    def __init__(self, target):
        self.target = target
        self.action_complete_target = None
        self.following_keys = []

from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.decorators import step, MINOR


class Enter(object):
    def into(self, target):
        self.target = target
        return self

    def then_hit(self, *keys):
        self.following_keys.extend(keys)
        return self

    def then_wait_for(self, target):
        self.action_complete_target = target
        return self

    @step("{0} enters '{text}' into the {target}.",
          desc_attrs=['text', 'target'],
          severity=MINOR)
    def perform_as(self, the_actor):
        element = self.target.resolve_for(the_actor)
        element.send_keys(self.text)
        for key in self.following_keys:
            element.send_keys(key)
        if self.action_complete_target:
            the_actor.uses_ability_to(BrowseTheWeb).to_wait_for(
                self.action_complete_target.get_locator())

    @staticmethod
    def the_text(text):
        return Enter(text)

    def __init__(self, text):
        self.text = text
        self.target = None
        self.action_complete_target = None
        self.following_keys = []

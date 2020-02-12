"""
Abilities provide an API for actors to use other libraries to perform
actions. Abilities are granted to actors through their |Actor.who_can| or
|Actor.can| abilities.
"""


from .base_ability import BaseAbility
from .browse_the_web import BrowseTheWeb

__all__ = ["BaseAbility", "BrowseTheWeb"]

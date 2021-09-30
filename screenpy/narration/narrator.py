"""
The Narrator for the screenplay, who informs the audience what the actors are
doing. The Narrator's microphone is modular, allowing for any number of
adapters to be applied. Adapters must follow the Adapter protocol outlined in
screenpy.protocols.
"""

from contextlib import contextmanager
from copy import deepcopy
from typing import (
    Any,
    Callable,
    ContextManager,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
    Union,
)

from screenpy.protocols import Adapter

# pylint: disable=stop-iteration-return
# The above pylint warning may be a false-positive since Narrator calls `next`
# directly instead of iterating over the generators.

Kwargs = Union[Callable, str]
BackedUpNarration = Tuple[str, Dict[str, Kwargs], int]
ChainedNarrations = List[Tuple[str, Dict[str, Kwargs], List]]
Entangled = Tuple[Callable, List[Generator]]

# Levels for gravitas
AIRY = "airy"
LIGHT = "light"
NORMAL = "normal"
HEAVY = "heavy"
EXTREME = "extreme"


def _chainify(narrations: List[BackedUpNarration]) -> ChainedNarrations:
    """Organize backed-up narrations into an encapsulation chain.

    This helper function takes a flat list of narrations and exit levels and
    organizes it into an encapsulation structure. For example:
    [(kwargs1, 1), (kwargs2, 2), (kwargs3, 2), (kwargs4, 3)]
    =>
    [(kwargs1, [(kwargs2, []), (kwargs3, [(kwargs4, [])])])]

    This encapsulation structure can be used by _entangle_chain to correctly
    entangle the backed-up narrations, so each adapter handles them properly.

    This approach was created with help from @Doctor#7942 on Discord. Thanks!
    """
    result: ChainedNarrations = []
    stack = [result]
    # the first narration will have the relative base exit level
    normalizer = (narrations[0][-1] - 1) if narrations else 0
    for channel, channel_kwargs, exit_level in narrations:
        normalized_exit_level = exit_level - normalizer
        if normalized_exit_level == len(stack):
            # this function is a sibling of the previous one
            stack[-1].append((channel, channel_kwargs, []))
        elif normalized_exit_level > len(stack):
            # surface the latest function's child list and append to that
            child_list = stack[-1][-1][-1]
            stack.append(child_list)
            stack[-1].append((channel, channel_kwargs, []))
        else:
            # we've dropped down one or more levels, go back
            stack = stack[: -(len(stack) - normalized_exit_level)]
            stack[-1].append((channel, channel_kwargs, []))
    return result


class Narrator:
    """The narrator conveys the story to the audience."""

    def __init__(self, adapters: Optional[List[Adapter]] = None) -> None:
        self.adapters: List[Adapter] = adapters or []
        self.on_air = True
        self.cable_kinked = False
        self.backed_up_narrations: List[BackedUpNarration] = []
        self.exit_level = 1
        self.kink_exit_level = 0
        self.handled_exception = None

    @contextmanager
    def off_the_air(self) -> Generator:
        """Turns off narration completely during this context."""
        self.on_air = False
        yield
        self.on_air = True

    @contextmanager
    def mic_cable_kinked(self) -> Generator:
        """Put a kink in the microphone line, storing narrations.

        Once this context is left, all stored narrations will be flushed. You
        can call clear_backup to drop all stored narrations, or flush_backup
        to log them all (and clear them afterward).
        """
        previous_kink_level = self.kink_exit_level
        self.cable_kinked = True
        self.kink_exit_level = self.exit_level
        yield
        self.flush_backup()
        self.kink_exit_level = previous_kink_level
        self.cable_kinked = self.kink_exit_level == 1

    def clear_backup(self) -> None:
        """Clear the backed-up narrations from a kinked cable."""
        self._pop_backups_from_exit_level(self.kink_exit_level)

    @contextmanager
    def _increase_exit_level(self) -> Generator:
        """Increase the exit level for kinked narrations."""
        self.exit_level += 1
        yield
        self.exit_level -= 1

    def _pop_backups_from_exit_level(self, level: int) -> List[BackedUpNarration]:
        """Pop all backed-up narrations starting at the given level."""
        keep_narrations = []
        remove_narrations = []

        for narration in self.backed_up_narrations:
            if narration[-1] >= level:
                remove_narrations.append(narration)
            else:
                keep_narrations.append(narration)

        self.backed_up_narrations = keep_narrations
        return remove_narrations

    def flush_backup(self) -> None:
        """Let all the backed-up narration flow through the kink."""
        kinked_narrations = self._pop_backups_from_exit_level(self.kink_exit_level)
        narrations = _chainify(kinked_narrations)
        for adapter in self.adapters:
            full_narration_func = self._entangle_chain(adapter, deepcopy(narrations))
            full_narration_func()
        self.clear_backup()

    @contextmanager
    def _dummy_entangle(self, func: Callable) -> Generator:
        """Give back something that looks like an entangled func.

        If the narrator's mic cable is kinked or they are off-air, we still
        need to give back a context-managed function. We increase the exit
        level as well, for a future un-kinking of the mic cable.
        """
        with self._increase_exit_level():
            yield func

    def _entangle_chain(self, adapter: Adapter, chain: ChainedNarrations) -> Callable:
        """Mimic narration entanglement from a backed-up narration chain."""
        roots: List[Callable] = []
        for channel, channel_kwargs, enclosed in chain:
            with self._entangle_func(channel, [adapter], **channel_kwargs) as root:
                if enclosed:
                    for _, enclosed_kwargs, _ in enclosed:
                        enclosed_kwargs["func"] = root
                    self._entangle_chain(adapter, enclosed)
                roots.append(root)

        return lambda: [root() for root in roots]

    @contextmanager
    def _entangle_func(
        self,
        channel: str,
        adapters: Optional[List[Adapter]] = None,
        **channel_kwargs: Kwargs
    ) -> Generator:
        """Entangle the function in the adapters' contexts, decorations, etc.

        Each adapter yields the function back, potentially applying its own
        context or decorators. We extract the function with that context still
        intact. We will need to close the context as we leave, so we store
        each level of entanglement to leave later.
        """
        if adapters is None:
            adapters = self.adapters
        exits = []
        enclosed_func = channel_kwargs["func"]
        for adapter in adapters:
            channel_kwargs["func"] = enclosed_func
            closure = getattr(adapter, channel)(**channel_kwargs)
            enclosed_func = next(closure)
            exits.append(closure)
        try:
            yield enclosed_func
        finally:
            for exit_ in exits:
                # close the closures
                next(exit_, None)

    def narrate(self, channel: str, **kwargs: Union[Kwargs, None]) -> ContextManager:
        """Speak the message into the microphone plugged in to all the adapters."""
        channel_kws = {key: value for key, value in kwargs.items() if value is not None}
        if not callable(channel_kws["func"]):
            raise TypeError('Narration "func" is not callable.')

        if self.cable_kinked:
            enclosed_func = self._dummy_entangle(channel_kws["func"])
            channel_kws["func"] = lambda: "overflow"
            self.backed_up_narrations.append((channel, channel_kws, self.exit_level))
        else:
            enclosed_func = self._entangle_func(channel, **channel_kws)  # type: ignore

        return enclosed_func

    def announcing_the_act(
        self, func: Callable, line: str, gravitas: Optional[str] = None
    ) -> ContextManager:
        """Narrate the title of the act."""
        if not self.on_air:
            return self._dummy_entangle(func)
        return self.narrate("act", func=func, line=line, gravitas=gravitas)

    def setting_the_scene(
        self, func: Callable, line: str, gravitas: Optional[str] = None
    ) -> ContextManager:
        """Narrate the title of the scene."""
        if not self.on_air:
            return self._dummy_entangle(func)
        return self.narrate("scene", func=func, line=line, gravitas=gravitas)

    def stating_a_beat(self, func: Callable, line: str) -> ContextManager:
        """Narrate an emotional beat."""
        if not self.on_air:
            return self._dummy_entangle(func)
        return self.narrate("beat", func=func, line=line)

    def whispering_an_aside(self, line: str) -> ContextManager:
        """Narrate a conspiratorial aside (as a stage-whisper)."""
        if not self.on_air:
            return self._dummy_entangle(lambda: "<static>")
        return self.narrate("aside", func=lambda: "ssh", line=line)

    def explains_the_error(self, exc: Exception) -> None:
        """Explain the exception to all the adapters."""
        for adapter in self.adapters:
            adapter.error(exc)

    def attaches_a_file(self, filepath: str, **kwargs: Any) -> None:
        """Attach a file for the various adapters."""
        for adapter in self.adapters:
            adapter.attach(filepath, **kwargs)

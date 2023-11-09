"""The Narrator narrates the Screenplay.

The Narrator for the screenplay informs the audience what the actors are doing.
The Narrator's microphone is modular, allowing for any number of adapters to be
applied. Adapters must follow the Adapter protocol outlined in screenpy.protocols.
"""

from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from typing import TYPE_CHECKING

from screenpy.exceptions import UnableToNarrate

# pylint: disable=stop-iteration-return
# The above pylint warning may be a false-positive since Narrator calls `next`
# directly instead of iterating over the generators.

if TYPE_CHECKING:
    from typing import (
        Any,
        Callable,
        ContextManager,
        Dict,
        Generator,
        List,
        Tuple,
        Union,
    )

    from screenpy.protocols import Adapter

    Kwargs = Union[Callable, str]
    BackedUpNarration = Tuple[str, Dict[str, Kwargs], int]
    ChainedNarrations = List[Tuple[str, Dict[str, Kwargs], List]]
    Entangled = Tuple[Callable, List[Generator]]


def _chainify(narrations: list[BackedUpNarration]) -> ChainedNarrations:
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
    for channel, channel_kwargs, exit_level in narrations:
        if exit_level == len(stack):
            # this function is a sibling of the previous one
            stack[-1].append((channel, channel_kwargs, []))
        elif exit_level > len(stack):
            # surface the latest function's child list and append to that
            child_list = stack[-1][-1][-1]
            stack.append(child_list)
            stack[-1].append((channel, channel_kwargs, []))
        else:
            # we've dropped down one or more levels, go back
            stack = stack[: -(len(stack) - exit_level)]
            stack[-1].append((channel, channel_kwargs, []))
    return result


class Narrator:
    """The narrator conveys the story to the audience."""

    def __init__(self, adapters: list[Adapter] | None = None) -> None:
        self.adapters: list[Adapter] = adapters or []
        self.on_air = True
        self.backed_up_narrations: list[list[BackedUpNarration]] = []
        self.exit_level = 1
        self.handled_exception = None

    def attach_adapter(self, adapter: Adapter) -> None:
        """Attach a new adapter to the Narrator's microphone."""
        self.adapters.append(adapter)

    @property
    def cable_kinked(self) -> bool:
        """Whether or not the Narrator's microphone cable is kinked."""
        return len(self.backed_up_narrations) != 0

    @contextmanager
    def off_the_air(self) -> Generator:
        """Turns off narration completely during this context."""
        self.on_air = False
        try:
            yield
        finally:
            self.on_air = True

    @contextmanager
    def mic_cable_kinked(self) -> Generator:
        """Put a kink in the microphone line, storing narrations.

        Once this context is left, all stored narrations will be flushed. You
        can call clear_backup to drop all stored narrations, or flush_backup
        to log them all (and clear them afterward).
        """
        self.backed_up_narrations.append([])
        try:
            yield
        finally:
            self.flush_backup()
            self.backed_up_narrations.pop()

    def clear_backup(self) -> None:
        """Clear the backed-up narrations from a kinked cable."""
        if self.cable_kinked:
            self.backed_up_narrations[-1].clear()

    @contextmanager
    def _increase_exit_level(self) -> Generator:
        """Increase the exit level for kinked narrations."""
        self.exit_level += 1
        try:
            yield
        finally:
            self.exit_level -= 1

    def flush_backup(self) -> None:
        """Let all the backed-up narration flow through the kink."""
        if not self.cable_kinked:
            return

        kinked_narrations = self.backed_up_narrations[-1]
        if len(self.backed_up_narrations) > 1:
            self.backed_up_narrations[-2].extend(kinked_narrations)
        else:
            narrations = _chainify(kinked_narrations)
            for adapter in self.adapters:
                narration_func = self._entangle_chain(adapter, deepcopy(narrations))
                narration_func()
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
        roots: list[Callable] = []
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
        adapters: list[Adapter] | None = None,
        **channel_kwargs: Kwargs,
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
        except Exception as exc:
            self.explains_the_error(exc)
            raise
        finally:
            for exit_ in exits:
                # close the closures
                next(exit_, None)

    def narrate(self, channel: str, **kwargs: Kwargs | None) -> ContextManager:
        """Speak the message into the microphone plugged in to all the adapters."""
        channel_kws = {key: value for key, value in kwargs.items() if value is not None}
        if not callable(channel_kws["func"]):
            msg = 'Narration "func" is not callable.'
            raise UnableToNarrate(msg)

        if self.cable_kinked:
            enclosed_func = self._dummy_entangle(channel_kws["func"])
            channel_kws["func"] = lambda: "overflow"
            self.backed_up_narrations[-1].append(
                (channel, channel_kws, self.exit_level)
            )
        else:
            enclosed_func = self._entangle_func(channel, None, **channel_kws)

        return enclosed_func

    def announcing_the_act(
        self, func: Callable, line: str, gravitas: str | None = None
    ) -> ContextManager:
        """Narrate the title of the act."""
        if not self.on_air:
            return self._dummy_entangle(func)
        return self.narrate("act", func=func, line=line, gravitas=gravitas)

    def setting_the_scene(
        self, func: Callable, line: str, gravitas: str | None = None
    ) -> ContextManager:
        """Narrate the title of the scene."""
        if not self.on_air:
            return self._dummy_entangle(func)
        return self.narrate("scene", func=func, line=line, gravitas=gravitas)

    def stating_a_beat(
        self, func: Callable, line: str, gravitas: str | None = None
    ) -> ContextManager:
        """Narrate an emotional beat."""
        if not self.on_air:
            return self._dummy_entangle(func)
        return self.narrate("beat", func=func, line=line, gravitas=gravitas)

    def whispering_an_aside(
        self, line: str, gravitas: str | None = None
    ) -> ContextManager:
        """Narrate a conspiratorial aside (as a stage-whisper)."""
        if not self.on_air:
            return self._dummy_entangle(lambda: "<static>")
        return self.narrate("aside", func=lambda: "ssh", line=line, gravitas=gravitas)

    def explains_the_error(self, exc: Exception) -> None:
        """Explain the exception to all the adapters."""
        for adapter in self.adapters:
            adapter.error(exc)

    # ANN401 ignored here to allow for new adapters to use any kwargs.
    def attaches_a_file(self, filepath: str, **kwargs: Any) -> None:  # noqa: ANN401
        """Attach a file for the various adapters."""
        for adapter in self.adapters:
            adapter.attach(filepath, **kwargs)

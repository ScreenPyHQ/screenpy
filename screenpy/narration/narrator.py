"""The Narrator narrates the Screenplay.

The Narrator for the screenplay informs the audience what the actors are doing.
The Narrator's microphone is modular, allowing for any number of adapters to be
applied. Adapters must follow the Adapter protocol outlined in screenpy.protocols.

Narration flow
--------------
When things are normal (cable not kinked, on-air), narrating works like this:

    1. A pacing decorator (e.g. ``@beat``) calls ``narrate(channel, ...)``.
    2. ``narrate`` calls ``_entangle_func``, which passes the function through
       each adapter's generator for that channel. Adapters may wrap the
       function, add logging, change indentation, etc.
    3. The entangled function is yielded back inside a ``with`` block.
       The caller runs it, and when the block exits, each adapter's
       generator is closed (triggering any cleanup).

When the mic cable is *kinked* (``mic_cable_kinked`` context), narrations are
stored instead of played immediately. They're kept as a flat list of
``(channel, kwargs, depth)`` tuples, where ``depth`` tracks nesting. When the
kink is released (or ``flush_backup`` is called), the flat list is rebuilt into
a tree and replayed through every adapter, preserving the original nesting.
"""

from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from typing import TYPE_CHECKING

from screenpy.exceptions import UnableToNarrate

if TYPE_CHECKING:
    from collections.abc import Generator
    from contextlib import AbstractContextManager
    from pathlib import Path
    from typing import Any, Callable, Union

    from screenpy.protocols import Adapter

    Kwargs = Union[Callable, str]

    # A single stored narration: (channel_name, channel_kwargs, nesting_depth).
    KinkedNarration = tuple[str, dict[str, Kwargs], int]
    # A node in the rebuilt narration tree: (channel_name, kwargs, children).
    NarrationNode = tuple[str, dict[str, Kwargs], list["NarrationNode"]]


def _build_narration_tree(narrations: list[KinkedNarration]) -> list[NarrationNode]:
    """Rebuild a flat list of kinked narrations into a nested tree.

    Each narration carries a *depth* value (1-based) that records how deeply
    nested it was when it was originally stored.  This function uses a stack to
    reconstruct the parent/child relationships:

    * ``depth == len(stack)``: sibling of the previous node.
    * ``depth > len(stack)``: child of the previous node (go deeper).
    * ``depth < len(stack)``: we've returned to a shallower level (go back).

    For example:
        Input:  [(a, kw, 1), (b, kw, 2), (c, kw, 2), (d, kw, 3)]
        Output: [(a, kw, [(b, kw, []), (c, kw, [(d, kw, [])])])]

    Args:
        narrations: the list of KinkedNarrations to rebuild.

    Returns:
        list[NarrationNode]: the rebuilt narration tree, ready to be narrated.
    """
    root: list[NarrationNode] = []
    # stack[i] is the children-list at depth i.
    # stack[0] is always `root`.
    stack: list[list[NarrationNode]] = [root]

    for channel, kwargs, depth in narrations:
        # Trim the stack back if we've returned to a shallower level.
        while len(stack) > depth:
            stack.pop()

        # Grow the stack if we're entering a deeper level.
        # The new level's parent is always the most-recently-added node.
        while len(stack) < depth:
            stack.append(stack[-1][-1][-1])

        node: NarrationNode = (channel, kwargs, [])
        stack[-1].append(node)

    return root


class Narrator:
    """The narrator conveys the story to the audience.

    Attributes:
        adapters: the list of attached microphone adapters.
        on_air: ``True`` when narration is active.
        backed_up_narrations: a list of kink-level buffers; each buffer is a
            flat list of ``(channel, kwargs, depth)`` tuples recorded while
            the cable was kinked.
        depth: the current nesting depth (1 = top level).  Incremented when
            entering a ``_dummy_entangle`` context, decremented on exit.
        handled_exception: the last exception passed to ``explains_the_error``.
    """

    def __init__(self, adapters: list[Adapter] | None = None) -> None:
        self.adapters: list[Adapter] = adapters or []
        self.on_air = True
        self.backed_up_narrations: list[list[KinkedNarration]] = []
        self.depth = 1
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

        Narrations that happen inside this context are buffered instead of
        being sent to the adapters immediately.

        On exit the buffer is flushed (sent through the adapters in order).
        You can call ``clear_backup`` to drop the buffer, or ``flush_backup``
        to send it early.
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

    def flush_backup(self) -> None:
        """Let all the backed-up narration flow through the kink.

        If there are multiple nested kinks, the narrations are pushed up to
        the parent kink's buffer.  Otherwise they are rebuilt into a tree and
        replayed through every adapter.
        """
        if not self.cable_kinked:
            return

        kinked_narrations = self.backed_up_narrations[-1]
        if len(self.backed_up_narrations) > 1:
            # Push narrations up to the parent kink level.
            self.backed_up_narrations[-2].extend(kinked_narrations)
        else:
            #  kink — replay through every adapter.
            tree = _build_narration_tree(kinked_narrations)
            for adapter in self.adapters:
                self._replay_kinked(adapter, deepcopy(tree))

        self.clear_backup()

    @contextmanager
    def _dummy_entangle(self, func: Callable) -> Generator:
        """Yield the function back without any adapter processing.

        Used in two situations:
        * Off-air: narration is suppressed, but the caller still expects
            a context-managed function.
        * Cable kinked: the narration has been buffered. The depth is tracked
            so the tree can be reconstructed later on flush.
        """
        self.depth += 1
        try:
            yield func
        finally:
            self.depth -= 1

    @contextmanager
    def _entangle_func(
        self,
        channel: str,
        adapters: list[Adapter] | None = None,
        **channel_kwargs: Kwargs,
    ) -> Generator:
        """Pass the function through each adapter's channel generator.

        Each adapter's channel method (e.g. ``adapter.beat()``) is a generator
        that:
        1. Sets up its context (logging, indentation, etc.).
        2. ``yield``s the (possibly wrapped) function back.
        3. Tears down its context when the generator is closed.

        This method chains through every adapter, feeding each one's output as
        the next one's ``func`` argument. The final result is yielded to the
        caller inside a ``with`` block. When the block exits, every adapter
        generator is closed in order, triggering cleanup.
        """
        if adapters is None:
            adapters = self.adapters

        open_contexts = []
        enclosed_func = channel_kwargs["func"]

        # Step into each adapter's context, collecting the wrapped function.
        for adapter in adapters:
            channel_kwargs["func"] = enclosed_func
            context = getattr(adapter, channel)(**channel_kwargs)
            enclosed_func = next(context)  # enter the adapter's context
            open_contexts.append(context)

        try:
            yield enclosed_func
        except Exception as exc:
            self.explains_the_error(exc)
            raise
        finally:
            # Close each adapter's context to trigger teardown.
            for context in open_contexts:
                next(context, None)

    def _replay_kinked(self, adapter: Adapter, tree: list[NarrationNode]) -> None:
        """Replay a tree of kinked narrations through a single adapter.

        Walks the tree depth-first.  For each node the adapter's channel
        generator is entered (which may log, indent, etc.), then children are
        replayed *inside* that context so that nesting/indentation is correct.

        After the tree walk, every top-level entangled function is called.
        This matters for channels like ``act`` and ``scene`` whose adapters
        defer logging until the wrapped function is actually invoked.
        """
        roots: list[Callable] = []

        for channel, kwargs, children in tree:
            with self._entangle_func(channel, [adapter], **kwargs) as entangled:
                if children:
                    # Let children see the parent's entangled function.
                    for _, child_kwargs, _ in children:
                        child_kwargs["func"] = entangled
                    self._replay_kinked(adapter, children)
                roots.append(entangled)

        # Invoke top-level functions (triggers deferred logging for act/scene).
        for root in roots:
            root()

    # ------------------------------------------------------------------
    # Narration entry points
    # ------------------------------------------------------------------

    def narrate(self, channel: str, **kwargs: Kwargs | None) -> AbstractContextManager:
        """Speak the message into the microphone plugged in to all the adapters.

        If the cable is kinked the narration is buffered for later replay;
        otherwise it is sent through the adapters immediately.
        """
        channel_kws = {key: value for key, value in kwargs.items() if value is not None}
        if not callable(channel_kws["func"]):
            msg = 'Narration "func" is not callable.'
            raise UnableToNarrate(msg)

        if self.cable_kinked:
            enclosed_func = self._dummy_entangle(channel_kws["func"])
            channel_kws["func"] = lambda: "overflow"
            self.backed_up_narrations[-1].append((channel, channel_kws, self.depth))
        else:
            enclosed_func = self._entangle_func(channel, None, **channel_kws)

        return enclosed_func

    def announcing_the_act(
        self, func: Callable, line: str, gravitas: str | None = None
    ) -> AbstractContextManager:
        """Narrate the title of the act."""
        if not self.on_air:
            return self._dummy_entangle(func)
        return self.narrate("act", func=func, line=line, gravitas=gravitas)

    def setting_the_scene(
        self, func: Callable, line: str, gravitas: str | None = None
    ) -> AbstractContextManager:
        """Narrate the title of the scene."""
        if not self.on_air:
            return self._dummy_entangle(func)
        return self.narrate("scene", func=func, line=line, gravitas=gravitas)

    def stating_a_beat(
        self, func: Callable, line: str, gravitas: str | None = None
    ) -> AbstractContextManager:
        """Narrate an emotional beat."""
        if not self.on_air:
            return self._dummy_entangle(func)
        return self.narrate("beat", func=func, line=line, gravitas=gravitas)

    def whispering_an_aside(
        self, line: str, gravitas: str | None = None
    ) -> AbstractContextManager:
        """Narrate a conspiratorial aside (as a stage-whisper)."""
        if not self.on_air:
            return self._dummy_entangle(lambda: "<static>")
        return self.narrate("aside", func=lambda: "ssh", line=line, gravitas=gravitas)

    def explains_the_error(self, exc: Exception) -> None:
        """Explain the exception to all the adapters."""
        for adapter in self.adapters:
            adapter.error(exc)

    # ANN401 ignored here to allow for adapters to use needed kwargs.
    def attaches_a_file(
        self, filepath: Path | str, **kwargs: Any  # noqa: ANN401
    ) -> None:
        """Attach a file for the various adapters."""
        for adapter in self.adapters:
            adapter.attach(filepath, **kwargs)

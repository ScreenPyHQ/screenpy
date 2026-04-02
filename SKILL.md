# ScreenPy

Composition-based Screenplay Pattern test framework for Python. Actors are granted Abilities, perform Actions, ask Questions, and verify Resolutions. All via **protocols** (structural subtyping) — no base classes required.

**ScreenPy is the core.** Domain-specific Abilities, Actions, Questions, and Adapters come from extension packages (`screenpy_selenium`, `screenpy_requests`, `screenpy_playwright`, `screenpy_appium`, `screenpy_adapter_allure`). Always check which extensions a project has installed.

**When writing tests**, follow the coding style and conventions of the project under test — match its existing file layout, naming patterns, fixture style, and any custom Actions/Tasks/Questions already in use. Leverage ScreenPy's aliases (e.g. `See(...)` over `See.the(...)`, `Equals` over `IsEqualTo`) to make test code read as close to natural English as possible.

## Protocols

| Concept | Protocol | Method | Purpose |
|---|---|---|---|
| Ability | `Forgettable` | `forget()` | Access to a tool/resource |
| Action/Task | `Performable` | `perform_as(actor)` | Something an Actor does |
| Question | `Answerable` | `answered_by(actor)` | Retrieves a value |
| Resolution | `Resolvable` | `resolve() → Matcher` | Expected-value matcher |

Optional: `Describable` (`describe() → str`) for logging descriptions.

## Test Flow

```python
from screenpy import AnActor, given, when, then
from screenpy.actions import See
from screenpy.resolutions import IsEqualTo

Perry = AnActor.named("Perry").who_can(SomeAbility())

given(Perry).was_able_to(SetUp())          # arrange
when(Perry).attempts_to(DoAction())        # act
then(Perry).should(                        # assert
    See.the(SomeQuestion(), IsEqualTo("expected")),
)
Perry.exit()                               # cleanup + forget abilities
```

`given`/`when`/`then`/`and_` are identity functions returning the Actor. Actor method aliases: `was_able_to`, `did`, `attempts_to`, `tries_to`, `will`, `does`, `should`, `shall` — all equivalent.

## Built-In Actions

`See`, `SeeAllOf`, `SeeAnyOf` — assertions. `Eventually` — retry until timeout. `Either(...).or_(...)` — try/fallback. `Silently` — suppress narration unless error. `MakeNote`/`Log` — store/log values. `Pause` — sleep (requires reason). `Debug` — breakpoint. `AttachTheFile`, `Stop`.

Aliases exist: `Assert=See`, `Quietly=Silently`, `Try=Either`, `Sleep=Pause`, etc.

## Built-In Resolutions

`IsEqualTo` (`Equals`), `IsNot` (`DoesNot`), `ContainsTheText`, `ReadsExactly`, `ContainsTheItem`, `ContainsTheEntry`, `ContainsTheKey`, `ContainsTheValue`, `ContainsItemMatching`, `HasLength`, `IsEmpty`, `IsGreaterThan`, `IsGreaterThanOrEqualTo`, `IsLessThan`, `IsLessThanOrEqualTo`, `IsCloseTo`, `IsInRange`, `StartsWith`, `EndsWith`, `Matches`. All wrap PyHamcrest matchers.

## Pacing & Narration

Decorators narrate through adapters on `the_narrator` (default: `StdOutAdapter`).

- `@act("title")` — suite grouping
- `@scene("title")` — feature grouping
- `@beat("{} does {thing}.")` — step narration (`{}` = actor name, `{thing}` = `self.thing`)
- `aside("message")` — ad-hoc log line

```python
the_narrator.attach_adapter(SomeAdapter())  # add adapters in conftest.py
```

## Director & Notes

```python
when(Perry).attempts_to(MakeNote.of_the(Q()).as_("key"))
# MUST be a separate call — noted_under evaluates at argument-build time
then(Perry).should(See.the(Q2(), IsEqualTo(noted_under("key"))))
```

## Writing Custom Components

**Ability:** class with `forget()`. **Action/Task:** class with `perform_as(actor)` + `@beat`. **Question:** class with `answered_by(actor)`. **Resolution:** class with `describe()` + `resolve() → Matcher` + `@beat`.

```python
# Action example
class ClickOn:
    @beat("{} clicks on the {target}.")
    def perform_as(self, the_actor):
        the_actor.ability_to(BrowseTheWeb).browser.find_element(*self.target).click()
    def describe(self): return f"Click on the {self.target}."
    def __init__(self, target): self.target = target

# Resolution example
class IsPalpable:
    def describe(self): return "A palpable tension."
    @beat("... hoping it's palpable.")
    def resolve(self): return has_saturation_greater_than(85)
    def __init__(self): pass
```

## Settings

Override via code (`settings.TIMEOUT = 60`), env var (`SCREENPY_TIMEOUT=60`), or `[tool.screenpy]` in `pyproject.toml`.

## Cleanup

```python
Perry.has_ordered_cleanup_tasks(A(), B())       # stops on first failure
Perry.has_independent_cleanup_tasks(C(), D())   # runs all regardless
Perry.exit()                                    # runs cleanup + forget
```

## Patterns

```python
# Retry
actor.will(Eventually(See.the(Q(), Equals("done"))).for_(30).seconds())

# Try/fallback
actor.will(Either(TryThis()).or_(DoThat()).ignoring(ValueError))

# Suppress narration
actor.will(Silently(NoisyTask()))

# Multiple assertions
then(actor).should(See.the(Q1(), R1()), See.the(Q2(), R2()))
then(actor).should(SeeAll.the((Q1(), R1()), (Q2(), R2())))  # same as above
then(actor).should(SeeAny.the((Q1(), R1()), (Q2(), R2())))  # passes if any match
```

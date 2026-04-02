===================
AI Agent Skills
===================

ScreenPy ships with a ``SKILL.md`` file
at the root of the repository.
This file teaches AI coding agents
(such as GitHub Copilot, Cursor, or Claude)
how to write Screenplay Pattern tests
using ScreenPy.

Each official ScreenPy extension
will also include its own ``SKILL.md``
describing the Abilities,
Actions,
Questions,
and Resolutions it provides.

Any custom extensions you create
can follow this pattern
by adding their own ``SKILL.md`` files.

What is a Skill File?
=====================

A skill file is a concise reference document
written for AI agents,
not humans.
It describes:

* The concepts and protocols in the library.
* The available Actions,
  Resolutions,
  and other components.
* Common patterns and gotchas.
* How to write custom components.

Agents use this context
to generate correct,
idiomatic ScreenPy tests
without needing to read
the full documentation.

How to Use the Skills
=====================

There are several ways
to make these skills available
to your AI agent.

Workspace Context (Recommended)
-------------------------------

Most modern AI coding tools
automatically index files
in your workspace or repository.
If ScreenPy (and any extensions)
are installed as editable packages
or their source is present in your workspace,
the agent will discover
the ``SKILL.md`` files automatically.

Custom Instructions
-------------------

Many AI tools support custom instruction files
that are loaded into every conversation.
You can reference the ScreenPy skills
from your project's instruction file.

For **GitHub Copilot**,
create a ``.github/copilot-instructions.md``::

    This project uses ScreenPy for testing.
    Refer to the SKILL.md files in the screenpy,
    screenpy_selenium, and screenpy_requests packages
    for usage patterns and conventions.

For **Cursor**,
add a ``.cursorrules`` file
with similar content.

For **Claude Projects**,
paste the relevant skill files
into the project knowledge.

Concatenated Context
--------------------

For token-constrained setups,
you can concatenate the core skill
and any extension skills
into a single file::

    cat \
      .venv/lib/python3.*/site-packages/screenpy/SKILL.md \
      .venv/lib/python3.*/site-packages/screenpy_selenium/SKILL.md \
      > .agent-context/screenpy-skills.md

Then point your agent's custom instructions
at that combined file.

Tips
====

* **Let the agent match your style.**
  The core skill instructs agents
  to follow the conventions
  of your existing test suite.
  The more consistent your tests are,
  the better the agent's output will be.

* **Prefer aliases for readability.**
  The skill encourages agents
  to use ScreenPy's natural-language aliases
  (e.g. ``See(...)`` over ``See.the(...)``,
  ``Equals`` over ``IsEqualTo``)
  so generated tests read like English.

* **Extension skills expand vocabulary.**
  The core skill teaches the framework;
  extension skills teach the domain-specific parts.
  An agent with both
  will generate tests
  that use the right Actions and Questions
  for your technology stack.

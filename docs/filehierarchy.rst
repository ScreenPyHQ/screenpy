==============
File Hierarchy
==============

The key to a good Screenplay Pattern suite
is understanding how the files all fit together.
The hierarchy described herein
is one example
of how your project
can organize and name its files.
Renaming or reorganizing the files
will not break
any of ScreenPy's functionality.

Here is an example hierarchy,
with extra explanation below:

- suite_root

  - features

    - feature1.py

    - etc...

  - tasks

    - task1.py

    - etc...

Features Directory
==================

The feature films!
The story arcs!
The whole point of the suite!
These are the features of your application
that you are testing;
this is where all the actual test files go.

Tasks Directory
===============

Tasks are descriptive ways
to group one or more Actions
that your Actors will do.
There may be many tasks
your Actors will need to perform.

For more information,
see the :ref:`tasks` section!

Directories for Custom Elements
===============================

You may have need of directories
to hold custom :ref:`actions`,
:ref:`questions`,
or :ref:`abilities`.
This is a common thing!

You can name these new directories
after the objects they contain.
This is the organization strategy
followed by ScreenPy itself.
Or,
you know,
whatever works best for your team!

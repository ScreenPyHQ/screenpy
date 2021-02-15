.. _filehierarchy:

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

    - ...

  - tasks

    - task1.py

    - ...

  - ui

    - page1.py

    - ...

.. _features-dir:

Features
--------

The feature films!
The story arcs!
The whole point of the suite!
These are the features of your application
that you are testing;
this is where all the actual test files go.

.. _tasks-dir:

Tasks
-----

Tasks are descriptive ways
to group one or more actions
that your actors will do.
A common task is a :ref:`LogIn <logintask>` task,
which will contain the actions necessary to log in.
There may be many tasks your actors will need to perform.

For more information,
see the :ref:`tasks` section!

.. _userinterface-dir:

User Interface (ui)
-------------------

These files collect
all the locators
and URLs
for the pages of your application.
These will not be
super interesting files;
they're kind of like
the blocking notes
for the screenplay.

Directories for Custom Elements
-------------------------------

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

.. _filehierarchy:

File Hierarchy
==============

The key to a good Screenplay Pattern suite
is understanding how the files all fit together.
The hierarchy described herein is one example
of how the files can be organized and named.
If your team feels strongly
that there are better conventions to follow,
renaming the files will not break
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

  - user_interface

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
A common task is a ``LogIn`` task,
which will contain the actions necessary to log in.
There may be many tasks your actors will need to perform.

For more information,
see the :ref:`tasks` section!

.. _userinterface-dir:

User Interface
--------------

These files collect all the locators
(built using the |Target| class)
and maybe URLs
for the pages of your application.
These probably will not be super interesting files;
they're kind of like the blocking notes for the screenplay.

Additional Directories
----------------------

You may have need of additional directories,
maybe to hold new :ref:`actions`,
:ref:`questions`,
or :ref:`abilities`,
custom to your testing needs.
This is a common thing!

You can follow ScreenPy's organization strategy
in your own test directory,
and just name these additional directories
after the objects they contain.
Or,
you know,
whatever works best for your team!

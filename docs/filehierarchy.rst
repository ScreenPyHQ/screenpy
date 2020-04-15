.. _filehierarchy:

File Hierarchy
==============

The key to a good Screenplay Pattern suite
is understanding how the files all fit together.
The hierarchy described herein
is one example
of how the files can be organized and named.
If your team feels strongly that there are better conventions to follow,
renaming the files will not break
any of ScreenPy's functionality.

Here is an example hierarchy:

- suite_root

  - features        # this is where the actual test files will live

    - feature1.py

    - ...

  - tasks           # groups of actions your actors can perform, with descriptive names

    - task1.py

    - ...

  - user_interface  # files containing locators and/or URLs for each page

    - page1.py

    - ...

You may have other folders,
such as `actions`
or `abilities`,
depending on whether your Actors
need additional capabilities.
The above blueprint

.. _features-dir:

Features
--------

The feature films!
The story arcs!
The whole point of the suite!
These are the features of your application
that you are testing;
this is where
all the actual test files go.

.. _tasks-dir:

Tasks
-----

Tasks are descriptive ways
to group one or more actions
that your actors will do.
A common task is a ``LogIn`` task,
which will contain the actions necessary to log in.
There may be many tasks
your actors will need to perform
in your suite.

For more information,
see the :ref:`tasks` section!

.. _userinterface-dir:

User Interface
--------------

These files collect all the locators
(built using the |Target| class)
and maybe URLs
for the pages of your application.
These probably will not be
super interesting files;
they're kind of like
the blocking notes
for the screenplay.

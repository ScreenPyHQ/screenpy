.. _filehierarchy:

File Hierarchy
==============

The key to a good Screenplay Pattern suite is understanding how the files all fit together. The hierarchy described herein is one example of how the files can be organized and named. If your team feels strongly that there are better conventions to follow, renaming the files will not break any of ScreenPy's functionality.


Here is an example hierarchy:

- suite_root

  - features        # this is where the actual test files will live

    - feature1.py

    - ...

  - questions       # questions your actors will ask about the site

    - question1.py

    - ...

  - tasks           # groups of actions your actors can perform

    - task1.py

    - ...

  - user_interface  # files containing locators for each page

    - page1.py

    - ...

  - requirements.txt  # where you list screenpy!


.. _features-dir:

Features
--------

The feature films! The story arcs! The whole point of the suite! These are the features of your application that you are testing; this is where all the actual test files go.


.. _questions-dir:

Questions
---------

Questions are things your actor asks about the application, to perform a thrilling turnabout (test fail) or a cathartic confirmation (test pass) upon finding the answer. These files are where you will access elements on the page to figure out if your test has passed.

Questions will need to have an ``asked_by`` method defined, which takes in an instantiated |Actor|. For an example, see the |Text.asked_by| method of the built-in |Text| class.


.. _tasks-dir:

Tasks
-----

Tasks are descriptive ways to group one or more actions that your actors will do. A common task is a ``Start`` task, which will instruct the actor to open the browser to the starting page. There may be many tasks your actors will need to do in your suite.

Tasks, like actions, will need to define a ``perform_as`` method that takes in an instantiated |Actor|.


.. _userinterface-dir:

User Interface
--------------

These files collect all the locators (built using the |Target| class) and maybe URLs for the pages of your application. These probably will not be super interesting files, they're kind of like the blocking notes for the screenplay.

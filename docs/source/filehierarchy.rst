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


.. _featuresdir:

Features
--------

The feature films! The story arcs! The whole point of the suite! These are the features of your application that you are testing; this is where all the actual test files go.


.. _questionsdir:

Questions
---------

Questions are things your actor asks about the application, to perform a thrilling turnabout (test fail) or a cathartic confirmation (test pass) upon finding the answer. These files are where you will access elements on the page to figure out if your test has passed.

Questions will need to have a `asked_by` method defined, which takes in an instantiated :class:`|Actor|`.


.. _tasksdir:

Tasks
-----

Tasks are descriptive ways to group one or more actions that your actors will do. A common task is a `Start` task, which will instruct the actor to open the browser to the starting page. There may be many tasks your actors will need to do in your suite.

Tasks, like actions, will need to define a `perform_as` method that takes in an instantiated :class:`|Actor|`.


.. _userinterfacedir:

User Interface
--------------

These files are where you will store all your locators and URLs. Build them using :class:`|Target|` and pass 'em in to actions!

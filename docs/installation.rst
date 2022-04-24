Installation
============

To install ScreenPy,
run the following command
in a `virtual environment <https://docs.python.org/3/library/venv.html>`_:

``pip install screenpy``

Official Extensions
-------------------

There are several extensions to ScreenPy
which are officially recognized.
To install them,
use `pip's extras feature <https://www.python.org/dev/peps/pep-0508/#extras>`__.
You can install multiple options
by separating with commas:

``pip install screenpy[selenium,requests,allure]``

Selenium
++++++++

This extension adds an ability
to ``BrowseTheWeb`` using
`Selenium <https://www.selenium.dev/>`__.
It provides Actors
with several Actions,
Questions,
and Resolutions
to support testing web applications.

``pip install screenpy[selenium]``

Requests
++++++++

This extension adds an ability
to ``MakeAPIRequests`` using
`Requests <https://docs.python-requests.org/en/latest/>`__.
It provides Actors
with several Actions and Questions
to support API testing.

``pip install screenpy[requests]``

PyOTP
+++++

This extension adds an Ability
to ``AuthenticateWith2FA`` using
`PyOTP <https://github.com/pyauth/pyotp>`__.
It uh,
doesn't provide anything else...
currently.
But Actors can use their Ability
to get their 2FA token!
(It's also used by ``screenpy_selenium`` above.)

``pip install screenpy[pyotp]``

Allure
++++++

This extension adds an Adapter
for the :ref:`Narrator <narrator api>`
which enables logging through
`Allure <https://docs.qameta.io/allure-report/>`__.

``pip install screenpy[allure]``

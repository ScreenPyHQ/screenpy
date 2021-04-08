.. _installation:

Installation
============

To install ScreenPy,
run the following command
in a `virtual environment <https://docs.python.org/3/library/venv.html>`_:

``pip3 install screenpy``

This will also install
the ``screenpy-quickstart`` script
and the following dependencies:

1. `Selenium <https://selenium-python.readthedocs.io/>`__
2. |PyHamcrest|
3. `Allure <https://docs.qameta.io/allure/>`__'s pytest plugin
4. `pytest <https://docs.pytest.org/en/latest/>`__
5. `PyOTP <https://pyotp.readthedocs.io/en/latest/>`__

You will also need a |WebDriver|
to connect your code to the browser.
Follow `Selenium's driver installation instructions <https://selenium-python.readthedocs.io/installation.html#drivers>`__
for any browser drivers you need.

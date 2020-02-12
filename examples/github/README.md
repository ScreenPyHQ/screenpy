pytest Example
==============

This example uses [pytest](https://docs.pytest.org/en/latest/)'s test organization style.


Running the Tests
----------
To run the tests, call the following in the project root folder:

    python -m pytest features/

To run the tests with Allure reporting:

    python -m pytest features/ --alluredir allure_report/
    allure serve allure_report

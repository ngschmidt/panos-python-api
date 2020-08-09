# Unit Testing Strategies

[Back to Home Page](https://ngschmidt.github.io/panos-python-api/)

## Validating base code

Prior to primary branch merge, the dev branch is subjected to the following static analysis testing:

* Flake8 Defaults, with 160 Column Maximum width
* YAMLLint Defaults (where applicable)

## Validating API Support

The included unit testing script, `unit-tests.py`, has a for loop that will iterate through all recorded API invocations with an API endpoint, and report back any errors. This is also integrated with a Jenkins pipeline, and is highly repeatable.

Duplicating results is *HIGHLY ENCOURAGED*, and if issues are found please feel free to add them to the GitHub "issues" column. Jenkins build configuration for the `dev` branch is included in the GitHub 'code' project.
